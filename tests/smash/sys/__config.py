

"""
unit tests
"""

import pytest
import os
from pathlib import Path

from pprint import pprint, pformat
from smash.sys.out import rprint, listprint, dictprint #ToDo: move these functions outside the package under test


#----------------------------------------------------------------------#

def test__Config( ) :
    from smash.sys.config import Config

    config = Config()

    # assert False

#----------------------------------------------------------------------#

def test__ConfigSectionView( conftree ) :
    from smash.sys.config import Config
    from smash.sys.config import getdeepitem
    from collections import OrderedDict
    config = Config( tree=conftree )
    config._yaml_data = OrderedDict( )
    config._yaml_data[1] = OrderedDict( )
    config._yaml_data[1][2] = OrderedDict( )
    config._yaml_data[1][2][3] = OrderedDict( )
    config._yaml_data[1][2][3][4] = OrderedDict( )
    config._yaml_data[1][2][3][4][5] = 6
    keys = [1, 2, 3, 4, 5]

    value0 = getdeepitem( config._yaml_data, keys )
    assert value0 == 6

    value1 = config[1][2][3][4][5]
    assert value1 == '6'

    value2 = getdeepitem( config, keys )

    assert value2 == '6'

    # assert False


#----------------------------------------------------------------------#

@pytest.fixture( scope='session' )
def conftree( path_root_config ) :
    from smash import ConfigTree
    return ConfigTree()


####################
def try_Config( config ) :
    import smash.sys.out as out

    print( config )
    pprint( config._yaml_data )
    print('tree-root:', config.tree.root)

    print('\nparents')
    listprint(config.parents)

    print( '\nKRO' )
    listprint(config.key_resolution_order)

    print( '\n${path:ROOT}    ', out.pink(config['path']['ROOT'] ))
    print( '\n${path:ROOT}    ', out.pink(config['path']['ROOT'] ))
    print( '\n${path:ENVS}    ', out.pink(config['path']['ENVS'] ))

    print( '\n~~~DONE~~~' )
    return config


####################
def test__Config_from_root( path_root_config, conftree ):
    from smash.sys.config import Config

    config = Config.from_yaml( path_root_config, tree=conftree )
    conftree.root = config
    config = try_Config( config )
    # assert False


####################
#todo: these can be parametrized

def test__Config_from_net( path_network_config, conftree ) :
    from smash.sys.config import Config

    config = Config.from_yaml( path_network_config, tree=conftree )
    config = try_Config( config )
    # assert False

def test__Config_from_data( path_data_config, conftree ) :
    from smash.sys.config import Config

    config = Config.from_yaml( path_data_config, tree=conftree )
    config = try_Config( config )
    # assert False

def test__Config_from_lib( path_lib_config, conftree ) :
    from smash.sys.config import Config

    config = Config.from_yaml( path_lib_config, tree=conftree )
    config = try_Config( config )
    # assert False

def test__Config_from_app( path_app_config, conftree ) :
    from smash.sys.config import Config

    config = Config.from_yaml( path_app_config, tree=conftree )
    config = try_Config( config )
    # assert False

def test__Config_from_host( path_host_config, conftree ) :
    from smash.sys.config import Config

    config = Config.from_yaml( path_host_config, tree=conftree )
    config = try_Config( config )
    # assert False

def test__Config_from_env( path_env00_config, conftree ) :
    from smash.sys.config import Config

    config = Config.from_yaml( path_env00_config, tree=conftree )
    config = try_Config( config )
    # assert False


####################

