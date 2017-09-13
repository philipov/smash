#-- smash.__main__

'''
application entry point
'''

from powertools import export
from powertools import AutoLogger
log = AutoLogger()

###
import colorama
colorama.init( )
import colored_traceback
colored_traceback.add_hook( )

import os
import sys
import traceback
import argparse

from pathlib import Path
from collections import namedtuple
from collections import deque

from .core.env import ContextEnvironment
from .core.env import VirtualEnvironment

#----------------------------------------------------------------------#

_argnames = list( )
_parser = argparse.ArgumentParser(
    description="Smart Shell"
)

def _add_argument( name, options=(), **kwargs ) :
    _parser.add_argument( *options, dest=name, **kwargs )
    _argnames.append( name )

#################### main
_add_argument( 'command',
               type=str,
               nargs=argparse.REMAINDER,
               help='executed inside subenvironment',
               )

#################### flags

_add_argument( 'verbose',
               options=('-v', '--verbose'),
               action='store_true',
               help='print extra information'
               )

####################
Arguments = namedtuple( 'Arguments', _argnames )


####################
@export
def parse( argv: list = None ) -> Arguments :
    args = _parser.parse_args( argv )
    return Arguments( **args.__dict__ )


#----------------------------------------------------------------------#


def main( args: Arguments ) :
    # ToDo: initialize logging: stdout/stderr redirect
    # ToDo: handle dev mode
    # ToDo: manage env list
    # ToDo: manage package list

    log.print( '~~~~~~~~~~~~~~~~~~~~ SMASH-BOOT')
    log.print( 'SCRIPT:  ', __file__ )
    log.print( 'TARGET:  ', args.command )

    cwd = Path( os.getcwd() )
    log.print( 'IWD:     ', cwd )
    log.print( '' )

    if args.verbose:
        from .core.plugins import report_plugins
        report_plugins()

    result = None
    with ContextEnvironment(cwd) as context:
        import re
        from smash.core.plugins import handlers
        from smash.core.handler import NoHandlerMatchedError

        log.info( "\nRun target file using associated command inside an environent" )
        arguments   = deque( args.command )
        filepath    = Path( arguments.popleft( ) )

        with VirtualEnvironment( context ) as interior :
            for pattern, Handler in handlers.items( ) :
                if re.match( pattern, filepath.name ) :
                    result = Handler( filepath, arguments, interior ).run( )
                    break
            else :
                raise NoHandlerMatchedError( filepath, handlers )

            print( "\ninterior.processes", interior.processes )


    log.print( '' )
    log.print( 'SMASH DONE...' )
    return result




##############################
def console( args=None ) :
    '''bind main to command-line argmuntes; print exceptions'''

    try :
        if args is None :
            args = sys.argv[1 :]
        return main( parse(args) )

    except Exception as err :
        traceback.print_tb( err.__traceback__ )
        log.print( sys.exc_info( )[0].__name__ + ':', err )
        input( '\nPress ENTER to continue...' )


##############################
if __name__ == '__main__' :
    console( )


#----------------------------------------------------------------------#
