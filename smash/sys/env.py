#-- smash.env.virtual

"""
"""

__all__ = []

import logging
logging.basicConfig( level=logging.INFO )
from ..utils.out import loggers_for
(debug, info, warning, error, critical) = loggers_for( __name__ )

from pathlib import Path
from contextlib import contextmanager
from collections import OrderedDict

import sys
import os
import subprocess
import psutil
import time

from .config import ConfigTree

#----------------------------------------------------------------------#

class MissingShellExportError( Exception ) :
    '''Neither Config nor its parents defined any exporter for shell variables'''


#----------------------------------------------------------------------#

class Environment:

    def __init__( self, workdir, pure, parent=None ) :
        self.cwd            = workdir

        self.processes      = list()
        self.pure           = pure
        self.parent         = parent


    def build(self):
        ''' prepare artifacts necessary for running the environment'''
        raise NotImplementedError

    def validate( self ) :
        ''' check if the environment state satisfies constraints'''
        raise NotImplementedError

    def initialize(self):
        ''' finalize preparation of the environment'''
        raise NotImplementedError

    def teardown(self):
        ''' clean up the environment when it's no longer needed'''
        raise NotImplementedError

    ####################
    def __enter__( self ) :
        self.build( )
        self.validate( )
        self.initialize( )
        return self

    def __exit__( self, exc_type, exc_value, traceback) :
        self.teardown( )


    ####################
    @property
    def variables( self ) :
        ''' access to shell state variables'''
        raise NotImplementedError


    ####################
    def run(self, command):
        ''' execute a command within the environment'''
        raise NotImplementedError



#----------------------------------------------------------------------#



#----------------------------------------------------------------------#

class ContextEnvironment( Environment ) :
    ''' Environment within which smash is running,
        could be an explicit smash instance,
        or some implicit unmanaged system environment
    '''

    def __init__( self, workdir, *, pure = False ) :
        super( ).__init__( workdir, pure)
        self.configtree = ConfigTree.from_path( workdir )

        debug( 'CONFIGS:  ', self.configtree )
        debug( '' )
        assert self.configtree.final

    def build( self ) :
        pass

    def validate( self ) :
        pass

    def initialize( self ) :
        sys.path.append( str( self.cwd ) )
        os.chdir( str( self.cwd ) )

    def teardown( self ) :
        pass

    def run( self, command ) :
        raise NotImplementedError

    @property
    def variables( self ) :
        raise OrderedDict(os.environ)


#----------------------------------------------------------------------#

SUBPROCESS_DELAY = 0.01
class VirtualEnvironment(Environment):
    ''' Environment that is launched as a child of the smash process
        shell variables are supplied by evaluating the 'Environment' __export__ process in the configtree
    '''

    def __init__( self, context:ContextEnvironment, *, pure = True ):
        super().__init__(context.cwd, pure)
        self.config= context.configtree.env

    def build( self ) :
        pass

    def validate( self ) :
        pass

    def initialize( self ) :
        pass

    def teardown( self ) :
        pass


    ####################
    @property
    def variables( self ) :
        from ..sys.plugins import exporters

        try : # todo: refactor how environment export works. subenv should be the export sink key, and Exporters should push values into it. The virtual environment should just check that sink after exporters have been ran.
            export_subtrees = self.config.exports['Shell']['subenv']
        except KeyError :
            if self.config.is_pure :
                raise MissingShellExportError( str(
                    self.config.filepath ) + ' and its parents did not define any Exporters for pure virtual environment.' )
            else :
                print( "Warning: No Shell Exporter defined. Will use only exterior environment variables." )
                return OrderedDict( )
        exporter = exporters['Shell']
        result = exporter( self.config, export_subtrees, 'subenv' ).result

        if not self.config.is_pure or not self.pure :
            result.update( os.environ )
        return result


    ####################
    def run( self, command:tuple) :
        proc        = subprocess.Popen( ' '.join(command), env=self.variables, shell=True )
        pid_shell   = proc.pid

        ### collect child pids so they can be stored for later termination
        pids_children = [process.pid for process in psutil.Process( pid_shell ).children( recursive=True )]
        self.processes.extend(pids_children)
        # todo: detect and report when command is not found, or exits with nonzero return

        time.sleep( SUBPROCESS_DELAY )
        proc.terminate( ) #terminate exterior shell
        proc.wait( )
        return pid_shell






#----------------------------------------------------------------------#
