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

from ..core.config import Config, ConfigTree
from ..core.env import InstanceEnvironment, BoxEnvironment
from .. import templates

#----------------------------------------------------------------------------------------------#


def new( instance:InstanceEnvironment, boxpath:Path ):
    ''' create a new box
    '''
    from dulwich import porcelain

    ### create default paths/files
    boxes_root      = Path(instance.configtree.env[templates.PATH_VARS_SECTION][templates.PATH_BOXES])

    newbox_root     = boxes_root / boxpath
    newbox_master   = newbox_root / 'master'
    with suppress( FileExistsError ) :
        instance.mkdir(newbox_root)
    with suppress( FileExistsError ) :
        instance.mkdir(newbox_master)

    copyfile( templates.BOX_BLANK, str( newbox_root/templates.BOX_YAMLISP ) )
    copyfile( templates.PKG_BLANK, str( newbox_master/templates.PKG_YAMLISP ) )
    copyfile( templates.ENV_BLANK, str( newbox_master/templates.ENV_YAMLISP ) )

    # todo: get default templates file from instance
    # todo: perform token substitution on default files

    ### create local master git repository
    repo = porcelain.init(str(newbox_master))

    ###
    return newbox_master



#----------------------------------------------------------------------------------------------#
