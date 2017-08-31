

'''
test for list evaluation without using testing framework
'''

#----------------------------------------------------------------------#


from smash.sys.config import ConfigTree
from smash.sys.config import Config
from smash.sys.config import getdeepitem
from smash.sys.out import listprint
from collections import OrderedDict
from pathlib import Path

path = Path('tests/testdata/env/00' ).resolve()
print('path', path)
configs = ConfigTree.from_path(path)


print(configs.current_env['path']['ROOT'])

# print(getdeepitem(configs.current_env._yaml_data, ['__inherit__']))
print(configs.current_env._yaml_data)
listprint( configs.current_env.parents )


#----------------------------------------------------------------------#

