#-- smash.__main__

'''
application entry point
'''

__all__ = []

###
import logging
logging.basicConfig( level=logging.INFO )
from .utils.out import loggers_for
(debug, info, warning, error, critical) = loggers_for( __name__ )

###
import colorama
colorama.init( )
import colored_traceback
colored_traceback.add_hook( )

import os
import sys
import traceback

from pathlib import Path


#----------------------------------------------------------------------#

from . import cmdline
from . import modes

from .sys.config import ConfigTree
from .utils.out import debuglog
from .sys.env import ContextEnvironment


@debuglog(__name__)
def main( args: cmdline.Arguments ) :
    # ToDo: initialize logging: stdout/stderr redirect
    # ToDo: handle dev mode
    # ToDo: manage env list
    # ToDo: manage package list

    info( '~~~~~~~~~~~~~~~~~~~~ SMASH')
    debug( 'SCRIPT:  ', __file__ )
    debug( 'VERBOSE: ', args.verbose )

    workdir = Path( os.getcwd( ) )
    debug( 'CWD:     ', workdir )
    debug( '' )

    info( 'MODE:    ', args.mode )
    info( 'TARGET:  ', args.target )
    info( '' )

    with ContextEnvironment(workdir) as context:
        do_func = getattr( modes
                         , 'do_'+args.mode
                         , modes.__default__
                         )

        result  = do_func( *args.target
                         , context=context
                         , verbose=args.verbose
                         )

    debug( '' )
    info( 'SMASH DONE...' )
    return result


##############################
def console( args=None ) :
    '''bind main to command-line argmuntes; print exceptions'''

    try :
        if args is None :
            args = sys.argv[1 :]
        return main( cmdline.parse(args) )

    except Exception as err :
        traceback.print_tb( err.__traceback__ )
        print( sys.exc_info( )[0].__name__ + ':', err )
        input( '\nPress ENTER to continue...' )


##############################
if __name__ == '__main__' :
    console( )


#----------------------------------------------------------------------#
