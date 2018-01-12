

"""
unit tests
"""

import pytest
import os
from pathlib import Path

from pprint import pprint, pformat
from smash.util.out import rprint, listprint, dictprint #ToDo: move these functions outside the package under test
from powertools.print import term as t


# todo: migration scripts for yaml
#----------------------------------------------------------------------------------------------#

####################
root_data = {
    '__yamlisp__': {
        'name':     '__root__',
        'version':  '0.0.0'
    },

    '__exports__': {
        '__shell__': ['Shell', 'env' ]
    },

    #############
    'boxes': {
        'pkg/platform': './platform',
        'env/00':       './env00'
    },

}

####################
plfm_data = {
    '__yamlisp__': {
        'name':     'pkg/platform',
        'version':  '0.0.0'
    },

    '__import__': {
      'root':       ['Import', '__root__']
    },

    #############
    'env@Win32': {
        'PATH': [
            'C:\Windows',
        ]
    },
    'env@Linux': {
        'PATH': [
            '/bin',
        ]
    },
    'env': {
        'PATH': [
            '@{env~Platform:PATH}'
        ]
    },

    #############
    'path': {
        'ROOT':     '.',
    },

    'python': {
        'VERSION':  '36',
    },

}

####################
host_data = {
    '__yamlisp__': {
        'name':     'host/python',
        'version':  '0.0.0'
    },

    '__import__': {
        'root':     ['Import', '__root__'],
    },

    #############
    'data': {
        'ROOT': './data',
    },

}

####################
env_data = {
    '__yamlisp__': {
        'name':     'env/00',
        'version':  '0.0.0'
    },

    '__import__': {
        'root':     '__root__',
        'context':  '__context__',
        'platform': 'pkg/platform',
        'host':     'host/python',
    },

    '@{platform::}': '<<',

    #############
    'env': {
        'PATH:': [
            '.',
            '@{platform::PATH}',
            '@{host::PATH}',
        ],
    },

    'pipfile': {
        'requires': [
            'conda',
        ]

    },

}


#----------------------------------------------------------------------------------------------#

def test__data2tree():
    from smash.core.yamlisp import data2tree

    data = {
        '__yamlisp__': {
            'name':     'root',
            'version':  '0.0.0'
        },
        'testlist': [
            {
                '1A':   'True',
                '1B':   'False'

            },
            {
                '2A':   'False',
                '2B':   'True'
            },
            'value2',
            'value3'
        ]
    }
    tree0 = data2tree(data)
    print('tree\n', tree0)
    print(tree0.get_node(('__yamlisp__',)))

    tree0 = data2tree(env_data)
    print('tree\n', tree0)

    assert False


#----------------------------------------------------------------------------------------------#

def test__YAMLispNode_empty( ) :
    from smash.core.yamlisp import YAMLispNode

    config = YAMLispNode()
    print(config)
    print(config.raw_data)

    # assert False


#----------------------------------------------------------------------------------------------#

@pytest.fixture( scope='session' )
def boxtree( path_root_config ) :
    from smash.core.yamlisp import BoxTree
    return BoxTree()


def test__YAMLispSection( boxtree ) :
    from smash.core.yamlisp import YAMLispNode
    from smash.core.yamlisp import getdeepitem
    from ruamel.yaml.comments import CommentedMap

    config = YAMLispNode( tree=boxtree )
    print('${__yamlisp__:}    ', t.cyan(config['__yamlisp__']))
    print('${__yamlisp__:name}', t.cyan(config['__yamlisp__']['name']))

    config['__yamlisp__']['name'] = 'root'
    print('${__yamlisp__:name}', t.cyan(config['__yamlisp__']['name']))

    # keys = [1, 2, 3, 4, 5]

    # value0 = getdeepitem( config.raw_data, keys )
    # assert value0 == 6
    #
    # value1 = config[1][2][3][4][5]
    # assert value1 == '6'
    #
    # value2 = getdeepitem( config, keys )
    #
    # assert value2 == '6'

    assert False


#----------------------------------------------------------------------------------------------#

#
####################
def try_YAMLispNode( config ) :
    from smash.util import out

    print( config )
    pprint( config.raw_data )
    print('tree-root:', config.tree.root)

    # print('\nparents')
    # listprint(config.parents)

    # print( '\nKRO' )
    # listprint(config.key_resolution_order)

    # print( '\n${path:ROOT}    ', out.pink(config['path']['ROOT'] ))
    # print( '\n${path:ROOT}    ', out.pink(config['path']['ROOT'] ))
    # print( '\n${path:ENVS}    ', out.pink(config['path']['ENVS'] ))

    print( '\n~~~DONE~~~' )
    return config


