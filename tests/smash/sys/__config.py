

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

@pytest.fixture( scope='session' )
def configtree( path_root_config ) :
    from smash import ConfigTree

    configs = ConfigTree( )
    return configs


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
def test__Config_from_root( path_root_config, configtree ):
    from smash.sys.config import Config

    config = Config.from_yaml( path_root_config, tree=configtree )
    configtree.root = config

    config = try_Config( config )
    # assert False

def test__Config_from_data( path_data_config, configtree ) :
    from smash.sys.config import Config

    config = Config.from_yaml( path_data_config, tree=configtree )

    config = try_Config( config )
    # assert False

def test__Config_from_host( path_host_config, configtree ) :
    from smash.sys.config import Config

    config = Config.from_yaml( path_host_config, tree=configtree )

    config = try_Config( config )
    # assert False


def test__Config_from_env( path_env00_config, configtree ) :
    from smash.sys.config import Config
    import smash.sys.out as out

    config = Config.from_yaml( path_env00_config, tree=configtree )

    config = try_Config( config )


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

    # assert False


def test__Config_magic( path_env00_config, configtree ) :
    config = configtree[path_env00_config]
    print( '\nconfig.magic' )
    print( config.magic['__inherits__'] )

    # assert False


#----------------------------------------------------------------------#

def test__ConfigSectionView( configtree ) :

    from smash.sys.config import Config
    from smash.sys.config import getdeepitem
    from collections import OrderedDict
    config = Config( tree=configtree )
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

####################


def try_ConfigTree_from_path( target_path ) :
    from smash.sys.config import ConfigTree

    print( '' )
    workdir = Path( os.getcwd() )
    print( 'CWD:     ', workdir )
    print( 'PATH:    ', target_path )

    print( '' )
    configs = ConfigTree.from_path( target_path )
    print( 'configs', configs )

    print('nodes')
    pprint(configs.nodes)
    print('root:            ', end='')
    pprint(configs.root)
    print('root_filepath:   ', end='')
    pprint(configs.root_filepath)
    print('env_path:        ', end='')
    pprint(configs.env_path)
    print('out_file:        ', end='')
    pprint(configs.out_file)
    print('raw_file:        ', end = '')
    pprint(configs.raw_file)

    print('\nfind_nodes')
    listprint( configs.find_nodes( '.*yml' ) )

    print( '\nenvlist' )
    listprint( configs.envlist )

    print( '\npackagelist' )
    listprint( configs.packagelist )

    print("\nconfigs.by_name")
    dictprint(configs.by_name)
    #print( '${00#__env__/shell:PYTHONHOME}:', configs.env['00']['shell']['PYTHONHOME'] )

    print( "\nconfigs.by_env" )
    dictprint( configs.by_env )

    print( "\nconfigs.by_pkg" )
    dictprint( configs.by_pkg )

    print( '\nconfigs.current_env' )
    print( configs.current_env )
    print( '\nKRO         ' )
    listprint( list( configs.current_env.key_resolution_order ) )

    print( '\n[path]      ', configs.current_env['path'])
    print( '\n[path][ENVS]', configs.current_env['path']['ENVS'] )

    print('\nsections     ', configs.current_env.sections)

    # print('\nsubenv')
    # subenv = configs.subenv(pure=True)
    # print('~~~')
    # dictprint( subenv )

    print('\n~~~DONE~~~')
    return configs

###################
def test__ConfigTree_from_root( path_testdata ) :
    configs = try_ConfigTree_from_path( path_testdata )
    # assert False


def test__ConfigTree_from_env( path_env00 ) :
    configs = try_ConfigTree_from_path( path_env00 )
    # assert False


#----------------------------------------------------------------------#
