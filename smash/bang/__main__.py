#-- smash.bang.__main__

'''
application entry point
'''

from powertools import AutoLogger
log = AutoLogger()

from powertools import term

from pathlib import Path
from collections import namedtuple

import os
import click

class Group(click.Group):
    ''' group with subcommand order relying on python 3.6 dicts '''
    def list_commands(self, ctx):   return self.commands
# todo: color codes in doc strings need to be parsed by click. how shall I hook into that?

#----------------------------------------------------------------------------------------------#

class UnknownTemplateError( Exception ) :
    ''' template_name argument was not found in the templates dictionary '''

###     SMASH!
##############################
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

from ..setup.arguments import __version__
@click.group(           name = 'smash!',        context_settings=CONTEXT_SETTINGS, cls=Group)
@click.version_option(  __version__,
                        '--version','-V',       prog_name='smash.bang')
@click.option(          '--verbose', '-v',      default=False, is_flag=True, help='Display additional logging information.' )
@click.option(          '--simulation', '-S',   default=False, is_flag=True, help='What if the world is just a dream?' )
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


#----------------------------------------------------------------------------------------------#

###     BOOT
##############################
@console.group(name='tree', cls=Group)
@click.pass_context
def Tree( ctx ) :
    ''' manage instances '''


##############################
@Tree.command( name='new' )
@click.argument( 'instance_name' )
@click.argument( 'template_name', default = 'smash' )
@click.pass_context
def tree_new( ctx, instance_name:str, template_name:str ) :
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
@Tree.command( name='pack' )
def tree_pack() :
    ''' build executable distribution archive
    '''

##############################
@Tree.command( name='spoon' )
def tree_spoon() :
    ''' create the union of the boxes in two instances
    '''

##############################
@Tree.command( name='test' )
def tree_test() :
    ''' run deployment tests on an instance or an archive
    '''

##############################
@Tree.command('branches')
@click.pass_context
def tree_branches( ctx ) :
    ''' list branches
    '''
    log.info("TREE SWITCH", ctx.obj.context_env, ' ', ctx.obj.interior_env )


##############################
@Tree.command('switch')
@click.pass_context
def tree_switch( ctx ) :
    ''' switch branches
    '''
    log.info("TREE SWITCH", ctx.obj.context_env, ' ', ctx.obj.interior_env )


##############################
@Tree.command('sync')
@click.pass_context
def tree_sync( ctx ) :
    ''' synchronize your box with its source
    '''
    log.info("BOX SYNC ", ctx.obj.context_env, ' ', ctx.obj.interior_env )

#----------------------------------------------------------------------------------------------#

###     BOX
##############################

@console.group('box', cls=Group)
@click.pass_context
def Box( ctx ) :
    ''' control environment inside current instance
    '''
    from ..core.env import InstanceEnvironment, BoxEnvironment

    parent_args     = ctx.obj
    context_env     = parent_args.context_env
    instance_env    = InstanceEnvironment(parent=context_env)
    interior_env    = BoxEnvironment( instance_env )

    ctx.obj = namedtuple('BoxArguments', [
        'context_env', 'instance_env', 'interior_env'
    ])(  context_env,   instance_env,   interior_env )


##############################
@Box.command('browse')
@click.pass_context
def box_browse( ctx ) :
    ''' list boxes available on package indices
    '''
    log.info("BOX BROWSE ", ctx.obj.context_env, ' ', ctx.obj.interior_env )


##############################
@Box.command('get')
@click.pass_context
def box_get( ctx ) :
    ''' get a box from a package index
    '''
    log.info("BOX GET ", ctx.obj.context_env, ' ', ctx.obj.interior_env )


##############################
@Box.command('list')
@click.pass_context
def box_list( ctx ) :
    ''' list installed boxes
    '''
    log.info("BOX LIST ", ctx.obj.context_env, ' ', ctx.obj.interior_env )


##############################
@Box.command('new')
@click.pass_context
def box_new( ctx ) :
    ''' create a new box
    '''
    log.info("BOX NEW ", ctx.obj.context_env, ' ', ctx.obj.interior_env )

##############################
@Box.command('test')
@click.pass_context
def box_test( ctx ) :
    ''' run a box's testing suite
    '''
    log.info("BOX TEST ", ctx.obj.context_env, ' ', ctx.obj.interior_env )

