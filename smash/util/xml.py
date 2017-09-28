
#-- smash.sys.yaml

'''
process yaml files
'''

from powertools import AutoLogger
log = AutoLogger()

from collections import OrderedDict
from pathlib import Path

import xmltodict

#----------------------------------------------------------------------#

def load(filename:Path):
    with filename.open() as xmlfile :
        data = xmltodict.parse( xmlfile.read() )
    return data


def convert_xmldict(data):
    result = None
    log.info(type(data))

    return result

def data2xml(data):
    ''' convert lists/dicts to xml.etree '''


def xml2data(filename:Path):
    ''' convert file containing XML to lists/dicts '''

#----------------------------------------------------------------------#

dump_args = OrderedDict(
    pretty=True,
    full_document=False,
    attr_prefix='~',
    short_empty_elements=True
)

def dump(filepath: Path, data, kwargs=dump_args ):
    with open(str(filepath), 'w') as file:
        xmltodict.unparse(data, output=file )
        xmltodict.unparse(data)





#----------------------------------------------------------------------#
