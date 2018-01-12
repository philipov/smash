#-- smash.core.exceptions

""" smash exception bases
"""


#----------------------------------------------------------------------------------------------#


class SmashException(Exception):
    ''' base class for package exceptions
    '''

class SmashError(SmashException):
    ''' errors are fatal
    '''

class SmashWarning(SmashException):
    ''' warnings are not fatal unless strict
    '''

class SmashCondition(SmashException):
    ''' conditions pass a value back up the stack
        they should be caught and implemented
    '''


#----------------------------------------------------------------------------------------------#