####################
def test__YAMLispNode_from_file( path_root_config, boxtree ):
    from smash.core.yamlisp import YAMLispNode

    config = YAMLispNode.from_file( path_root_config, tree=boxtree )
    boxtree.root = config
    config = try_YAMLispNode( config )
    # assert False


####################
#todo: these can be parametrized

# def test__YAMLisp_from_net( path_network_config, conftree ) :
#     from smash.core.config import YAMLisp
#
#     config = YAMLisp.from_yaml( path_network_config, tree=conftree )
#     config = try_YAMLisp( config )
#     # assert False
#
# def test__YAMLisp_from_data( path_data_config, conftree ) :
#     from smash.core.config import YAMLisp
#
#     config = YAMLisp.from_yaml( path_data_config, tree=conftree )
#     config = try_YAMLisp( config )
#     # assert False
#
# def test__YAMLisp_from_lib( path_lib_config, conftree ) :
#     from smash.core.config import YAMLisp
#
#     config = YAMLisp.from_yaml( path_lib_config, tree=conftree )
#     config = try_YAMLisp( config )
#     # assert False
#
# def test__YAMLisp_from_app( path_app_config, conftree ) :
#     from smash.core.config import YAMLisp
#
#     config = YAMLisp.from_yaml( path_app_config, tree=conftree )
#     config = try_YAMLisp( config )
#     # assert False
#
# def test__YAMLisp_from_host( path_host_config, conftree ) :
#     from smash.core.config import YAMLisp
#
#     config = YAMLisp.from_yaml( path_host_config, tree=conftree )
#     config = try_YAMLisp( config )
#     # assert False
#
def test__YAMLisp_from_env( path_env00_config, boxtree ) :
    from smash.core.yamlisp import YAMLispNode

    config = YAMLispNode.from_file( path_env00_config, tree=boxtree )
    boxtree.env = config
    config = try_YAMLispNode( config )

    # assert False

# ####################
# def test__YAMLisp_protocol_check( path_bad_protocol, conftree  ) :
#     from smash.core.config import YAMLisp
#
#     with pytest.raises(YAMLisp.ProtocolError):
#         config = YAMLisp.from_yaml( path_bad_protocol, tree=conftree )
#

    # assert False

####################
#
# def test__YAMLisp_env_fields( path_env00_config, conftree ) :
#     from smash.util import out
#     config = conftree[path_env00_config]
#
#     print( '\n${path:PATH1}   ', out.pink( config['path']['PATH1'] ))
#     print( '\n${path:PATH2}   ', out.pink( config['path']['PATH2'] ))
#     print( '\n${shell:PYTHON} ', out.pink( config['shell']['PYTHON'] ))
#     print( '\n${path:APP}     ', out.pink( config['path']['APP'] ))
#     print( '\n${path:APP2}    ', out.pink( config['path']['APP2'] ))
#     print( '\n${path:APP2}    ', out.pink( config['path']['APP2'] ))
#     print( '\n${path:HOST1}   ', out.pink( config['path']['HOST1'] ))
#
#     print( '' )
#     list1 = config['path']['LIST1']
#     print( '${path:LIST1}    ')
#     print(out.pink( rprint(list1, quiet=True )))
#
#     print( '' )
#     list2 = config['extra']['LIST2']
#     print( '${extra:LIST2}    ' )
#     print( out.pink( rprint( list2, quiet=True ) ) )
#     # print( '\n   ', list2[2]['KEY1'] )
#
#     print( '\nconfig[extra][SUBKEYS][KEY2]   ', config['extra']['SUBKEYS']['KEY2'] )
#
#     print( '\n${shell:RECVAL}   ', out.pink( config['shell']['RECVAL'] ) )
#
#     # assert False


# def test__YAMLisp_env_parents( path_env00_config, conftree ) :
#     from smash.util import out
#     config = conftree[path_env00_config]
#     print( '\nconfig.magic' )
#     first_parent = config['__inherit__'][0]
#
#     print(out.yellow('-'*40))
#     kro = config.key_resolution_order
#
#     print( out.yellow( '-' * 40 ) )
#     listprint(kro)
#
#     print( out.yellow( '-' * 40 ) )
#     keys = config.keys( )
#     print('keys')
#     for key in keys:
#         print(out.cyan('KEY:'), key)
#
#     # assert False
#
#
# def test__YAMLisp_env_fields2( path_env00_config, conftree ) :
#     from smash.util import out
#     config = conftree[path_env00_config]
#
#     print( '\n${shell:REMOTE_URL}   ', out.pink( config['shell']['REMOTE_URL'] ) )
#     print( out.yellow( '-' * 40 ) )
#
#     # assert False



#----------------------------------------------------------------------------------------------#

