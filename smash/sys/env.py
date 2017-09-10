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
    ''' Neither Config nor its parents defined any exporter for shell variables '''


#----------------------------------------------------------------------#

################################
class Environment:

    def __init__( self, path, pure, *, parent=None ) :

        self.homepath           = path
        self.pure           = pure
        self.parent         = parent
        self.processes      = list()


    ####################
    def build(self):
        ''' run all the exporters '''
        raise NotImplementedError

    def validate( self ) :
        ''' check if the environment state satisfies constraints '''
        raise NotImplementedError

    def initialize(self):
        ''' finalize preparation of the environment '''
        raise NotImplementedError

    def teardown(self):
        ''' clean up the environment when it's no longer needed '''
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
        ''' access to shell state variables '''
        raise NotImplementedError


    ####################
    def run(self, command):
        ''' execute a command within the environment '''
        raise NotImplementedError


#----------------------------------------------------------------------#


#----------------------------------------------------------------------#

class ContextEnvironment( Environment ) :
    ''' Environment within which smash is running,
        could be an explicit smash instance,
        or some implicit unmanaged system environment
    '''

    def __init__( self, cwd, *, pure = False ) :
        super( ).__init__( cwd, pure)

        self.configtree = ConfigTree.from_path(cwd)
        debug( 'CONFIGS:  ', self.configtree, '\n' )
        assert self.configtree.final


    @property
    def instance_template( self ) :
        ''' determine whether the context is an instance, and retrieve its template '''
        return None


    ####################
    def build( self ) :
        ''' do what? '''
        pass

    def validate( self ) :
        ''' defer to instance template '''
        pass

    def initialize( self ) :
        sys.path.append( str( self.homepath ) )
        os.chdir( str( self.homepath ) )

    def teardown( self ) :
        pass


    ####################
    @property
    def variables( self ) :
        return OrderedDict( os.environ )


    ####################
    def run( self, command ) :
        raise NotImplementedError


#----------------------------------------------------------------------#

SUBPROCESS_DELAY = 0.01

################################
class VirtualEnvironment(Environment):
    ''' Environment that is launched as a child of the smash process
        shell variables are supplied by evaluating the 'Environment' __export__ process in the configtree
    '''

    def __init__( self, context:ContextEnvironment, *, pure = True ):
        self.config = context.configtree.env
        super().__init__(self.config.path, pure, parent=context)


    ####################
    def build( self ) :
        ''' create config files '''
        from .plugins import exporters
        for name, target in self.config.exports.items():
            exporter = exporters[name]
            for destination, sections in target.items():
                print('EXPORT {:<10} {:<50} {:<10}'.format(str(name), str(destination), str(sections)))
                result = exporter(self.config, sections, destination)



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

        debug( 'CWD:     ', self.homepath )
        debug( '' )
        variables = self.variables
        debug( '' )
        proc = subprocess.Popen(
            ' '.join(command),
            env     = variables,
            cwd     = str( self.homepath ),
            shell   = True
        )
        pid_shell = proc.pid

        ### collect child pids so they can be stored for later termination
        pids_children = [process.pid for process in psutil.Process( pid_shell ).children( recursive=True )]
        self.processes.extend(pids_children)
        # todo: detect and report when command is not found, or exits with nonzero return

        time.sleep( SUBPROCESS_DELAY )
        proc.terminate( ) #terminate exterior shell
        proc.wait( )
        return pid_shell


#----------------------------------------------------------------------#

#----------------------------------------------------------------------#

import conda
from conda.cli import python_api

################################
class CondaEnvironment( VirtualEnvironment ) :
    '''construct a conda environment, and run commands inside it'''

    def _manage(self, command, *arguments, **kwargs):
        print('manage', self.config)
        python_api.run_command( command, *arguments, **kwargs )

    ####################
    def build( self ) :
        ''' construct a conda environment'''

    def validate( self ) :
        ''' defer to instance template '''

    def initialize( self ) :
        ''' '''

    def teardown( self ) :
        ''' '''

    ####################
    @property
    def variables( self ) :
        raise NotImplementedError

    ####################
    def run( self, command ) :
        raise NotImplementedError

#----------------------------------------------------------------------#

################################
class DockerEnvironment( Environment ) :
    '''construct an environment inside a docker container, and run commands inside it'''
    def __init__( self, cwd, *, pure=False ) :
        super( ).__init__( cwd, pure )

        raise NotImplementedError


    ####################
    def build( self ) :
        ''' construct the docker image '''


    def validate( self ) :
        ''' defer to instance template '''


    def initialize( self ) :
        ''' boot the docker image'''

    def teardown( self ) :
        ''' destroy the docker image'''

    ####################
    @property
    def variables( self ) :
        raise NotImplementedError

    ####################
    def run( self, command ) :
        raise NotImplementedError

#----------------------------------------------------------------------#
class RemoteEnvironment( Environment ):
    ''' connect to a remote environment using ssh'''

    def __init__( self, remote:Environment, *, pure=False ) :
        super( ).__init__( remote.homepath, pure )

        raise NotImplementedError

    ####################
    def build( self ) :
        ''' '''

    def validate( self ) :
        ''' '''

    def initialize( self ) :
        ''' '''

    def teardown( self ) :
        ''' '''

    ####################
    @property
    def variables( self ) :
        raise NotImplementedError

    ####################
    def run( self, command ) :
        raise NotImplementedError

#----------------------------------------------------------------------#

builtin_environments = {
    'context'   : ContextEnvironment,
    'subenv'    : VirtualEnvironment,
    'conda'     : CondaEnvironment,
    'docker'    : DockerEnvironment,
    'remote'    : RemoteEnvironment
}

#----------------------------------------------------------------------#
