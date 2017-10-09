#-- smash.__main__

'''
application entry point
'''

from powertools import export
from powertools import AutoLogger
log = AutoLogger()

from powertools import term

from pathlib import Path
from collections import namedtuple
from functools import partial, partialmethod
from ruamel.yaml.comments import CommentedMap

import os
import sys
import click

Set = set # I really want to override 'set' below...

from ..setup.arguments import __version__

#----------------------------------------------------------------------------------------------#

class UnknownTemplateError( Exception ) :
    ''' template_name argument was not found in the templates dictionary '''


##############################
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(__version__, prog_name='smash.bang')
@click.option( '--verbose', '-v',       default=False, is_flag=True )
@click.option( '--simulation', '-S',    default=False, is_flag=True )
@click.pass_context
def console( ctx , verbose, simulation ) :
    ''' basic utilities for managing smash instances on a host
    '''
    from ..core.env import ContextEnvironment
    term.init_color()

    log.print( term.cyan( '\n~~~~~~~~~~~~~~~~~~~~ ' ), term.pink( 'SMASH'),term.cyan('.'), term.pink('BANG' ) )
    log.print( 'SCRIPT:  ', __file__ )
    cwd = Path( os.getcwd() )
    log.print( 'WORKDIR: ', cwd )

    ### precreate context environment
    context_env = ContextEnvironment( cwd )
    ctx.obj     = namedtuple('Arguments', ['context_env', 'verbose', 'simulation'])(
                                            context_env,   verbose,   simulation )


##############################
@console.command()
@click.argument( 'instance_name' )
@click.argument( 'template_name', default = 'smash' )
@click.pass_context
def boot( ctx, instance_name:str, template_name:str ) :
    ''' create new instance root in target directory using a registered template
    '''
    from ..core.plugins import instance_templates

    try:
        parent_args     = ctx.obj
        template        = instance_templates[template_name]
        install_root    = parent_args.context_env.homepath.resolve() / instance_name

        ### template creates the instance
        instance        = template( install_root,
            simulation  = parent_args.simulation,
            parent      = parent_args.context_env
        ).instance

    except KeyError as e:
        raise UnknownTemplateError(e)

    log.print( '\n', term.pink( '~~~~~~~~~~~~~~~~~~~~' ), term.cyan(' DONE '), '...' )


##############################
@console.command()
@click.argument( 'category', default='categories')
@click.pass_context
def look(ctx, category=None) :
    ''' display information
    '''
    from ..core.env import InstanceEnvironment
    from ..core.env import VirtualEnvironment

    parent_args = ctx.obj
    context_env = parent_args.context_env
    with context_env as context:
        with InstanceEnvironment(parent=context) as instance:
            with VirtualEnvironment( instance ) as interior :
                if category is 'categories':
                    log.info( "\n", term.green('LIST CATEGORIES'))
                else:
                    log.info( "\n", term.green('LIST '), category )


##############################

@console.command()
@click.confirmation_option()
@click.argument( 'token' )                              # `configfile::section1:section2:...:key`, key may be None
@click.argument( 'operator',    default=lambda:None )   # `=`, `[`, `]`, None
@click.argument( 'value',       default=lambda:None )   # str, int, None
@click.pass_context
def set( ctx, token, operator, value ) :
    ''' view or modify a node in the config tree

        the config object selected is either the environment config, or specified in the token using `::`

        \b
        if a value is specified:
            `=` will assign a scalar to a key
            `=` will create a new section, value can be 'list' or 'map'
            `[` and `]` on a key inserts the value next to the key, if section is a list
            `[` or `]` on a section append the value to the section, if section is a list
        if value is ommitted:
            `=` will delete a key
            `[` and `]` on a key move it up or down in its container
            `[` or `]` on a section pop a value, if section is a list
            ommitting the operator will print the token's value and exit without making changes

        if a change is made, a timestamped backup of the old file is stored in the .bak directory
    '''
    from ..core.env import InstanceEnvironment, VirtualEnvironment
    from .set import VALID_OPS, token_set, NothingToDo
    import time

    if operator not in VALID_OPS:
        raise ValueError(f'Invalid smash! set operator. Must be one of {VALID_OPS}')

    parent_args = ctx.obj
    context_env = parent_args.context_env
    with context_env as context:
        with InstanceEnvironment(parent=context) as instance:
            try:
                interior            = VirtualEnvironment( instance )
                config              = token_set( token, operator, value, interior.configtree )
            except NothingToDo:
                log.print( '\n', term.pink( '~~~~~~~~~~~~~~~~~~~~' ) )
            else:
                ### backup
                path:Path           = config.filepath
                timestamp           = time.strftime('%Y%m%d-%H%M%S.', time.localtime())
                new_filepath:Path   = config.path / '.bak' / (timestamp+str(config.filename))
                backup_path:Path    = new_filepath.parent
                if not backup_path.exists():
                    backup_path.mkdir()
                path.rename(new_filepath)

                ### write
                config.dump()

                log.print( '\n', term.pink( '~~~~~~~~~~~~~~~~~~~~' ), term.cyan(' DONE '), '...' )


##############################
@console.command()
def undo() :
    ''' undo the previous modification by set
    '''


##############################
@console.command()
def box() :
    ''' control environment inside current instance
    '''


##############################
@console.command()
def clone() :
    ''' pull an instance archive from the deployment registry and extract it to a new directory
    '''


##############################
@console.command()
def spawn() :
    ''' launch a service
    '''


##############################
@console.command()
def pack() :
    ''' build executable distribution archive
    '''


##############################
@console.command()
def test() :
    ''' run deployment tests on an instance or an archive
    '''


##############################
if __name__ == '__main__' :
    console()


#----------------------------------------------------------------------------------------------#
