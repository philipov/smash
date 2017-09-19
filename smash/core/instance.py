#-- smash.core.instance

"""

"""

from powertools import AutoLogger
log = AutoLogger()

################################


from ..util import out
from ..util.out import rprint
from pprint import pprint, pformat
from contextlib import suppress

from pathlib import Path
from shutil import copyfile
from inspect import getmro

from powertools import term


from ..util.meta import classproperty
from powertools import export
from .config import Config
from .env import InstanceEnvironment
from ..util.path import temporary_working_directory

from .. import templates

import wget
from . import platform
Platform = platform.match()

#----------------------------------------------------------------------#

# this is where I can begin to flesh out the idea of config files being actual classes.

# todo: use cookiecutter to deploy an instance


@export
class InstanceTemplate :
    '''template specifying an instance structure'''

    __slots__ = ('instance',)


#----------------------------------------------------------------------#

@export
class SmashTemplate( InstanceTemplate ) :
    ''''a default template for smash instance'''


    def __init__( self, homepath: Path, **kwargs ) :

        log.print( term.pink( '\ncreating new instance in current directory:', homepath ) )
        Path( homepath ).mkdir( 0o600 )

        self.write_root( homepath )
        self.instance = InstanceEnvironment( homepath, **kwargs )

        log.print( term.pink( '\ncreating subdirectories...' ) )
        self.execute_root()

        log.print( term.pink( '\ninstalling self-contained python...' ) )
        self.install_python()

        log.print( term.pink( '\ninstalling required packages' ) )

    @staticmethod
    def write_root( homepath: Path, root_file=None ) :
        if root_file is None :
            src = str( templates.INSTANCE_CONFIG )
            dst = str( Path( homepath ) / templates.INSTANCE_CONFIG.name )
            print( 'writing root config: ', src, dst )
            copyfile( src, dst )

        src = str( templates.PYTHON_CONFIG )
        dst = str( Path( homepath ) / templates.PYTHON_CONFIG.name )
        print( 'writing python package config: ', src, dst )
        copyfile( src, dst )

    def execute_root( self ) :
        '''create directories in root config's path section'''
        paths = self.instance.configtree.root['path'].allitems()
        pprint( paths )

        for path in map( Path, (p for k, p in paths) ) :
            with suppress( FileExistsError ) :
                absolute_path = self.instance.mkdir( path )
                log.print( term.cyan( 'MKDIR: ' ), f"{str(path):<16}", term.pink( ' | ' ), absolute_path )

    def install_python( self ) -> Path :
        ''' download miniconda
            Windows: https://repo.continuum.io/miniconda/Miniconda3-latest-Windows-x86_64.exe
            Linux: https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
        '''

        if Platform == platform.Linux :
            url = 'https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh'
        elif Platform == platform.Win32 :
            url = 'https://repo.continuum.io/miniconda/Miniconda3-latest-Windows-x86_64.exe'
        else :
            raise platform.PlatformError( 'unsupported platform' )

        out_filepath = wget.download( url, str( self.instance.homepath ) )
        log.print( '' )

        return Path(out_filepath)

#----------------------------------------------------------------------#



#----------------------------------------------------------------------#

builtin_templates = {
    'smash' : SmashTemplate,
}

#----------------------------------------------------------------------#
