#-- smash.__main__

'''
application entry point
'''

# from powertools import export
# from powertools import AutoLogger
# log = AutoLogger()

###
# import colorama
# colorama.init( )
# import colored_traceback
# colored_traceback.add_hook( )

# import os
# import sys
# import traceback
# import argparse
#
from pathlib import Path
from collections import namedtuple
#
# from ..core.env import ContextEnvironment
#
import click

#----------------------------------------------------------------------#





#----------------------------------------------------------------------#

@click.group()
@click.option( '--verbose', '-v', default=False, is_flag=True )
@click.pass_context
def console( ctx , verbose ) :
    '''root handler'''



##############################
@console.command()
@click.argument('instance_name')
def create( instance_name:str ) :
    '''Create new system root in target directory'''

    from .strap import install_configsystem

    install_root = Path( '.' ).resolve() / instance_name
    return install_configsystem( install_root, instance_name )

#
# ##############################
# def build( *command, context: ContextEnvironment, verbose=False ) :
#     """Build executable distribution archive"""
#
# ##############################
# def test( *command, context: ContextEnvironment, verbose=False ) :
#     """"Run instance-wide deployment tests"""
#
# ##############################
# def push( *command, context: ContextEnvironment, verbose=False ) :
#     """Send archive to deployment registry"""


##############################
if __name__ == '__main__' :
    console(ctx=dict())


#----------------------------------------------------------------------#
