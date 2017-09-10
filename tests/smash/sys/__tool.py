

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
def test__Tool( conftree ) :
    from smash.sys.tool import Tool
    # assert False


#----------------------------------------------------------------------#
def test__Task( conftree ) :
    from smash.sys.tool import Task
    # assert False


#----------------------------------------------------------------------#
def test__Loader( conftree ) :
    from smash.sys.tool import Loader
    # assert False


#----------------------------------------------------------------------#
def test__Validator( conftree ) :
    from smash.sys.tool import Validator
    # assert False


#----------------------------------------------------------------------#
def test__Daemon( conftree ) :
    from smash.sys.tool import Daemon
    # assert False


#----------------------------------------------------------------------#
def test__Monitor( conftree ) :
    from smash.sys.tool import Monitor
    # assert False


#----------------------------------------------------------------------#
def test__Service( conftree ) :
    from smash.sys.tool import Service
    # assert False


#----------------------------------------------------------------------#
