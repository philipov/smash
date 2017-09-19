#-- smash.core.env

"""
"""

import sys
from powertools import classproperty
from powertools import export

#----------------------------------------------------------------------#
@export
class Platform:
    ''' keep track of differences between platforms '''

    @classproperty
    def match(cls) -> bool:
        '''check the type of the host platform'''

        raise NotImplementedError


#----------------------------------------------------------------------#
@export
class Win32(Platform):
    ''' windows '''

    @classproperty
    def match( cls ) :
        return sys.platform == 'win32'


#----------------------------------------------------------------------#
@export
class Linux(Platform):
    ''' everything else '''

    @classproperty
    def match( cls ) :
        return sys.platform in ('linux', 'linux2')


#----------------------------------------------------------------------#
@export
class Mac(Platform):
    ''' another type of linux '''

    @classproperty
    def match( cls ) :
        return False


#----------------------------------------------------------------------#

class PlatformError(Exception):
    '''unsupported or unknown platform'''

@export
def match() -> Platform:
    if Win32.match:
        return Win32
    elif Linux.match:
        return Linux
    elif Mac.match:
        return Mac
    else:
        raise PlatformError('unknown platform')

#----------------------------------------------------------------------#
