

'''
unit tests
'''

import pytest

################################
@pytest.fixture( scope='session' )
def conftree( path_env00 ) :
    from smash import ConfigTree
    return ConfigTree.from_path( path_env00 )


#----------------------------------------------------------------------#
def test__Handler( conftree ) :
    from smash.core.handler import Handler

    # assert False


#----------------------------------------------------------------------#
def test__FileHandler( conftree ) :
    from smash.core.handler import FileHandler

    # assert False


#----------------------------------------------------------------------#
def test__YAMLHandler( conftree ) :
    from smash.core.handler import YAMLHandler

    # assert False


#----------------------------------------------------------------------#
def test__EXEHandler( conftree ) :
    from smash.core.handler import EXEHandler

    # assert False


#----------------------------------------------------------------------#
def test__ScriptHandler( conftree ) :
    from smash.core.handler import ScriptHandler

    # assert False


#----------------------------------------------------------------------#
def test__BashHandler( conftree ) :
    from smash.core.handler import BashHandler

    # assert False


#----------------------------------------------------------------------#
def test__BatchHandler( conftree ) :
    from smash.core.handler import BatchHandler

    # assert False


#----------------------------------------------------------------------#
