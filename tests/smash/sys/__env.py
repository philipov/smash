

'''
unit tests
'''

#----------------------------------------------------------------------#

def test__context(path_env00 ):
    from smash.sys.env import ContextEnvironment

    # assert False


################################
def test__subenv( path_env00 ) :
    from smash.sys.env import ContextEnvironment
    from smash.sys.env import VirtualEnvironment

    # assert False


################################
def test__conda( path_env00 ) :
    from smash.sys.env import ContextEnvironment
    from smash.sys.env import CondaEnvironment

    # assert False


################################
def test__docker( path_env00 ) :
    from smash.sys.env import ContextEnvironment
    from smash.sys.env import DockerEnvironment

    # assert False


################################
def test__remote( path_env00 ) :
    from smash.sys.env import ContextEnvironment
    from smash.sys.env import RemoteEnvironment

    # assert False


#----------------------------------------------------------------------#
