#-- smash.core.pkg

"""
package types,
"""


import logging
log = logging.getLogger( name=__name__ )
logging.basicConfig( level=logging.DEBUG )
log.debug = print

from pathlib import Path

from powertools import export

import conda



#----------------------------------------------------------------------#
@export
class PackageType:
    '''abstract monad for defining packaging semantics'''


################################
@export
class Application( PackageType ):
    ''' non-reusable, end-user code
    '''


class Library( PackageType ):
    ''' nice, reusable code
    '''


################################
@export
class Account( PackageType ):
    ''' information for a unique client
        user definitions and permissions
    '''


@export
class Host( PackageType ):
    ''' configuration for a uniquely-identifyable node on the network
        define which abstract resources are available,
        and the absolute position of those resources
    '''


################################
@export
class Resource( PackageType ):
    ''' abstract local system resource, which can be instantiated by the host
    '''

@export
class Network( Resource ):
    ''' abstract remote network resource
    '''

@export
class NetworkIndex( Network ) :
    ''' remote service that can be used to register and discover other remote resources
    '''


################################



@export
class PackageIndex( Network ) :
    ''' configuration for obtaining smash packages
        package index could be on the local filesystem or the network, depending on host
    '''

@export
class PipPackageIndex( PackageIndex) :
    ''' configuration for obtaining pip-compatible packages
    '''

@export
class CondaPackageIndex( PackageIndex ) :
    ''' configuration for obtaining conda packages
    '''

@export
class FTPPackageIndex( PackageIndex ) :
    ''' Source of packages on a remote ftp server
    '''


################################

@export
class Data( Resource ) :
    ''' abstract database definitions
        associated loader tasks
    '''

@export
class DataStore( Data ) :
    ''' a specific instance of database state
    '''


#----------------------------------------------------------------------#

#----------------------------------------------------------------------#

################################

@export
class Package :
    ''' base class for managing version-controlled modules on a smash instance
        provides an additional hook for importing plugins
    '''
    __pkg__ = [Library]


#----------------------------------------------------------------------#

@export
class Python( Package ):
    ''' install standard python
    '''

################################
@export
class Miniconda( Python ):
    ''' install miniconda
    '''

################################
@export
class Anaconda( Python ):
    ''' install anaconda
    '''


#----------------------------------------------------------------------#

@export
class Shell( Package ) :
    ''' interface for controlling a shell program
        use this to provide a wrapper for shell commands to enable tracking and versioning of state
    '''

################################
@export
class BatchCMD( Shell ) :
    ''' implement wrappers for windows batch script
    '''

################################
@export
class Bash( Shell ) :
    ''' implement wrappers for bash shell
    '''

################################
@export
class Xonsh( Shell ) :
    ''' implement wrappers for xonsh shell
    '''


#----------------------------------------------------------------------#

@export
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