####################
#
#
# def try_YAMLispTree_from_path( target_path ) :
#     from smash.core.config import YAMLispTree
#
#     print( '' )
#     workdir = Path( os.getcwd() )
#     print( 'CWD:     ', workdir )
#     print( 'PATH:    ', target_path )
#
#     print( '' )
#     conftree = YAMLispTree.from_path( target_path )
#     print( 'conftree', conftree )
#
#     print('nodes')
#     pprint(conftree.nodes)
#     print('root:            ', end='')
#     pprint(conftree.root)
#     print('root_filepath:   ', end='')
#     pprint(conftree.root_filepath)
#     print('env_path:        ', end='')
#     pprint(conftree.env_path)
#     print('out_file:        ', end='')
#     pprint(conftree.out_file)
#     print('raw_file:        ', end = '')
#     pprint(conftree.raw_file)
#
#     print('\nfind_nodes')
#     listprint( conftree.find_nodes( '.*yml' ) )
#
#     print( '\nenvlist' )
#     listprint( conftree.envlist )
#
#     print( '\npackagelist' )
#     listprint( conftree.packagelist )
#
#     print("\nconftree.by_name")
#     dictprint(conftree.by_name)
#     #print( '${00#__env__/shell:PYTHONHOME}:', conftree.env['00']['shell']['PYTHONHOME'] )
#
#     print( "\nconftree.by_env" )
#     dictprint( conftree.by_env )
#
#     print( "\nconftree.by_pkg" )
#     dictprint( conftree.by_pkg )
#
#     print( '\nconftree.current_env' )
#     print( conftree.env )
#     print( '\nKRO         ' )
#     listprint( list( conftree.env.key_resolution_order ) )
#
#     print( '\n[path]      ', conftree.env['path'] )
#     print( '\n[path][ENVS]', conftree.env['path']['ENVS'] )
#
#     print('\nsections     ', conftree.env.sections )
#
#     print('\ninherits',      conftree.env.__inherit__)
#
#     # print('\nsubenv')
#     # subenv = conftree.subenv(pure=True)
#     # print('~~~')
#     # dictprint( subenv )
#
#     print('\n~~~DONE~~~')
#     return conftree

###################
# def test__YAMLispTree_from_root( path_testdata ) :
#     conftree = try_YAMLispTree_from_path( path_testdata )
#     # assert False
#
#
# def test__YAMLispTree_from_env( path_env00 ) :
#     conftree = try_YAMLispTree_from_path( path_env00 )
#     # assert False
#
# def test__YAMLispTree_from_tasks( path_tasks ) :
#     conftree = try_YAMLispTree_from_path( path_tasks )
#     # assert False


#----------------------------------------------------------------------------------------------#
#
# def try_export( conftree ) :
#     from smash.util import out
#
#     # print( out.pink( '\n>>>>>>>>> PATH/ROOT' ), conftree.env['path']['ROOT'] )
#
#     # print(getdeepitem(configs.current_env._yaml_data, ['__inherit__']))
#
#     # print( out.pink( '\n>>>>>>>>> configs.env' ), conftree.env )
#     #
#     # print( out.pink( '\n>>>>>>>>> config.env.parents:'))
#     # listprint( conftree.env.parents )
#
#     # lib_key = Path( conftree.env['pkg']['LIB'] )
#     # print( out.pink( '\n>>>>>>>>> lib_key' ), lib_key )
#     #
#     # lib_config = conftree[lib_key]
#     # print( out.pink( '\n>>>>>>>>> lib_config' ), lib_config )
#
#     lib_config  = conftree[Path( conftree.env['pkg']['LIB'] )]
#     env_config  = conftree.env
#     root_config = conftree.root
#
#     print( '' )
#     lib_exports = lib_config['__export__']
#     print( out.pink( 'lib_config[__exports__]            ' ), lib_exports )
#
#     # print( out.pink('\n>>>>>>>>> lib_exports.keys'), lib_exports.keys( ) )
#     print( out.pink('\nlib_exports.items()    '), lib_exports.items( ) )
#
#     print( out.yellow( '-' * 40 ) )
#
#     print('')
#     export0 = env_config.__export__
#     print( out.pink('env_config.__exports__      '), export0)
#
#     print( '' )
#     export1 = lib_config.__export__
#     print( out.pink('lib_config.__exports__      '), export1 )
#
#     print( '' )
#     export2 = root_config.__export__
#     print( out.pink('root_config.__exports__     '), export2 )
#
#     print( '' )
#     export3 = env_config.exports
#     print( out.pink( 'env_config.exports      ' ) )
#     rprint(export3)
#
# def test__YAMLisp_env_export( path_env00_config, path_lib_config, conftree ) :
#
#     try_export( conftree )
#
#     # assert False
#
#
# def test__YAMLispTree_env_export( path_env00 ) :
#     from smash.core.config import YAMLispTree
#     conftree = YAMLispTree.from_path( path_env00 )
#
#     try_export( conftree )
#
#     # assert False


#----------------------------------------------------------------------------------------------#
