#-- smash.bang.__main__

''' smash.bang
    administration tool
'''

from powertools import AutoLogger
log = AutoLogger()
##############################
from powertools import term
from powertools import click
from powertools.print import pprint

import os
from pathlib import Path
from collections import namedtuple
from contextlib import contextmanager
from contextlib import suppress



from ..core.env import ContextEnvironment
from ..core.env import InstanceEnvironment
from ..core.env import BoxEnvironment
from ..setup.arguments import __version__


#----------------------------------------------------------------------------------------------#
###     SMASH!
##############################

term.init_color()

CONTEXT_SETTINGS = dict(
    help_option_names   = ['-h', '--help'],
    terminal_width      = 97,
    max_content_width   = 97,
    color               = True
)

##############################
@click.group(               'smash!',
    context_settings        = CONTEXT_SETTINGS,
    cls                     = click.Group
)
@click.version_option(
    __version__,
    '--version', '-V',
    prog_name = 'smash.bang'
)
@click.option(
    '--verbose', '-v',
    default = False,
    is_flag = True,
    help    = 'Display additional logging information.'
)
@click.option(
    '--simulation', '-S',
    default = False,
    is_flag = True,
    help    = 'What if the world is just a dream?'
)
@click.contextmanager
def console( verbose, simulation ) :
    ''' boxes grow on trees...
    '''
    if verbose:
        log.setDebug()


    log.print( term.cyan( '\n~~~~~~~~~~~~~~~~~~~~ ' ), term.pink( 'SMASH'),term.cyan('.'), term.pink('BANG' ) )
    log.print( 'SCRIPT:  ', __file__ )
    cwd = Path( os.getcwd() )
    log.print( 'WORKDIR: ', cwd, '\n' )

    ### precreate context environment
    with ContextEnvironment(
            cwd,
            verbose=verbose,
            simulation=simulation
        ) as outer_env:
        result, params = yield outer_env
        log.info('exit: ', result, ' | ', params)

    log.print( '\n', term.pink( '~~~~~~~~~~~~~~~~~~~~' ), term.cyan(' DONE'), '.' )



#----------------------------------------------------------------------------------------------#
###     TREE
##############################

@console.group('tree',
    cls = click.Group
)
@click.pass_obj
@click.contextmanager
def Tree( outer_env ) :
    ''' create and control the boxtree. '''

    log.info('TREE')
    # raise SystemExit
    yield


##############################
@Tree.command( 'new' )
@click.argument( 'instance_name' )
@click.argument( 'template_name', default = 'smash' )
@click.confirmation_option()
@click.pass_obj
def tree_new( outer_env, instance_name:str, template_name:str ) :
    ''' create new instance root in target directory using a registered template
    '''
    from . import tree

    install_root    = outer_env.homepath.resolve() / instance_name

    ### template creates the instance
    instance        = tree.new( install_root )




@Tree.command('get')
@click.pass_obj
def tree_get( outer_env ) :
    ''' get an existing box from a package index
    '''
    log.info("BOX GET ", outer_env )



@Tree.command('list')
@click.pass_obj
def tree_list( outer_env ) :
    ''' list installed boxes
    '''
    log.info("TREE LIST ", outer_env )



@Tree.command('branches')
@click.pass_obj
def tree_branches( outer_env ) :
    ''' list branches
    '''
    log.info("TREE SWITCH", outer_env )



@Tree.command('switch')
@click.pass_obj
def tree_switch( outer_env ) :
    ''' switch branches
    '''
    log.info("TREE SWITCH", outer_env )



@Tree.command('sync')
@click.pass_obj
def tree_sync( outer_env ) :
    ''' synchronize your box with its source
    '''
    log.info("BOX SYNC ", outer_env )



##############################
@Tree.command( name='pack' )
@click.pass_obj
def tree_pack(outer_env) :
    ''' build executable distribution archive
    '''

@Tree.command( name='test' )
@click.pass_obj
def tree_test(outer_env) :
    ''' run deployment tests
    '''


#----------------------------------------------------------------------------------------------#
###     BOX
##############################

@console.group('box',
    cls         = click.Group,
    short_help  = 'manage individual boxes on a boxtree instance.'
)
@click.pass_obj
@click.contextmanager
def Box( outer_env ) :
    ''' manage individual boxes on a boxtree instance.
    '''
    log.info(term.pink('BOX '), outer_env)

    with InstanceEnvironment(parent=outer_env) as instance_env:
        result, params = yield instance_env

    log.info(f'exit {result}, {params}')
    return "BOX"


##############################
@Box.command('new')
@click.pass_obj
def box_new( instance ) :
    ''' create a new box
    '''
    log.info(term.pink("BOX NEW "), instance )
    interior_env    = BoxEnvironment( instance )


    return "BOX NEW"



@Box.command('get')
@click.pass_obj
def box_get( instance ) :
    ''' get a box from a package index
    '''
    log.info("BOX GET " )



@Box.command('list')
@click.pass_obj
def box_list( instance ) :
    ''' list box contents
    '''
    log.info("BOX LIST ")



@Box.command('browse')
@click.pass_obj
def box_browse( instance ) :
    ''' list boxes available on package indices
    '''
    log.info("BOX BROWSE ", instance )



@Box.command('branches')
@click.pass_obj
def box_branches( instance ) :
    ''' list branches
    '''
    log.info("TREE SWITCH", instance )



@Box.command('switch')
@click.pass_obj
def box_switch( instance ) :
    ''' switch branches
    '''
    log.info("TREE SWITCH", instance )



@Box.command('sync')
@click.pass_obj
def box_sync( instance ) :
    ''' synchronize your box with its source
    '''
    log.info("BOX SYNC ", instance )


##############################
@Box.command('test')
@click.pass_obj
def box_test( instance ) :
    ''' run a box's testing suite
    '''
    log.info("BOX TEST ", instance )


#----------------------------------------------------------------------------------------------#
###     SET
##############################

@console.command('set',
    short_help  = 'view or modify a config node on the boxtree.'
)
# @click.confirmation_option()
@click.argument( 'token',       default='env::')        # `configfile::section1:section2:...:key`, key may be None
@click.argument( 'operator',    default=lambda:None )   # `=`, `[`, `]`, None
@click.argument( 'value',       default=lambda:None )   # str, int, None
@click.pass_obj
def Set( outer_env, token, operator, value ) :
    ''' view or modify a config node on the boxtree.

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
    from .set import VALID_OPS, token_set, NothingToDo
    import time

    if operator not in VALID_OPS:
        raise ValueError(f'Invalid smash! set operator. Must be one of {VALID_OPS}')

    with InstanceEnvironment(parent=outer_env) as instance:
        try:
            interior            = BoxEnvironment( instance )
            config              = token_set( token, operator, value, interior.configtree )
        except NothingToDo:
            pass
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


    # args, kwargs = yield
    # log.info(args, ' ', kwargs)


##############################
@console.command()
def undo() :
    ''' undo the previous modification by set.
    '''


#----------------------------------------------------------------------------------------------#



#----------------------------------------------------------------------------------------------#


##############################
@console.group()
def viper() :
    ''' commands for controlling a viper server.
    '''




#----------------------------------------------------------------------------------------------#



#----------------------------------------------------------------------------------------------#

##############################
if __name__ == '__main__' :
    console()


#----------------------------------------------------------------------------------------------#
