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


#----------------------------------------------------------------------#

class Environment:
    def __init__( self, workdir, configs, pure=False ) :
        self.cwd        = workdir
        self.configs    = configs
        self.processes  = list()
        self.pure       = pure
        self.parent     = None
        assert configs.final

    def build(self):
        raise NotImplementedError

    def initialize(self):
        raise NotImplementedError

    def validate(self):
        raise NotImplementedError

    def teardown(self):
        raise NotImplementedError

    def run(self, command):
        raise NotImplementedError

    @property
    def variables(self):
        from ..sys.plugins import exporters
        export_subtrees = self.configs.env.exports['Environment']['__env__']
        exporter = exporters['Environment']

        result = exporter( self.configs.env ).write( self.cwd )
        if not self.pure:
            result.update(os.environ)

        return result


#----------------------------------------------------------------------#

class ContextEnvironment( Environment ) :
    def build( self ) :
        pass

    def initialize( self ) :
        sys.path.append( str( self.cwd ) )
        os.chdir( str( self.cwd ) )


    def validate( self ) :
        pass

    def teardown( self ) :
        pass

    def run( self, command ) :
        raise NotImplementedError


#----------------------------------------------------------------------#

SUBPROCESS_DELAY = 0.01
class VirtualEnvironment(Environment):
    def build( self ) :
        pass

    def validate( self ) :
        pass

    def initialize( self ) :
        self.pure=True

    def teardown( self ) :
        pass

    def run( self, command:list ) :
        proc        = subprocess.Popen( ' '.join(command), env=self.variables, shell=True )
        pid_shell   = proc.pid

        # collect child pids so they can be stored for later termination
        pids_children = [process.pid for process in psutil.Process( pid_shell ).children( recursive=True )]
        self.processes.extend(pids_children)

        time.sleep( SUBPROCESS_DELAY )
        proc.terminate( ) #terminate exterior shell
        proc.wait( )
        return pid_shell


#----------------------------------------------------------------------#

@contextmanager
def environment( *args, envclass_=Environment, **kwargs ) -> Environment:
    '''virtual context manager'''
    env = envclass_( *args, **kwargs )
    env.build( )
    env.validate( )
    yield env

    env.teardown( )


@contextmanager
def subenv(*args, **kwargs) -> Environment:
    '''run a subordinate environment within python'''
    with environment( *args, envclass_=VirtualEnvironment, **kwargs ) as e:
        yield e


@contextmanager
def runtime_context( *args, **kwargs ) -> Environment:
    '''control the exterior python environment'''
    with environment( *args, envclass_=ContextEnvironment, **kwargs ) as e:
        yield e


#----------------------------------------------------------------------#
