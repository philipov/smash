

'''
unit tests
'''

import pytest

################################
@pytest.fixture( scope='session' )
def conftree( path_env00 ) :
    from smash import ConfigTree
    return ConfigTree.from_path( path_env00 )


#----------------------------------------------------------------------------------------------#
def test__PackageType(conftree):
    from smash.core.pkg import PackageType, builtin_package_types

    # assert False


#----------------------------------------------------------------------------------------------#
def test__Package(conftree):
    from smash.core.pkg import Package, builtin_packages

    # assert False


#----------------------------------------------------------------------------------------------#
