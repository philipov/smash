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

import os
import sys
import click

#----------------------------------------------------------------------#

class UnknownTemplateError( Exception ) :
    '''template_name argument was not found in the templates dictionary'''


##############################
@click.group()
@click.option( '--verbose', '-v',       default=False, is_flag=True )
@click.option( '--simulation', '-S',    default=False, is_flag=True )
@click.pass_context
def console( ctx , verbose, simulation ) :
    ''' basic utilities for managing smash instances on a host
    '''
    term.init_color()

    log.print( term.cyan( '\n~~~~~~~~~~~~~~~~~~~~ ' ), term.pink( 'SMASH'),term.cyan('.'), term.pink('BANG' ) )
    log.print( 'SCRIPT:  ', __file__ )
    cwd = Path( os.getcwd() )
    log.print( 'WORKDIR: ', cwd )

    ### precreate context environment
    from ..core.env import ContextEnvironment
    context_env = ContextEnvironment( cwd )
    ctx.obj     = namedtuple('Arguments', ['context_env', 'verbose', 'simulation'])(
                                            context_env,   verbose,   simulation )


##############################
@console.command()
@click.argument( 'instance_name' )
@click.argument( 'template_name', default = 'smash' )
@click.pass_context
def init( ctx, instance_name:str, template_name:str ) :
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
Set = set
@console.command()
@click.argument( 'token' )
@click.argument( 'value' )
@click.pass_context
def set( ctx, token, value ) :
    ''' new environment inside current instance
    '''
    from ..core.env import InstanceEnvironment
    from ..core.env import VirtualEnvironment

    parent_args = ctx.obj
    context_env = parent_args.context_env
    with context_env as context:
        with InstanceEnvironment(parent=context) as instance:
            with VirtualEnvironment( instance ) as interior :
                configpath = None
                sections = None
                key = None
                ## configfile::
                try:
                    (configpath, rest) = token.split('::')[0]
                except ValueError as e:
                    (configpath, rest) = interior.config.filepath, token
                #
                # ### section:section:key

                keys = rest.split(':')

                if len(keys) > 1:
                    try:
                        sections    = keys[:-1]
                        key         = keys[-1:]
                    except IndexError as e:
                        raise e
                elif len(keys) == 1:
                    sections    = list()
                    key         = keys[0]
                else:
                    raise IndexError(token)

                log.print( "\n", term.green('SET '), configpath, '::', sections, ':', key, term.green(' = '), value, '   ', keys )



##############################
@console.command()
def box() :
    ''' new environment inside current instance '''


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
def spawn() :
    ''' launch a service '''

##############################
@console.command()
def clone() :
    ''' pull an instance archive from the deployment registry and extract it to a new directory '''


##############################
@console.command()
def pack() :
    ''' build executable distribution archive '''


##############################
@console.command()
def test() :
    ''' run deployment tests on an instance or an archive '''


##############################
if __name__ == '__main__' :
    console()


#----------------------------------------------------------------------#
