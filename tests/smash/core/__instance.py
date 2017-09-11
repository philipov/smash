

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
def test__InstanceTemplate( conftree ) :
    from smash.core.instance import InstanceTemplate
    # assert False


#----------------------------------------------------------------------#
def test__SmashTemplate( conftree ) :
    from smash.core.instance import SmashTemplate
    # assert False


#----------------------------------------------------------------------#
