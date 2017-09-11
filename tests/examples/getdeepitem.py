

'''
test for getdeepitem without using testing framework
'''

#----------------------------------------------------------------------#


from smash.core.config import ConfigTree
from smash.core.config import Config
from smash.core.config import getdeepitem
from collections import OrderedDict

configtree = ConfigTree()
config = Config( tree=configtree )
configtree.root=config
config._yaml_data = OrderedDict( )
config._yaml_data[1] = OrderedDict( )
config._yaml_data[1][2] = OrderedDict( )
config._yaml_data[1][2][3] = OrderedDict( )
config._yaml_data[1][2][3][4] = OrderedDict( )
config._yaml_data[1][2][3][4][5] = 6
keys = [1, 2, 3, 4, 5]

value0 = getdeepitem( config._yaml_data, keys )
value1 = config[1][2][3][4][5]




#----------------------------------------------------------------------#