##############################
@Box.command('branches')
@click.pass_context
def box_branches( ctx ) :
    ''' list branches
    '''
    log.info("TREE SWITCH", ctx.obj.context_env, ' ', ctx.obj.interior_env )


##############################
@Box.command('switch')
@click.pass_context
def box_switch( ctx ) :
    ''' switch branches
    '''
    log.info("TREE SWITCH", ctx.obj.context_env, ' ', ctx.obj.interior_env )


##############################
@Box.command('sync')
@click.pass_context
def box_sync( ctx ) :
    ''' synchronize your box with its source
    '''
    log.info("BOX SYNC ", ctx.obj.context_env, ' ', ctx.obj.interior_env )



#----------------------------------------------------------------------------------------------#

###     SET
##############################
@console.command(name='set')
# @click.confirmation_option()
@click.argument( 'token' )                              # `configfile::section1:section2:...:key`, key may be None
@click.argument( 'operator',    default=lambda:None )   # `=`, `[`, `]`, None
@click.argument( 'value',       default=lambda:None )   # str, int, None
@click.pass_context
def Set( ctx, token, operator, value ) :
    ''' view or modify a node in the config tree

        token syntax => configfile::section:section:...:key

        If no configfile is specified, the current box's environment is the target.
        Section names end with a colon: Section names for lists are integers.
        If no key is specified, the operation will apply to the section.

        \b
        If a value is specified:
            `=` on a key will assign a str|int|float
            `=` on a section will create a new one. 'list','seq', or 'map','dict'
            `[` and `]` on a key inserts the value next to the key, if section is a list
            `[` or `]` on a section append the value to the section, if section is a list

        Assignments to keys implicitly create missing sections as mappings.
        List sections need to be assigned manually.

        \b
        If value is ommitted:
            `=` will delete a key
            `[` and `]` on a key move it up or down in its container
            `[` or `]` on a section pop a value, if section is a list
            ommitting the operator will print the token's value and exit without making changes

        If a change is made, a timestamped backup of the old file is stored in the .bak directory

    '''
    from ..core.env import InstanceEnvironment, BoxEnvironment
    from .set import VALID_OPS, token_set, NothingToDo
    import time

    if operator not in VALID_OPS:
        raise ValueError(f'Invalid smash! set operator. Must be one of {VALID_OPS}')

    parent_args = ctx.obj
    context_env = parent_args.context_env
    with context_env as context:
        with InstanceEnvironment(parent=context) as instance:
            try:
                interior            = BoxEnvironment( instance )
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

#----------------------------------------------------------------------------------------------#



#----------------------------------------------------------------------------------------------#

###     Tree
##############################
# @console.group('tree')
# @click.pass_context
# def Tree( ctx ) :
#     ''' control environment inside current instance
#     '''
#     from ..core.env import InstanceEnvironment, BoxEnvironment
#
#     parent_args     = ctx.obj
#     context_env     = parent_args.context_env
#     instance_env    = InstanceEnvironment(parent=context_env)
#     interior_env    = BoxEnvironment( instance_env )
#
#     ctx.obj = namedtuple('BoxArguments', [
#         'context_env', 'instance_env', 'interior_env'
#     ])(  context_env,   instance_env,   interior_env )


#----------------------------------------------------------------------------------------------#

##############################
# @console.command('look')
@click.argument( 'category', default='categories')
@click.pass_context
def Look(ctx, category=None) :
    ''' display information
    '''
    from ..core.env import InstanceEnvironment
    from ..core.env import BoxEnvironment

    parent_args = ctx.obj
    context_env = parent_args.context_env
    with context_env as context:
        with InstanceEnvironment(parent=context) as instance:
            interior = BoxEnvironment( instance )
            if category is 'categories':
                log.info( "\n", term.green('LIST CATEGORIES'))
            else:
                log.info( "\n", term.green('LIST '), category )


# ##############################
# @console.command()
# def clone() :
#     ''' pull an instance archive from the deployment registry and extract it to a new directory
#     '''


# ##############################
# @console.command()
# def spawn() :
#     ''' launch a service
#     '''

##############################
@console.group()
def viper() :
    ''' commands for controlling a viper server
    '''




#----------------------------------------------------------------------------------------------#



#----------------------------------------------------------------------------------------------#

##############################
if __name__ == '__main__' :
    console()


#----------------------------------------------------------------------------------------------#
