

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
def test__MashHandler( conftree ) :
    from smash.core.handler import MashHandler

    # assert False


#----------------------------------------------------------------------#
def test__CommandHandler( conftree ) :
    from smash.core.handler import CommandHandler

    # assert False


################################
def test__Daemonizer( conftree ) :
    from smash.core.handler import CommandHandler

    # assert False

#----------------------------------------------------------------------#
def test__ScriptHandler( conftree ) :
    from smash.core.handler import ScriptHandler

    # assert False


################################
def test__BashHandler( conftree ) :
    from smash.core.handler import BashHandler

    # assert False


################################
def test__BatchHandler( conftree ) :
    from smash.core.handler import BatchHandler

    # assert False


################################
def test__PythonHandler( conftree ) :
    from smash.core.handler import PythonHandler

    # assert False


#----------------------------------------------------------------------#
