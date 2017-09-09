#-- smash.env.virtual

"""
"""


import logging
log = logging.getLogger( name=__name__ )
logging.basicConfig( level=logging.DEBUG )
log.debug = print

from pathlib import Path
from contextlib import contextmanager
from collections import OrderedDict

__all__ = []

import sys
import os
import subprocess
import psutil
import time

class MissingShellExportError(Exception):
    '''Neither Config nor its parents defined any exporter for shell variables'''

#----------------------------------------------------------------------#

class Environment:
    def __init__( self, workdir, configs, pure=False ) :
        self.cwd            = workdir
        self.configtree     = configs
        self.processes      = list()
        self.pure           = pure
        self.parent         = None
        assert configs.final

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

    def run(self, command):
        ''' execute a command within the environment'''
        raise NotImplementedError

    @property
    def variables( self ) :
        ''' access to shell state variables'''
        raise NotImplementedError


#----------------------------------------------------------------------#

class ContextEnvironment( Environment ) :
    ''' Environment within which smash is running,
        could be an explicit smash instance,
        or some implicit unmanaged system environment
    '''
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
    def build( self ) :
        pass

    def validate( self ) :
        pass

    def initialize( self ) :
        self.pure = True

    def teardown( self ) :
        pass

    def run( self, command:list ) :
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


    @property
    def variables( self ) :
        from ..sys.plugins import exporters

        try: # todo: refactor how environment export works. subenv should be the export sink key, and Exporters should push values into it. The virtual environment should just check that sink after exporters have been ran.
            export_subtrees = self.configtree.env.exports['Shell']['subenv']
        except KeyError:
            if self.configtree.env.is_pure:
                raise MissingShellExportError(str(self.configtree.env.filepath)+' and its parents did not define any Exporters for pure virtual environment.')
            else:
                print("Warning: No Shell Exporter defined. Will use only exterior environment variables.")
                return OrderedDict()
        exporter        = exporters['Shell']
        result          = exporter( self.configtree.env, export_subtrees, 'subenv' ).result

        if not self.pure :
            result.update( os.environ )
        return result


#----------------------------------------------------------------------#

@contextmanager
def environment( *args, envclass_=Environment, **kwargs ) -> Environment:
    '''virtual context manager'''
    env = envclass_( *args, **kwargs )
    env.build( )
    env.validate( )
    env.initialize( )
    yield env

    env.teardown( )


@contextmanager
def subenv(*args, **kwargs) -> VirtualEnvironment:
    '''run a subordinate environment within python'''
    with environment( *args, envclass_=VirtualEnvironment, **kwargs ) as e:
        yield e


@contextmanager
def runtime_context( *args, **kwargs ) -> ContextEnvironment:
    '''control the exterior python environment'''
    with environment( *args, envclass_=ContextEnvironment, **kwargs ) as e:
        yield e


#----------------------------------------------------------------------#
