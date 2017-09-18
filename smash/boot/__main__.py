#-- smash.__main__

'''
application entry point
'''

from powertools import export
from powertools import AutoLogger
log = AutoLogger()

from pathlib import Path
from collections import namedtuple

import os
import sys
import click

#----------------------------------------------------------------------#

@click.group()
@click.option( '--verbose', '-v', default=False, is_flag=True )
@click.option( '--simulation', '-S', default=False, is_flag=True )
@click.pass_context
def console( ctx , verbose, simulation ) :
    ''' basic utilities for managing smash instances on a host '''
    from ..core.env import ContextEnvironment
    context_env = ContextEnvironment( os.getcwd() )
    ctx.obj     = namedtuple('Arguments', ['context_env', 'verbose', 'simulation'])(
                                            context_env,   verbose,   simulation )


##############################
@console.command()
@click.argument( 'instance_name' )
@click.argument( 'template_name', default = 'smash' )
@click.pass_context
def create( ctx, instance_name:str, template_name:str ) :
    ''' create new instance root in target directory using a registered template '''
    from ..core.plugins import templates
    try:
        parent_args = ctx.obj
        template    = templates[template_name]
    except KeyError as e:
        raise e
    else:
        install_root    = parent_args.context_env.homepath.resolve( ) / instance_name
        instance        = template( install_root, simulation=parent_args.simulation, parent=parent_args.context_env ).instance

        print('created', instance)


##############################
@console.command()
def build() :
    '''build executable distribution archive'''


##############################
@console.command()
def test() :
    '''run deployment tests on an instance or an archive'''


##############################
@console.command()
def push() :
    '''upload archive to deployment registry'''


##############################
@console.command()
def clone() :
    '''pull an instance archive from the deployment registry and extract it to a new directory'''


##############################
if __name__ == '__main__' :
    console()


#----------------------------------------------------------------------#
