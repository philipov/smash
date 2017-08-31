#-- smash.modes

"""
callback functions implementing the action selected by the first command-line parameter.
"""

import logging
log = logging.getLogger( name="smash.modes" )
logging.basicConfig( level=logging.DEBUG )
debug = print
info = print

import sys
import os
from pathlib import Path

#todo: use coroutines that yield for user input

#----------------------------------------------------------------------#

__all__ = []

def export( obj ) :
    try :
        __all__.append( obj.__name__ )
    except AttributeError :
        __all__.append( obj.__main__.__name__ )
    return obj

#----------------------------------------------------------------------#

@export
def do_cmd(*target, workdir, configs, verbose=False):
    info( "Execute target shell command inside an environment" )

    # subenv  = proc.build_subenv( config, pure_mode=pure_mode )

    sys.path.append(str(workdir) )
    os.chdir(str(workdir))

    # subenv = proc.build_subenv(configs)


    # (shell, children) = proc.execute(args, subenv)
    return True

@export
def do_open( *target, workdir, configs, verbose=False ):
    info( "Run target file using associated command inside an environent" )


@export
def do_test( *target, workdir, configs, verbose=False ):
    info( "Run tests for a target package" )


@export
def do_build( *target, workdir, configs, verbose=False ):
    info( "Build executable distribution archive" )


@export
def do_install( *target, workdir, configs, verbose=False ):
    info( "Create new system root in target directory" )
    from .sys.manager import install_configsystem
    install_root = Path(target[0])
    return install_configsystem(install_root)


@export
def do_pkg( *target, workdir, configs, verbose=False ):
    info( "Package Manager" )


@export
def do_env( *target, workdir, configs, verbose=False ):
    info( "Environment Manager" )

@export
def __default__( *target, workdir, configs, verbose=False ):
    info( "Unknown Command", )




#----------------------------------------------------------------------#
