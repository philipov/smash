#-- smash.core.env

"""
"""


from powertools import export
from powertools import AutoLogger
log = AutoLogger()
from powertools.print import dictprint
from powertools import term

from pathlib import Path
from contextlib import contextmanager
from collections import OrderedDict
from collections import deque

import sys
import os
import subprocess
import psutil
import time

from .config import ConfigTree

#----------------------------------------------------------------------#

class MissingShellExportError( Exception ) :
    ''' not config nor its parents defined any exporter for shell variables '''


#----------------------------------------------------------------------#

################################
@export
class Environment:
    ''' represent the state of an environment where commands may be executed '''

    def __init__( self, path, *, pure, parent=None ) :

        self.homepath       = path
        self.pure           = pure
        self.parent         = parent
        self.processes      = list()
        self.results        = deque()
        self.closed         = False

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
    def run(self, *command):
        ''' execute a command within the environment '''
        raise NotImplementedError

    #################### iterator/coroutine interfaces
    #todo: can an environment be represented as a coroutine? send commands in, yield results back out

    def __await__(self):
        return self
    def __iter__(self):
        return self
    def __next__(self):
        if self.closed:
            raise StopIteration(self.results)
        try:
            return self.results.popleft()
        except IndexError as e:
            return None

    def send(self, value):
        return self.run(value)

    def close(self):
        self.closed = True

    def throw(self, exc_type, exc_value=None, traceback=None):
        '''raise exception inside of the __exit__ method??'''
        raise exc_type(self, exc_value, traceback)


#----------------------------------------------------------------------#


#----------------------------------------------------------------------#
@export
class ContextEnvironment( Environment ) :
    ''' Environment within which smash is running,
        could be an explicit smash instance,
        or some implicit unmanaged system environment
    '''

    def __init__( self, cwd, *, pure = False ) :
        super( ).__init__( cwd, pure=pure)

        self.configtree = ConfigTree.from_path(cwd)
        log.debug( 'CONFIGS:  ', self.configtree, '\n' )
        assert self.configtree.final


    @property
    def instance_template( self ) :
        ''' determine whether the context is an instance, and retrieve its template '''
        return None


    ####################
    def build( self ) :
        ''' do what? '''


    def validate( self ) :
        ''' defer to instance template '''


    def initialize( self ) :
        sys.path.append( str( self.homepath ) )
        os.chdir( str( self.homepath ) )

    def teardown( self ) :
        ''' do what? '''


    ####################
    @property
    def variables( self ) :
        return OrderedDict( os.environ )


    ####################
    def run( self, *command ) :
        raise NotImplementedError


#----------------------------------------------------------------------#

SUBPROCESS_DELAY = 0.01

################################
@export
class VirtualEnvironment(Environment):
    ''' Environment that is launched as a child of the smash process
        shell variables are supplied by evaluating the 'Environment' __export__ process in the configtree
    '''

    def __init__( self, context:ContextEnvironment, *, pure = True ):
        self.config = context.configtree.env
        super().__init__(self.config.path, pure=pure, parent=context)


    ####################
    def build( self ) :
        ''' create config files '''
        from .plugins import exporters

        print(term.white('\nBUILD VIRTUAL ENVIRONMENT'))
        for name, target in self.config.exports.items():
            if name == 'Shell': continue
            exporter = exporters[name]

            for destination, sections in target.items():
                print(term.red('\nEXPORT'),' {:<10} {:<50} {:<10} {:<10}'.format(str(name), str(destination), str(sections), str(exporter)) )
                result = exporter(self.config, sections, destination).export()
        print(term.white('\n----------------'))


    def validate( self ) :
        pass

    def initialize( self ) :
        pass

    def teardown( self ) :
        pass


    ####################
    @property
    def variables( self ) :
        from ..core.plugins import exporters

        try : # todo: refactor how environment export works. subenv should be the export sink key, and Exporters should push values into it. The virtual environment should just check that sink after exporters have been ran.
            export_subtrees = self.config.exports['Shell']['subenv']
        except KeyError :
            if self.config.is_pure :
                raise MissingShellExportError( str(
                    self.config.filepath ) + ' and its parents did not define any Exporters for pure virtual environment.' )
            else :
                print( "Warning: No Shell Exporter defined. Will use only exterior environment variables." )
                return OrderedDict( )
        exporter    = exporters['Shell']
        subenv      = exporter( self.config, export_subtrees, 'subenv' ).export()

        result = OrderedDict()
        if not self.pure :
            result.update( os.environ )
        result.update( subenv )
        # log.info()
        # dictprint(result)
        return result


    ####################
    def run( self, *command:tuple) :

        log.print( 'CWD:     ', self.homepath )
        log.print( '' )
        variables = self.variables
        log.print( '' )
        proc = subprocess.Popen(
            ' '.join(str(c) for c in command),
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

# todo: fix 'No cio_test package found.'
# https://github.com/conda/conda/issues/5356


import conda
from conda.cli import python_api

################################
@export
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
    def run( self, *command ) :
        raise NotImplementedError


#----------------------------------------------------------------------#

################################
@export
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
    def run( self, *command ) :
        raise NotImplementedError


#----------------------------------------------------------------------#
@export
class RemoteEnvironment( Environment ):
    ''' connect to a remote environment using ssh'''

    def __init__( self, remote:Environment, *, pure=True ) :
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
    def run( self, *command ) :
        raise NotImplementedError


#----------------------------------------------------------------------#

builtin_environment_types = {
    'context'   : ContextEnvironment,
    'subenv'    : VirtualEnvironment,
    'conda'     : CondaEnvironment,
    'docker'    : DockerEnvironment,
    'remote'    : RemoteEnvironment
}

#----------------------------------------------------------------------#