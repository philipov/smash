# box.py

'''
box test
'''

from powertools import AutoLogger
log=AutoLogger()
from powertools import term
from powertools.print import pprint

from box import Box

#----------------------------------------------------------------------------------------------#

class MetaBox(type):
    ''' put your boxes into boxes
    '''

    @classmethod
    def __prepare__(metacls, name, bases=None, **kwargs):
        return Box()


class Section(dict):

    def __getattr__(self, item):
        return self.data[item]

    def __setattr__(self, key, value):
        self[key] = value
        return self


#----------------------------------------------------------------------------------------------#

################################
class BaseBox(metaclass=MetaBox):
    ''' put your software into boxes
    '''
    path = Box(
        A= 'a',
        B= 'b'
    )

#----------------------------------------------------------------------------------------------#


class ExampleBox(BaseBox):
    ''' '''


    var = {
        'A': '',
        'PATH': BaseBox.path.b
    }

#----------------------------------------------------------------------#

B = ExampleBox

pprint(B.__dict__)


#----------------------------------------------------------------------#
