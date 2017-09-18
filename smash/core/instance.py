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
from inspect import getmro
from powertools import term

from ..util.meta import classproperty
from powertools import export
from .config import Config
from .env import InstanceEnvironment
from ..util.path import temporary_working_directory

#----------------------------------------------------------------------#

# this is where I can begin to flesh out the idea of config files being actual classes.

# todo: use cookiecutter to deploy an instance


@export
class InstanceTemplate :
    '''template specifying an instance structure'''

    __slots__ = ('instance',)
    def __init__( self, homepath:Path, **kwargs ) :

        self.instance = InstanceEnvironment(homepath, **kwargs)
        self.prepare_pathsystem( )


    pathsystem = ['.']

    def prepare_pathsystem( self ):
        '''create directories in the pathsystem list for subclass and parents'''

        for cls in filter(  lambda x: x is not object,
                            reversed(getmro(type(self)))
                            ):
            for path in map(Path, cls.pathsystem):
                with suppress(FileExistsError):
                    absolute_path = self.instance.mkdir(path)
                    log.print( term.pink( 'MKDIR: ' ), f"{str(path):<16}", term.pink( ' | ' ), absolute_path )

#----------------------------------------------------------------------#

@export
class SmashTemplate( InstanceTemplate ) :
    ''''a default template for smash instance'''

    pathsystem = [
        'env',
        'pkg',
        'dev',
        'data',
        'docs',
        'sh',
        'secrets'
    ]


#----------------------------------------------------------------------#

@export
class YAMLTemplate( InstanceTemplate ) :
    ''' load a template from a YAML file'''


#----------------------------------------------------------------------#

builtin_templates = {
    'smash' : SmashTemplate,
    'yaml'  : YAMLTemplate
}

#----------------------------------------------------------------------#
