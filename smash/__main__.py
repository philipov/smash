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
import click

from pathlib import Path
from collections import namedtuple
from collections import deque

from .core.env import ContextEnvironment
from .core.env import VirtualEnvironment
#
# #----------------------------------------------------------------------#

#----------------------------------------------------------------------#

@click.command()
@click.option('--verbose', '-v', default=False, is_flag=True)
@click.argument('command', nargs=-1)
def console( command, verbose ) :
    """Run target file using associated command inside an environent"""
    # ToDo: initialize logging: stdout/stderr redirect
    # ToDo: handle dev mode
    # ToDo: manage env list
    # ToDo: manage package list

    log.print( '~~~~~~~~~~~~~~~~~~~~ SMASH')
    log.print( 'SCRIPT:  ', __file__ )
    log.print( 'TARGET:  ', command )

    cwd = Path( os.getcwd() )
    log.print( 'IWD:     ', cwd )
    log.print( '' )

    if verbose:
        from .core.plugins import report_plugins
        report_plugins()

    result      = None
    arguments   = deque( command )
    filepath    = Path( arguments.popleft( ) )
    with ContextEnvironment(cwd) as context:
        import re
        from smash.core.plugins import handlers
        from smash.core.handler import NoHandlerMatchedError

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
    # return result

#----------------------------------------------------------------------#

if __name__ == '__main__':
    console()
