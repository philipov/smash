#-- smash.boot.archive

"""
"""

from powertools import export
from powertools import AutoLogger
log = AutoLogger( )
from powertools import term

from pathlib import Path
from shutil import copyfile
from contextlib import suppress

from ..core.env import VirtualEnvironment
from ..util.path import copyfile2, temporary_working_directory
from .. import templates


#----------------------------------------------------------------------------------------------#


def new( parent:VirtualEnvironment, boxpath:Path, cookiecutter=None ):
    ''' create a new box
    '''
    from dulwich import porcelain

    ### create default paths/files
    boxes_root      = Path(parent.configtree.env[templates.PATH_VARS_SECTION][templates.PATH_BOXES])

    newbox_root     = boxes_root / boxpath
    newbox_master   = newbox_root / 'master'
    with suppress( FileExistsError ) :
        parent.mkdir(newbox_root)
    with suppress( FileExistsError ) :
        parent.mkdir(newbox_master)

    copyfile2( templates.TEMPLATES_ROOT, newbox_root,   templates.BOX_YAMLispNode )
    copyfile2( templates.TEMPLATES_ROOT, newbox_master, templates.PKG_YAMLispNode )
    copyfile2( templates.TEMPLATES_ROOT, newbox_master, templates.ENV_YAMLispNode )
    copyfile2( templates.TEMPLATES_ROOT, newbox_master, templates.GITIGNORE )
    copyfile2( templates.TEMPLATES_ROOT, newbox_master, templates.README )

    # todo: get default templates file from instance
    # todo: perform token substitution on default files

    ### create local master git repository
    with temporary_working_directory(newbox_master):
        newbox_repo = porcelain.init(str(newbox_master))
        porcelain.add(newbox_repo)

    ###
    return newbox_master



#----------------------------------------------------------------------------------------------#