def test__Config_env_fields( path_env00_config, conftree ) :
    from smash.sys import out
    config = conftree[path_env00_config]

    print( '\n${path:PATH1}   ', out.pink( config['path']['PATH1'] ))
    print( '\n${path:PATH2}   ', out.pink( config['path']['PATH2'] ))
    print( '\n${path:PYTHON}  ', out.pink( config['path']['PYTHON'] ))
    print( '\n${path:APP}     ', out.pink( config['path']['APP'] ))
    print( '\n${path:APP2}    ', out.pink( config['path']['APP2'] ))
    print( '\n${path:APP2}    ', out.pink( config['path']['APP2'] ))
    print( '\n${path:HOST1}   ', out.pink( config['path']['HOST1'] ))

    print( '' )
    list1 = config['path']['LIST1']
    print( '${path:LIST1}    ')
    print(out.pink( rprint(list1, quiet=True )))

    print( '' )
    list2 = config['path']['LIST2']
    print( '${path:LIST2}    ' )
    print( out.pink( rprint( list2, quiet=True ) ) )
    # print( '\n   ', list2[2]['KEY1'] )

    print( '\nconfig[path][SUBKEYS][KEY2]   ', config['path']['SUBKEYS']['KEY2'] )

    print( '\n${shell:RECVAL}   ', out.pink( config['shell']['RECVAL'] ) )

    # assert False


def test__Config_env_parents( path_env00_config, conftree ) :
    from smash.sys import out
    config = conftree[path_env00_config]
    print( '\nconfig.magic' )
    first_parent = config['__inherit__'][0]

    print(out.yellow('-'*40))
    kro = config.key_resolution_order

    print( out.yellow( '-' * 40 ) )
    listprint(kro)

    # assert False


def test__Config_env_fields2( path_env00_config, conftree ) :
    from smash.sys import out
    config = conftree[path_env00_config]

    print( '\n${shell:REMOTE_URL}   ', out.pink( config['shell']['REMOTE_URL'] ) )
    print( out.yellow( '-' * 40 ) )

    # assert False


#----------------------------------------------------------------------#

####################


def try_ConfigTree_from_path( target_path ) :
    from smash.sys.config import ConfigTree

    print( '' )
    workdir = Path( os.getcwd() )
    print( 'CWD:     ', workdir )
    print( 'PATH:    ', target_path )

    print( '' )
    conftree = ConfigTree.from_path( target_path )
    print( 'conftree', conftree )

    print('nodes')
    pprint(conftree.nodes)
    print('root:            ', end='')
    pprint(conftree.root)
    print('root_filepath:   ', end='')
    pprint(conftree.root_filepath)
    print('env_path:        ', end='')
    pprint(conftree.env_path)
    print('out_file:        ', end='')
    pprint(conftree.out_file)
    print('raw_file:        ', end = '')
    pprint(conftree.raw_file)

    print('\nfind_nodes')
    listprint( conftree.find_nodes( '.*yml' ) )

    print( '\nenvlist' )
    listprint( conftree.envlist )

    print( '\npackagelist' )
    listprint( conftree.packagelist )

    print("\nconftree.by_name")
    dictprint(conftree.by_name)
    #print( '${00#__env__/shell:PYTHONHOME}:', conftree.env['00']['shell']['PYTHONHOME'] )

    print( "\nconftree.by_env" )
    dictprint( conftree.by_env )

    print( "\nconftree.by_pkg" )
    dictprint( conftree.by_pkg )

    print( '\nconftree.current_env' )
    print( conftree.current_env )
    print( '\nKRO         ' )
    listprint( list( conftree.current_env.key_resolution_order ) )

    print( '\n[path]      ', conftree.current_env['path'])
    print( '\n[path][ENVS]', conftree.current_env['path']['ENVS'] )

    print('\nsections     ', conftree.current_env.sections)

    # print('\nsubenv')
    # subenv = conftree.subenv(pure=True)
    # print('~~~')
    # dictprint( subenv )

    print('\n~~~DONE~~~')
    return conftree

###################
def test__ConfigTree_from_root( path_testdata ) :
    conftree = try_ConfigTree_from_path( path_testdata )
    # assert False


def test__ConfigTree_from_env( path_env00 ) :
    conftree = try_ConfigTree_from_path( path_env00 )
    # assert False

def test__ConfigTree_from_tasks( path_tasks ) :
    conftree = try_ConfigTree_from_path( path_tasks )
    # assert False

#----------------------------------------------------------------------#
