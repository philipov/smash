

"""
unit tests
"""

import pytest
import os
from pathlib import Path

from pprint import pprint, pformat
from smash.util.out import rprint, listprint, dictprint #ToDo: move these functions outside the package under test


#----------------------------------------------------------------------#

def test__Config( ) :
    from smash.core.config import Config

    config = Config()

    # assert False

#----------------------------------------------------------------------#

def test__ConfigSectionView( conftree ) :
    from smash.core.config import Config
    from smash.core.config import getdeepitem
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
    from smash.util import out

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
    from smash.core.config import Config

    config = Config.from_yaml( path_root_config, tree=conftree )
    conftree.root = config
    config = try_Config( config )
    # assert False


####################
#todo: these can be parametrized

def test__Config_from_net( path_network_config, conftree ) :
    from smash.core.config import Config

    config = Config.from_yaml( path_network_config, tree=conftree )
    config = try_Config( config )
    # assert False

def test__Config_from_data( path_data_config, conftree ) :
    from smash.core.config import Config

    config = Config.from_yaml( path_data_config, tree=conftree )
    config = try_Config( config )
    # assert False

def test__Config_from_lib( path_lib_config, conftree ) :
    from smash.core.config import Config

    config = Config.from_yaml( path_lib_config, tree=conftree )
    config = try_Config( config )
    # assert False

def test__Config_from_app( path_app_config, conftree ) :
    from smash.core.config import Config

    config = Config.from_yaml( path_app_config, tree=conftree )
    config = try_Config( config )
    # assert False

def test__Config_from_host( path_host_config, conftree ) :
    from smash.core.config import Config

    config = Config.from_yaml( path_host_config, tree=conftree )
    config = try_Config( config )
    # assert False

def test__Config_from_env( path_env00_config, conftree ) :
    from smash.core.config import Config

    config = Config.from_yaml( path_env00_config, tree=conftree )
    conftree.env_path =config.path
    config = try_Config( config )
    # assert False

####################
def test__Config_protocol_check( path_bad_protocol, conftree  ) :
    from smash.core.config import Config

    with pytest.raises(Config.ProtocolError):
        config = Config.from_yaml( path_bad_protocol, tree=conftree )


    # assert False

####################

def test__Config_env_fields( path_env00_config, conftree ) :
    from smash.util import out
    config = conftree[path_env00_config]

    print( '\n${path:PATH1}   ', out.pink( config['path']['PATH1'] ))
    print( '\n${path:PATH2}   ', out.pink( config['path']['PATH2'] ))
    print( '\n${shell:PYTHON} ', out.pink( config['shell']['PYTHON'] ))
    print( '\n${path:APP}     ', out.pink( config['path']['APP'] ))
    print( '\n${path:APP2}    ', out.pink( config['path']['APP2'] ))
    print( '\n${path:APP2}    ', out.pink( config['path']['APP2'] ))
    print( '\n${path:HOST1}   ', out.pink( config['path']['HOST1'] ))

    print( '' )
    list1 = config['path']['LIST1']
    print( '${path:LIST1}    ')
    print(out.pink( rprint(list1, quiet=True )))

    print( '' )
    list2 = config['extra']['LIST2']
    print( '${extra:LIST2}    ' )
    print( out.pink( rprint( list2, quiet=True ) ) )
    # print( '\n   ', list2[2]['KEY1'] )

    print( '\nconfig[extra][SUBKEYS][KEY2]   ', config['extra']['SUBKEYS']['KEY2'] )

    print( '\n${shell:RECVAL}   ', out.pink( config['shell']['RECVAL'] ) )

    # assert False


def test__Config_env_parents( path_env00_config, conftree ) :
    from smash.util import out
    config = conftree[path_env00_config]
    print( '\nconfig.magic' )
    first_parent = config['__inherit__'][0]

    print(out.yellow('-'*40))
    kro = config.key_resolution_order

    print( out.yellow( '-' * 40 ) )
    listprint(kro)

    print( out.yellow( '-' * 40 ) )
    keys = config.keys( )
    print('keys')
    for key in keys:
        print(out.cyan('KEY:'), key)

    # assert False


def test__Config_env_fields2( path_env00_config, conftree ) :
    from smash.util import out
    config = conftree[path_env00_config]

    print( '\n${shell:REMOTE_URL}   ', out.pink( config['shell']['REMOTE_URL'] ) )
    print( out.yellow( '-' * 40 ) )

    # assert False



#----------------------------------------------------------------------#

####################


def try_ConfigTree_from_path( target_path ) :
    from smash.core.config import ConfigTree

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
    print( conftree.env )
    print( '\nKRO         ' )
    listprint( list( conftree.env.key_resolution_order ) )

    print( '\n[path]      ', conftree.env['path'] )
    print( '\n[path][ENVS]', conftree.env['path']['ENVS'] )

    print('\nsections     ', conftree.env.sections )

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

def try_export( conftree ) :
    from smash.util import out

    # print( out.pink( '\n>>>>>>>>> PATH/ROOT' ), conftree.env['path']['ROOT'] )

    # print(getdeepitem(configs.current_env._yaml_data, ['__inherit__']))

    # print( out.pink( '\n>>>>>>>>> configs.env' ), conftree.env )
    #
    # print( out.pink( '\n>>>>>>>>> config.env.parents:'))
    # listprint( conftree.env.parents )

    # lib_key = Path( conftree.env['pkg']['LIB'] )
    # print( out.pink( '\n>>>>>>>>> lib_key' ), lib_key )
    #
    # lib_config = conftree[lib_key]
    # print( out.pink( '\n>>>>>>>>> lib_config' ), lib_config )

    lib_config  = conftree[Path( conftree.env['pkg']['LIB'] )]
    env_config  = conftree.env
    root_config = conftree.root

    print( '' )
    lib_exports = lib_config['__export__']
    print( out.pink( 'lib_config[__exports__]            ' ), lib_exports )

    # print( out.pink('\n>>>>>>>>> lib_exports.keys'), lib_exports.keys( ) )
    print( out.pink('\nlib_exports.items()    '), lib_exports.items( ) )

    print( out.yellow( '-' * 40 ) )

    print('')
    export0 = env_config.__export__
    print( out.pink('env_config.__exports__      '), export0)

    print( '' )
    export1 = lib_config.__export__
    print( out.pink('lib_config.__exports__      '), export1 )

    print( '' )
    export2 = root_config.__export__
    print( out.pink('root_config.__exports__     '), export2 )

    print( '' )
    export3 = env_config.exports
    print( out.pink( 'env_config.exports      ' ) )
    rprint(export3)

def test__Config_env_export( path_env00_config, path_lib_config, conftree ) :

    try_export( conftree )

    # assert False


def test__ConfigTree_env_export( path_env00 ) :
    from smash.core.config import ConfigTree
    conftree = ConfigTree.from_path( path_env00 )

    try_export( conftree )

    # assert False


#----------------------------------------------------------------------#
