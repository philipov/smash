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
OP_SET              = '='
OP_LIST_LEFT        = '['
OP_LIST_RIGHT       = ']'
TOKEN_SEP_FILE      = '::'
TOKEN_SEP_SECTION   = ':'
VALID_OPS           = (
    None,
    OP_SET,
    OP_LIST_LEFT,
    OP_LIST_RIGHT
)
@console.command()
@click.argument( 'token' )
@click.argument( 'operator',    default=lambda:None )
@click.argument( 'value',       default=lambda:None )
@click.pass_context
def set( ctx, token, operator, value ) :
    ''' view or modify a value in a yamilsp config file
        stores a timestamped backup of the old file in the .bak directory
    '''
    from ..core.env import InstanceEnvironment
    from ..core.env import VirtualEnvironment
    from ..core.config import Config
    from ..core.config import getdeepitem
    import time

    if operator not in VALID_OPS:
        raise ValueError(f'Invalid smash! set operator. Must be one of {VALID_OPS}')

    parent_args = ctx.obj
    context_env = parent_args.context_env
    with context_env as context:
        with InstanceEnvironment(parent=context) as instance:
            interior = VirtualEnvironment( instance )

            ## configfile::
            try:
                (configpath, rest) = token.split(TOKEN_SEP_FILE)[0]
            except ValueError as e:
                (configpath, rest) = interior.config.filepath, token
            config:Config = interior.configtree[configpath]

            # ### section:section:key
            keys = rest.split(TOKEN_SEP_SECTION)
            if len(keys) > 1:
                try:
                    sections    = keys[:-1]
                    key         = keys[-1]
                except IndexError as e:
                    raise e
            elif len(keys) == 1:
                sections    = list()
                key         = keys[0]
            else:
                raise IndexError(token)

            ### display value
            try:
                view = getdeepitem(config._yaml_data, sections)
                if key is '':
                    key             = None
                    current_value   = view
                elif isinstance(view, list):
                    key = int(key)
                    if key < 0:
                        key = len(view) + key
                    current_value = view[key]
                else:
                    current_value = view[key]
            except KeyError as e:
                raise e
            log.print( "\n", term.green('SHOW: '), configpath, TOKEN_SEP_FILE, sections, TOKEN_SEP_SECTION, key, term.green(f' {OP_SET} '), current_value )

            ### early exit
            if operator is value is None:
                return

            ### apply operator
            new_value = NotImplemented

            try:
                value = int(value)
            except TypeError as e:
                pass
            except ValueError as e:
                pass

            ###     SET SCALAR VALUE
            if operator == OP_SET:
                ### delete item
                if value is None:
                    del view[key]
                    new_value = None

                ### assign item
                else:
                    view[key]:str = value
                    new_value = view[key]

            ###     LIST OPERATIONS
            elif operator in (OP_LIST_LEFT, OP_LIST_RIGHT):

                if value is None \
                and isinstance(view, (list, CommentedMap)): ### null-op on sequence

                    ### pop the left or right of list
                    if key is None:
                        {   OP_LIST_LEFT:   partial(view.pop,  0),
                            OP_LIST_RIGHT:  view.pop,
                        }[operator]()
                        new_value = None

                    ### move key up or down in order
                    else:
                        if isinstance(view, CommentedMap):
                            def convert(k):
                                i = list( view.items() ).index( (k, view[k]) )
                                if i < 0:
                                    i = len(view) - i
                                return i
                        else:
                            convert = int

                        if operator == OP_LIST_LEFT:
                            if convert(key) == 0:
                                new = len(view)
                            else:
                                new = convert(key)-1
                        elif operator == OP_LIST_RIGHT:
                            if convert(key) == len(view)-1:
                                new = 0
                            else:
                                new = convert(key)+1
                        else:
                            raise RuntimeError('move left or right')

                        if isinstance(view,CommentedMap):
                            log.info(f'new:{new} key:{key} = {current_value}')
                            del view[key]
                            view.insert(new, key, current_value)
                            new_value = view[key]
                        else:
                            view.pop(key)
                            view.insert(new, current_value)
                            new_value = view[new-1]

                # todo: finish operator consistency, then document
                ### append to left or right of list
                elif isinstance(current_value, list):
                    {   OP_LIST_LEFT:   partial(current_value.insert, 0),
                        OP_LIST_RIGHT:  current_value.append,
                    }[operator](value)
                    new_value = view[key]

                ### insert value next to key
                elif isinstance(current_value, str) \
                and isinstance(view, list):
                    {   OP_LIST_LEFT:   partial(view.insert, key),
                        OP_LIST_RIGHT:  partial(view.insert, key+1),
                    }[operator](value)
                else:
                    raise TypeError(f'invalid type ({type(view)}, {type(current_value)}) for list setters')

            log.print(
                "\n", term.green('SET:  '),
                configpath, TOKEN_SEP_FILE,
                sections, TOKEN_SEP_SECTION,
                key, term.green(f' {OP_SET} '), new_value
            )
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



##############################
@console.command()
def undo() :
    ''' undo the previous modification by set '''


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
