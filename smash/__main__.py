#-- smash.__main__

'''
application entry point
'''

from powertools import export
from powertools import AutoLogger
log = AutoLogger()
from powertools import term

import os
import click

from pathlib import Path
from collections import namedtuple
from collections import deque


from .core.env import ContextEnvironment
from .core.env import VirtualEnvironment

from .__setup__ import __version__

#----------------------------------------------------------------------------------------------#


#----------------------------------------------------------------------------------------------#
CONTEXT_SETTINGS = dict(help_option_names = ['-h', '--help'])

@click.command(context_settings = CONTEXT_SETTINGS)
@click.version_option(__version__,  prog_name = 'smash.bang')
@click.option('--verbose', '-v',    default = False,  is_flag = True)
@click.option('--file', '-f',       default = None,   is_flag = True)
@click.argument('command',          nargs = -1)
@click.pass_context
def console( ctx, command, file, verbose ) :
    """Run target file using associated command inside an environent"""
    # ToDo: initialize logging: stdout/stderr redirect
    # ToDo: handle dev mode
    # ToDo: manage env list
    # ToDo: manage package list

    term.init_color()

    log.print('\n', term.cyan('~~~~~~~~~~~~~~~~~~~~ '), term.pink('SMASH'))
    log.print('SCRIPT:  ', __file__)
    log.print('TARGET:  ', command)

    cwd = Path( os.getcwd() )
    log.print('IWD:     ', cwd)
    log.print('')


    if verbose:
        from .core.plugin import report_plugins
        report_plugins()

    result      = None
    arguments   = deque( command )
    context     = None
    try:
        filepath    = Path( arguments.popleft() )
    except IndexError as e:
        # todo: interactive mode: contextually launch shell configured for virtual environment, instance, or else the system default
        log.print(term.white(">>> "),"Display status here")
    else:
        ### wild lands of unmanaged state
        with ContextEnvironment(cwd) as context:
            ### the wall that guards the lands of version control
            # with InstanceEnvironment(parent=context) as instance:
                ### virtual environments may use a different python version from instance
            with VirtualEnvironment( cwd ) as interior :
                import re
                from smash.core.plugin import handlers
                from smash.core.handler import NoHandlerMatchedError

                log.info('get handler')
                for pattern, Handler in reversed( handlers.items( ) ):
                    log.info(
                        term.dpink('handler match attempt'),
                        f' {pattern:<16} {str(Handler):<50} {filepath.name}'
                    )
                    if re.match( pattern, str(filepath.name) ) :
                        log.info('matched')
                        result = Handler( filepath, list(arguments), interior ).run( ctx )
                        break
                else :
                    raise NoHandlerMatchedError( filepath, handlers )

                log.info( "\ninterior.children", interior.children )


    log.print( '\n', term.pink( '~~~~~~~~~~~~~~~~~~~~' ), term.cyan(' DONE...') )

    ### precreate context environment
    context_env = context
    ctx.obj = namedtuple( 'Arguments', ['context', 'verbose', ] )(
        context_env, verbose )


#----------------------------------------------------------------------------------------------#

if __name__ == '__main__':
    console()


#----------------------------------------------------------------------------------------------#
