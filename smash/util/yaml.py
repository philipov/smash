#-- smash.sys.yaml

'''
process yaml files
'''

from powertools import AutoLogger
log = AutoLogger()
from powertools.print import rprint

from collections import OrderedDict
from collections import namedtuple
from collections import defaultdict
from pathlib import Path


#----------------------------------------------------------------------#
### YAML Anchors, references, nested values    - https://gist.github.com/bowsersenior/979804

import ruamel.yaml as yaml
try :
    from ruamel.yaml import CLoader as Loader, CDumper as Dumper
except ImportError :
    from ruamel.yaml import Loader, Dumper
import sys

yaml.representer.RoundTripRepresenter.add_representer(
    OrderedDict,
    yaml.representer.RoundTripRepresenter.represent_ordereddict )

from ruamel.yaml.comments import CommentedMap

from ruamel.yaml import dump as yaml_dump


#----------------------------------------------------------------------#
### LOAD YAMLISP

### OrderedDictYYAMLLoader - https://gist.github.com/enaeseth/844388
class OrderedDictYAMLLoader(  Loader ) :
    """
    A YAML loader that loads mappings into ordered dictionaries.
    """

    def __init__( self, *args, **kwargs ) :
        Loader.__init__( self, *args, **kwargs )

        self.add_constructor( u'tag:yaml.org,2002:map', type( self ).construct_yaml_map )
        self.add_constructor( u'tag:yaml.org,2002:omap', type( self ).construct_yaml_map )

    def construct_yaml_map( self, node ) :
        data = CommentedMap( )
        yield data
        value = self.construct_mapping( node )
        data.update( value )

    def construct_mapping( self, node, deep=False ) :
        if isinstance( node, yaml.MappingNode ) :
            self.flatten_mapping( node )
        else :
            raise yaml.constructor.ConstructorError(
                None, None,
                'expected a mapping node, but found %s' % node.id,
                node.start_mark )

        mapping = CommentedMap( )
        for key_node, value_node in node.value :
            key = self.construct_object( key_node, deep=deep )
            try :
                hash( key )
            except TypeError as exc :
                raise yaml.constructor.ConstructorError( 'while constructing a mapping',
                                                         node.start_mark, 'found unacceptable key (%s)' % exc,
                                                         key_node.start_mark )
            value = self.construct_object( value_node, deep=deep )
            mapping[key] = value
        return mapping


##############################
def load( filename:Path ) :
    result = None
    with filename.open( ) as file:
        result = yaml.load(file, Loader=OrderedDictYAMLLoader )

    return result

#----------------------------------------------------------------------#

# todo: custom dict that keeps the original file cached and associates values to lines in the file.

#----------------------------------------------------------------------#
#### DUMP YAMLISP

import re
split_fields = re.compile(
r"""
    (?P<indent>\s*)
    (?P<dash>-?\s*)
    (?P<key>[^\s]*)\s?
    (?P<value>[^\s]*)
""", re.VERBOSE)

class LineFields(namedtuple('LineFields', ['indent', 'dash', 'key', 'value'])):
    rank        = property( lambda self: len( self.indent ) + len( self.dash ) )
    min_padding = property( lambda self: self.rank + len( self.key ) + 2 )

COMMENT_BAR = '############################################################\n'

##############################
def alignment_and_breaks( yaml_output:str ):

    ### parse
    lines   = list()
    for line in yaml_output.splitlines(True):
        m       = split_fields.match(line)
        lf = LineFields(
            m.group('indent'),
            m.group('dash'),
            m.group('key'),
            m.group('value')
        )
        lines.append(lf)

    ### find padding
    maxpadding  = defaultdict(int)
    for line in lines:
        line:LineFields
        is_list     = len(line.dash) == len(line.value) == 0
        if not is_list and maxpadding[line.rank] < line.min_padding:
            maxpadding[line.rank] = line.min_padding
    # log.info('max_len:')
    # rprint(maxpadding)

    ### reconstruct
    result      = COMMENT_BAR
    prevline    = LineFields(' ','','','')

    for line in lines:
        line:LineFields

        empty_line  = '\n' if any(case(line, prevline)    # todo: make this pluggable
            for case in [
                lambda l, p: p.rank > l.rank,
                lambda l, p: p.key.startswith('~') and len(l.dash) > 0,
                lambda l, p: p.key in (
                    '__protocol__:',
                    '__inherit__',
                ),
            ]
        )        else ''

        padding     = maxpadding[line.rank]
        left        = f'{line.indent}{line.dash}{line.key}'
        padded_line = f'{left:<{padding}} {line.value}'
        result     += f'{empty_line}{padded_line}\n'

        prevline = line
        # lens        = LineFields(*(len(v) for v in line))
        # log.info(f'{line.indent_len:>3} {line.padding:>3} {maxpadding[line.indent_len]:>3} {lens} {line}')
        # log.info('') if empty_line == '\n' else None

    result += '\n' + COMMENT_BAR
    return result


##############################
def make_yml() :
    yml = yaml.YAML()
    yml.explicit_start      = False
    yml.indent              = 2
    yml.block_seq_indent    = 0
    yml.typ                 = 'safe'
    yml.tags                = False

    return yml

def dump( filename: Path, data ) :
    yml = make_yml()

    with open( str(filename), 'w' ) as file :
        yml.dump( data, file, transform=alignment_and_breaks )
    # yml.dump( data, sys.stdout, transform=transformer)


#----------------------------------------------------------------------#
