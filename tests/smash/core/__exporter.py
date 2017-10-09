

'''
unit tests
'''
import pytest

#----------------------------------------------------------------------------------------------#

@pytest.fixture( scope='session' )
def conftree( path_env00 ) :
    from smash import ConfigTree
    return ConfigTree.from_path(path_env00)

def test__Exporter(conftree):
    '''abstract base class'''
    from smash.core.exporter import Exporter
    # assert False


#----------------------------------------------------------------------------------------------#
def test__ExportShell(conftree):
    from smash.core.exporter import ExportShell
    # assert False


#----------------------------------------------------------------------------------------------#
def test__ExportShellScript(conftree):
    from smash.core.exporter import ExportShellScript
    # assert False

def test__ExportShellScriptCMD(conftree):
    from smash.core.exporter import ExportShellScriptCMD
    # assert False

def test__ExportShellScriptBASH(conftree):
    from smash.core.exporter import ExportShellScriptBASH
    # assert False


#----------------------------------------------------------------------------------------------#

def test__ExportDebug(conftree):
    from smash.core.exporter import ExportDebug
    # assert False


#----------------------------------------------------------------------------------------------#
def test__ExportYAML(conftree):
    from smash.core.exporter import ExportYAML
    # assert False


#----------------------------------------------------------------------------------------------#
def test__ExportXML(conftree):
    from smash.core.exporter import ExportXML
    # assert False


#----------------------------------------------------------------------------------------------#
def test__ExportINI(conftree):
    from smash.core.exporter import ExportINI
    # assert False


#----------------------------------------------------------------------------------------------#
