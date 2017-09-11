#-- smash.__main__

'''
application entry point
'''

__all__ = []

###
import powertools
log = powertools.AutoLogger()

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

from .util.out import debuglog
from .core.env import ContextEnvironment


@debuglog(__name__)
def main( args: cmdline.Arguments ) :
    # ToDo: initialize logging: stdout/stderr redirect
    # ToDo: handle dev mode
    # ToDo: manage env list
    # ToDo: manage package list

    log.print( '~~~~~~~~~~~~~~~~~~~~ SMASH')
    log.print( 'SCRIPT:  ', __file__ )
    log.print( 'MODE:    ', args.mode )
    log.print( 'TARGET:  ', args.target )

    cwd = Path( os.getcwd() )
    log.print( 'IWD:     ', cwd )
    log.print( '' )

    if args.verbose:
        from .core.plugins import report_plugins
        report_plugins()

    with ContextEnvironment(cwd) as context:
        do_func = getattr( modes
                         , 'do_'+args.mode
                         , modes.__default__
                         )

        result  = do_func( *args.target
                         , context=context
                         , verbose=args.verbose
                         )

    log.print( '' )
    log.print( 'SMASH DONE...' )
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
