#-- smash.__main__

'''
application entry point
'''

###
import os
import sys
import traceback

from pathlib import Path

import colorama
colorama.init()
import colored_traceback
colored_traceback.add_hook()
###
import logging
log = logging.getLogger( name=__name__ )
logging.basicConfig( level=logging.DEBUG )
# debug   = lambda *a, **b : log.debug( ''.join( str(arg) for arg in a ))
# info    = lambda *a, **b : log.info(  ''.join( str(arg) for arg in a ))
debug = print
info  = print
# debug = lambda *a, **b : None

###
__all__ = []

#----------------------------------------------------------------------#

from . import cmdline
from . import modes

from .sys.config import ConfigTree


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

    configs = ConfigTree.from_path(workdir)
    debug('CONFIGS:  ', configs)
    debug( '' )

    info( 'MODE:    ', args.mode )
    info( 'TARGET:  ', args.target )
    info( '' )

    do_func = getattr( modes
                     , 'do_'+args.mode
                     , modes.__default__
                     )

    result  = do_func( *args.target
                     , workdir=workdir
                     , configs=configs
                     , verbose=args.verbose
                     )

    debug( '' )
    info( 'SMASH DONE...' )
    return result


##############################
def run( args=None ) :
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
    run()


#----------------------------------------------------------------------#
