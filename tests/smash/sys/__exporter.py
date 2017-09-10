

'''
unit tests
'''
import pytest

#----------------------------------------------------------------------#

@pytest.fixture( scope='session' )
def conftree( path_env00 ) :
    from smash import ConfigTree
    return ConfigTree.from_path(path_env00)

def test__Exporter(conftree):
    '''abstract base class'''
    from smash.sys.exporter import Exporter
    # assert False


#----------------------------------------------------------------------#
def test__ExportShell(conftree):
    from smash.sys.exporter import ExportShell
    # assert False


#----------------------------------------------------------------------#
def test__ExportShellScript(conftree):
    from smash.sys.exporter import ExportShellScript
    # assert False

def test__ExportShellScriptCMD(conftree):
    from smash.sys.exporter import ExportShellScriptCMD
    # assert False

def test__ExportShellScriptBASH(conftree):
    from smash.sys.exporter import ExportShellScriptBASH
    # assert False


#----------------------------------------------------------------------#

def test__ExportDebug(conftree):
    from smash.sys.exporter import ExportDebug
    # assert False


#----------------------------------------------------------------------#
def test__ExportYAML(conftree):
    from smash.sys.exporter import ExportYAML
    # assert False


#----------------------------------------------------------------------#
def test__ExportXML(conftree):
    from smash.sys.exporter import ExportXML
    # assert False


#----------------------------------------------------------------------#
def test__ExportINI(conftree):
    from smash.sys.exporter import ExportINI
    # assert False


#----------------------------------------------------------------------#
