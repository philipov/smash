#-- smash.core.pkg

"""
package types,
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
    ''' non-reusable, end-user code
    '''


class Library( PackageType ):
    ''' nice, reusable code
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
class Resource( PackageType ):
    ''' abstract local system resource, which can be instantiated by the host
    '''

class Network( Resource ):
    ''' abstract remote network resource
    '''

class NetworkIndex( Network ) :
    ''' remote service that can be used to register and discover other remote resources
    '''


################################


class PackageIndex( Network ) :
    ''' configuration for obtaining smash packages
        package index could be on the local filesystem or the network, depending on host
    '''

class PipPackageIndex( PackageIndex) :
    ''' configuration for obtaining pip-compatible packages
    '''

class CondaPackageIndex( PackageIndex ) :
    ''' configuration for obtaining conda packages
    '''

class FTPPackageIndex( PackageIndex ) :
    ''' Source of packages on a remote ftp server
    '''


################################
class Data( Resource ) :
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
    __pkg__ = [Library]


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
    'app'       : Application,
    'lib'       : Library,

    'acct'      : Account,
    'host'      : Host,

    'res'       : Resource,
    'net'       : Network,

    'idx-net'   : NetworkIndex,
    'idx-pkg'   : PackageIndex,
    'idx-pip'   : PipPackageIndex,
    'idx-conda' : CondaPackageIndex,
    'idx-ftp'   : FTPPackageIndex,

    'data'      : Data,
    'store'     : DataStore
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


