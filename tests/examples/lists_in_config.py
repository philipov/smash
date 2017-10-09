

'''
test for list evaluation without using testing framework
'''

#----------------------------------------------------------------------------------------------#


from smash.core.config import ConfigTree
from smash.core.config import Config
from smash.core.config import getdeepitem
from smash.core.out import listprint
from collections import OrderedDict
from pathlib import Path

path = Path('tests/testdata/env/00' ).resolve()
print('path', path)
configs = ConfigTree.from_path(path)


print( configs.env['path']['ROOT'] )

# print(getdeepitem(configs.current_env._yaml_data, ['__inherit__']))
print( configs.env._yaml_data )
listprint( configs.env.parents )


#----------------------------------------------------------------------------------------------#

