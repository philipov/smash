#-- smash.sys.pkg

"""
"""


import logging
log = logging.getLogger( name=__name__ )
logging.basicConfig( level=logging.DEBUG )
log.debug = print

from pathlib import Path


__all__ = []

import conda



#----------------------------------------------------------------------#

class PackageType:
    '''abstract monad for defining packaging semantics'''


################################
class Application( PackageType ):
    ''' Non-reusable code
    '''


class Library( PackageType ):
    ''' Reusable code
    '''


################################
class Account( PackageType ):
    ''' information for a unique client
        user definitions and permissions
    '''


class Host( PackageType ):
    ''' configuration for a uniquely-identifyable node on the network
        define which abstract resources are available,
        and the absolute position of those resources
    '''


################################
class Network( PackageType ):
    ''' abstract network resources
    '''


class Data( PackageType ) :
    ''' abstract database definitions
        associated loader tasks
    '''


class DataStore( Data ) :
    ''' a specific instance of database state
    '''


#----------------------------------------------------------------------#

#----------------------------------------------------------------------#

################################
class Package :
    ''' base class for managing version-controlled modules on a smash instance
        provides an additional hook for importing plugins
    '''
    __pkg__ = Library


#----------------------------------------------------------------------#

class Python( Package ):
    ''' install standard python
    '''

################################
class Miniconda( Python ):
    ''' install miniconda
    '''

################################
class Anaconda( Python ):
    ''' install anaconda
    '''


#----------------------------------------------------------------------#

class Shell( Package ) :
    ''' interface for controlling a shell program
        use this to provide a wrapper for shell commands to enable tracking and versioning of state
    '''

################################
class BatchCMD( Shell ) :
    ''' implement wrappers for windows batch script
    '''

################################
class Bash( Shell ) :
    ''' implement wrappers for bash shell
    '''

################################
class Xonsh( Shell ) :
    ''' implement wrappers for xonsh shell
    '''


#----------------------------------------------------------------------#

class Git( Package ):
    pass


#----------------------------------------------------------------------#

builtin_package_types = {
    'app'   : Application,
    'lib'   : Library,
    'acct'  : Account,
    'host'  : Host,
    'net'   : Network,
    'data'  : Data,
    'store' : DataStore
}

################################
builtin_packages = {
    'Python'    : Python,
    'Miniconda' : Miniconda,
    'Anaconda'  : Anaconda,
    'Git'       : Git,
    'Shell'     : Shell,
    'BatchCMD'  : BatchCMD,
    'Bash'      : Bash,
    'Xonsh'     : Xonsh,
}


#----------------------------------------------------------------------#


