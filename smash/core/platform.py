#-- smash.core.env

"""
"""

import sys
from powertools import classproperty

#----------------------------------------------------------------------#

class Platform:
    ''' keep track of differences between platforms '''

    @classproperty
    def match(cls) -> bool:
        '''check the type of the host platform'''

        raise NotImplementedError


#----------------------------------------------------------------------#
class Win32(Platform):
    ''' windows '''

    @classproperty
    def match( cls ) :
        return sys.platform == 'win32'


#----------------------------------------------------------------------#
class Linux(Platform):
    ''' everything else '''

    @classproperty
    def match( cls ) :
        return sys.platform in ('linux', 'linux2')


#----------------------------------------------------------------------#
class Mac(Platform):
    ''' another type of linux '''

    @classproperty
    def match( cls ) :
        return False


#----------------------------------------------------------------------#
