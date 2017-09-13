#-- smash.env.__main__

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

from ..core.env import ContextEnvironment

#----------------------------------------------------------------------#

_argnames = list( )
_parser = argparse.ArgumentParser(
    description="Smart Shell"
)

def _add_argument( name, options=(), **kwargs ) :
    _parser.add_argument( *options, dest=name, **kwargs )
    _argnames.append( name )

#################### main
_add_argument( 'mode',
               type=str,
               help='execution mode',
               )

_add_argument( 'target',
               type=str,
               nargs=argparse.REMAINDER,
               help='what is to be executed',
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

class Main:

    @staticmethod
    def do_test( *target, context: ContextEnvironment, verbose=False ) :
        log.info( "Run tests for a target package" )

    @staticmethod
    def do_build( *target, context: ContextEnvironment, verbose=False ) :
        log.info( "Build executable distribution archive" )


    @staticmethod
    def __default__( *target, context: ContextEnvironment, verbose=False ) :
        log.info( "Unknown Command", )


#----------------------------------------------------------------------#


def main( args: Arguments ) :
    # ToDo: initialize logging: stdout/stderr redirect
    # ToDo: handle dev mode
    # ToDo: manage env list
    # ToDo: manage package list

    log.print( '~~~~~~~~~~~~~~~~~~~~ SMASH-BOOT')
    log.print( 'SCRIPT:  ', __file__ )
    log.print( 'MODE:    ', args.mode )
    log.print( 'TARGET:  ', args.target )

    cwd = Path( os.getcwd() )
    log.print( 'IWD:     ', cwd )
    log.print( '' )

    if args.verbose:
        from ..core.plugins import report_plugins
        report_plugins()

    with ContextEnvironment(cwd) as context:
        do_func = getattr( Main
                         , 'do_'+args.mode
                         , Main.__default__
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
        return main( parse(args) )

    except Exception as err :
        traceback.print_tb( err.__traceback__ )
        log.print( sys.exc_info( )[0].__name__ + ':', err )
        input( '\nPress ENTER to continue...' )


##############################
if __name__ == '__main__' :
    console( )


#----------------------------------------------------------------------#
