

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
platform_data = {
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

@pytest.fixture( scope='session' )
def configs( path_root_config ) :
    from smash.core.yamlisp import BoxTree
    return BoxTree()


def test__YAMLispNode_empty( ) :
    from smash.core.yamlisp import YAMLispNode

    config = YAMLispNode()
    print(config)
    print(config.raw_data)

    # assert False


#----------------------------------------------------------------------------------------------#

def test__data2tree(path_testdata, configs):
    from smash.core.yamlisp import data2tree
    from smash.core.yamlisp import tree2data
    from smash.core.yamlisp import YAMLispNode
    from smash.util import yaml

    config = YAMLispNode()


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
            'value1',
            {
                '2A':   'False',
                '2B':   'True'
            },
            'value2',
            'value3'
        ]
    }

    tree0 = data2tree(data, config=config )
    print('tree\n', tree0)
    print(tree0.get_node(('__yamlisp__',)))

    data0 = tree2data(tree0)
    rprint(data)
    print('DATA:')
    rprint(data0)
    yaml.dump(path_testdata/'data2tree2data.yaml', data0)

    tree1 = data2tree(env_data, config=config)
    print('tree\n', tree1)

    # assert False



#----------------------------------------------------------------------------------------------#



def test__YAMLispSection( configs ) :
    from smash.core.yamlisp import YAMLispNode
    from smash.core.yamlisp import getdeepitem
    from ruamel.yaml.comments import CommentedMap

    # config = YAMLispNode( collection=configs )
    # print('${__yamlisp__:}    ', t.cyan(config['__yamlisp__']))
    # print('${__yamlisp__:name}', t.cyan(config['__yamlisp__']['name']))
    #
    # config['__yamlisp__']['name'] = 'root'
    # print('${__yamlisp__:name}', t.cyan(config['__yamlisp__']['name']))

    # assert False


#----------------------------------------------------------------------------------------------#

#
####################
def try_YAMLispNode( config ) :
    from smash.util import out

    print( config )
    pprint( config.raw_data )
    print('configs-root:', config.collection.root)
    print('tree\n', config.parse_tree)

    print( '\n~~~DONE~~~' )
    return config


####################
def test__YAMLispNode_from_file( path_root_config, configs ):
    from smash.core.yamlisp import YAMLispNode

    config = YAMLispNode.from_file( path_root_config, collection=configs )
    configs.root = config
    config = try_YAMLispNode( config )
    # assert False


def test__YAMLisp_from_env( path_env00_config, configs ) :
    from smash.core.yamlisp import YAMLispNode

    config = YAMLispNode.from_file( path_env00_config, collection=configs )
    configs.env = config
    config = try_YAMLispNode( config )

    # assert False


#----------------------------------------------------------------------------------------------#


def test__YAMLispValue_from_node( configs ):
    from smash.core.yamlisp import YAMLispNode
    from smash.core.yamlisp import YAMLispValue

    data = {
        '__yamlisp__': {
            'name':     'test',
            'version':  '0.0.0'
        },
        'path': {
            'HERE': './',
            'DATA': '${HERE}/data'
        },
        'vars': {
            'A': 'a',
            'B': 'b',
            'C': '00${A}c${B}00',
            'D': '${A}${C}${B}',
            'E': 'A',
            'F': '}${${E}}{${A}}',
        }
    }
    config = YAMLispNode( collection=configs, data=data, filepath=Path('.').resolve() )

    print(config.parse_tree)

    section0 = config['path']
    print("SECTION0", section0)

    value0 = config['path']['HERE']
    print("VALUE0", value0)

    value1 = config['path']['DATA']
    print("VALUE1", value1)


    assert False


#----------------------------------------------------------------------------------------------#
