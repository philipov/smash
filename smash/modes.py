#-- smash.modes

"""
callback functions implementing the action selected by the first command-line parameter.
"""

import logging
log = logging.getLogger( name=__name__ )
logging.basicConfig( level=logging.DEBUG )
debug = print
info = print


from pathlib import Path

#todo: use coroutines that yield for user input

from .core.env import ContextEnvironment
from .core.env import VirtualEnvironment

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
def do_run(*command, context:ContextEnvironment, verbose=False):
    with VirtualEnvironment(context) as interior:
        info( "\nExecute target shell command inside an environment" )
        shell = interior.run(command)
        print("\ninterior.processes", interior.processes)

    print('interior.run:', shell)
    return True


@export
def do_open( *target, context: ContextEnvironment, verbose=False ):

    info( "Run target file using associated command inside an environent" )


@export
def do_test( *target, context:ContextEnvironment, verbose=False ):

    info( "Run tests for a target package" )


@export
def do_build( *target, context:ContextEnvironment, verbose=False ):

    info( "Build executable distribution archive" )


@export
def do_install( *target, context:ContextEnvironment, verbose=False ):

    info( "Create new system root in target directory" )
    from .boot.strap import install_configsystem
    install_root = Path(target[0])
    return install_configsystem(install_root)


@export
def do_pkg( *target, context:ContextEnvironment, verbose=False ):

    info( "Package Manager" )


@export
def do_env( *target, context:ContextEnvironment, verbose=False ):

    info( "Environment Manager" )


@export
def __default__( *target, context:ContextEnvironment, verbose=False ):

    info( "Unknown Command", )




#----------------------------------------------------------------------#
