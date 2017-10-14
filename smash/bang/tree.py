#-- smash.bang.tree

"""
"""

from powertools import AutoLogger
log = AutoLogger()

################################

from powertools import term
from ..util import out
from ..util.out import rprint
from pprint import pprint, pformat

from pathlib import Path
from shutil import copyfile
from contextlib import suppress
from itertools import chain

from powertools import export
from ..core.config import Config
from ..core.env import InstanceEnvironment

from .. import templates

import wget
from ..core import platform
Platform = platform.match()

from ..core.pkg import Miniconda


#----------------------------------------------------------------------------------------------#

def write_root( homepath: Path, root_file=None ) :
    ''' strap your boots with hard-coded paths '''

    if root_file is None :
        src = str( templates.INSTANCE_CONFIG )
        dst = str( Path( homepath ) / templates.ROOT_YAMLISP )
        print( term.cyan('writing root config: '), term.dyellow(src), "-->", term.dyellow(dst), '\n' )
        copyfile( src, dst )

        src = str( templates.SMASH_PY )
        dst = str( Path( homepath ) / templates.SMASH_PY.name  )
        print( term.cyan( 'writing smash.py: ' ), term.dyellow( src ), "-->", term.dyellow( dst ), '\n' )
        copyfile( src, dst )


################################

def create_pathsystem( config:Config, instance:InstanceEnvironment ) :
    ''' create directories in config's path and pkg sections '''

    paths = chain(
        config['path'].allpaths(),
        config['pkg'].allpaths(),
    )
    for key, path in paths:
        with suppress( FileExistsError ) :
            log.info( term.pink( 'MKDIR: ' ), f"{str(path):<16}" )
            absolute_path = instance.mkdir( path )




################################

def install_package( config:Config, template_path, pkg_name):
    for filename in [
            templates.NIX_YAMLISP,
            templates.WIN_YAMLISP,
            templates.MAC_YAMLISP,
            templates.PKG_YAMLISP,
        ]:
        src = str( template_path / filename )
        dst = str( Path(config['pkg'][pkg_name]) / filename)

        try:
            copyfile( src, dst )
            log.print( term.cyan('writing ',pkg_name,' package config: '),
                       '',term.dyellow(src),
                       ' --> ', term.dyellow(dst),
                       '\n')
        except:
            raise

        config.tree.add_node(Path(dst))



def install_default_packages( config:Config ):
    ''' copy additional yamlisp files '''

    install_package( config, templates.NET,     'PLATFORM' )
    install_package( config, templates.HOST,    'HOST' )
    install_package( config, templates.NET,     'NET' )

    install_package( config, templates.PYTHON,  'PYTHON' )

#----------------------------------------------------------------------------------------------#

def new( homepath: Path, **kwargs ):

    log.print( term.pink( '\ncreating new instance in current directory... '), homepath.name )

    ###
    Path( homepath ).mkdir( 0o600 )
    write_root( homepath )

    ### inherit context as a parent from kwargs # todo: explicit argument
    instance = InstanceEnvironment( homepath, **kwargs )
    config = instance.configtree.env

    ###
    log.print( term.pink( '\ncreating subdirectories... ' ) )
    create_pathsystem( config, instance )

    ###
    log.print( term.pink( '\ninstalling smash prerequisites... ' ) )
    install_default_packages( config )

    ###
    log.print( term.pink( '\ninstalling self-contained python...' ) )
    with Miniconda(instance, config) as mc:
        mc.download()
        mc.install()

    log.info(mc)

    return instance


#----------------------------------------------------------------------------------------------#