#-- smash.core.instance

"""

"""

import logging

log = logging.getLogger( name=__name__ )
debug = lambda *a, **b : print( "".join( str( arg ) for arg in a ) )
info = lambda *a, **b : print( "".join( str( arg ) for arg in a ) )

################################


from ..util import out
from ..util.out import rprint
from pprint import pprint, pformat

from pathlib import Path

from ..util.meta import classproperty
from powertools import export
from .config import Config
from .env import InstanceEnvironment

#----------------------------------------------------------------------#

# this is where I can begin to flesh out the idea of config files being actual classes.

# todo: use cookiecutter to deploy an instance

class InstanceTemplateBase :
    def prepare_pathsystem(self):
        pass

@export
class InstanceTemplate(InstanceTemplateBase) :
    '''template specifying an instance structure'''

    __slots__ = ('instance')
    def __init__( self, homepath:Path, **kwargs ) :
        if homepath.exists():
            raise FileExistsError( ''.join( str(s) for s in [homepath,' already exists' ]) )
        self.instance = InstanceEnvironment(homepath, **kwargs)

        self.prepare_pathsystem( )


    pathsystem = ['.']

    def prepare_pathsystem( self ):
        for path in map(Path, self.pathsystem):
            self.instance.mkdir(path)
        super().prepare_pathsystem()


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
        'secrets',
        *InstanceTemplate.pathsystem
    ]



#----------------------------------------------------------------------#

builtin_templates = {
    'smash' : SmashTemplate,
}

#----------------------------------------------------------------------#
