#-- smash.core.pkg

"""
package types,
"""

from powertools import AutoLogger
log:AutoLogger = AutoLogger()
from powertools import term as t
from powertools import assertion

from pathlib import Path
from collections import namedtuple
from collections import deque
from collections import OrderedDict
from ..util.yaml import CommentedMap

import hashlib
from ..util.yaml import load as load_yaml
from ..util.path import stack_of_files
#from ..core.config import YAMLisp, CONFIG_PROTOCOL
from .. import templates

from .exception import SmashError

from treelib import Tree


#----------------------------------------------------------------------------------------------#
#   dict/list tree traversal

####################

class DeepKeyError(SmashError, KeyError):
    ''' dkey didn't match '''

def getdeepitem( data, dkey ):
    ''' look up value for a sequence of keys in a deep struct
    '''

    item = data
    for key in dkey:
        if isinstance(item, dict) \
        and key in item:
            item = item[key]

        elif isinstance(item, list) \
        and key < len(item):
            item = item[key]

        else:
            raise KeyError( key, dkey )

    return item


####################

Item = namedtuple('Item', ['dkey', 'value'])

def data2tree(data, *, config=None) -> Tree:
    ''' construct Tree object from nested dict/lists
        breadth-first stack-based tree traversal
    '''

    stack   = deque([ Item(dkey = (), value = data) ])
    tree    = Tree()
    parent  = None

    while stack:
        cur_item = stack.popleft()

        if isinstance(cur_item.value, dict):
            node = YAMLispSection(config, cur_item.dkey, mode=dict)
            for key, value in list(cur_item.value.items()):
                stack.append(Item((*cur_item.dkey, key) , value) )

        elif isinstance(cur_item.value, list):
            node = YAMLispSection(config, cur_item.dkey, mode=list)
            for i, value in list(enumerate(cur_item.value)):
                stack.append( Item((*cur_item.dkey, i), value) )
        else:
            node = YAMLispValue(config, cur_item.dkey, cur_item.value)

        if len(cur_item.dkey) > 0:
            parent = cur_item.dkey[:-1]

        tree.create_node(
            identifier  = cur_item.dkey,
            tag         = cur_item.dkey,
            parent      = parent,
            data        = node
        )
        print(parent, t.cyan(cur_item))

    return tree


#----------------------------------------------------------------------------------------------#


#----------------------------------------------------------------------------------------------#
#   BoxTree

class BoxTree:
    ''' boxes grow on trees '''

    class NotFinalizedError(Exception):
        '''configtree should be finalized for writing before being used'''

    class HashfilePathUndefined(Exception):
        ''' environment must have pkg:HASHFILE to access the hashfile '''
    class HashfileMissing(Exception):
        ''' attempt to access hashfile on a configtree that doesn't have one defined. '''

    ####################
    __slots__ = (
        '_nodes',
        'root',
        'env',
        'out_file',
        'raw_file',
        '_final'
    )
    def __init__( self ) :

        self._nodes     = OrderedDict( )
        self.root       = None
        self.env        = None

        self.out_file   = None
        self.raw_file   = None
        self._final     = False


    ####################
    def add_node( self, node) :
        node: YAMLispNode
        try:
            assert node.filepath not in self._nodes
            self._nodes[node.filepath] = node
        except AssertionError as e:
            log.warn( f'Node already exists {str(node.filepath)}, skipping...' )

        return node


    ####################
    @classmethod
    def from_path( cls, target_path: Path ) :
        """ Find the root file for a target path, load it and its children. """

        ### Find Root File
        try:
            root_file = stack_of_files( target_path, '__root__.yml' )[0]
            root_path = root_file.parents[0]
        except IndexError as e:
            raise FileNotFoundError("Could not find '__root__.yml' file in <" +str(target_path)+ ">, or inside any parent directory")

        ### Find Env File
        try :
            env_file = stack_of_files( target_path, '__env__.yml' )[0]
            env_path = env_file.parents[0]
        except IndexError as e :
            log.info( 'Warning - __env__.yml file not found. Using root node...' )
            env_file = None
            env_path = root_file.parents[0]

        # print("env_file", env_path)
        self = cls()

        if root_file is not None :
            root = self.add_node( YAMLispNode.from_file( root_file, tree=self ) )
            self.root = root

        if env_file is not None:
            env = self.add_node( YAMLispNode.from_file( env_file, tree=self ) )
            self.env = env

        # self.finalize()
        return self


    ####################
    def __getitem__(self, filepath:Path):
        ''' access to nodes using filepath as key '''
        return self._nodes[filepath]



    # @property
    # def hashfile( self ) -> YAMLispNode :
    #     ''' config containing the saved hash results of the last smash invokation '''
    #     try:
    #
    #         hashfile_path = self.env[templates.BOX_SECTION]['HASHFILE']
    #     except YAMLispSectionView.CouldNotGetItem as e:
    #         raise YAMLispTree.HashfilePathUndefined(self)
    #
    #     try:
    #         return self[Path(hashfile_path)]
    #     except KeyError as e:
    #         raise YAMLispTree.HashfileMissing(self, hashfile_path)


    ####################
    @property
    def has_changed(self) -> bool:
        ''' if the files are the same, we can skip running export (save Shell).
            if the hashes of the new configs don't match the hashes in the hashfile,
            or there are new config files, or if the hashfile doesn't exist,
            then all exports will be executed again.
        '''
        return True

        # try:                                    ### missing hashfile
        #
        #     hashes = self.hashfile['smashbrowns']
        # except YAMLispTree.HashfileMissing as e:
        #     log.warn(e)
        #     return True
        #
        # hashitems = list( hashes.items() )      ### file number doesn't match
        # if len(hashitems) != len(self.nodes):
        #     log.warn('different number of configs')
        #     return True
        #
        # for filename, hashcode in hashitems:    ### codes don't match
        #     log.info('check hashes ', filename)
        #     new_hash = self[Path( filename )].hash
        #     if str(self.hashfile.filepath) == str(filename):
        #         continue
        #     if new_hash != hashcode:
        #         log.warn('hashcode mismatch: ', filename )
        #         log.warn( new_hash, term.red(' != '), hashcode )
        #         return True
        # return False                            ### Match!


#----------------------------------------------------------------------------------------------#


#----------------------------------------------------------------------------------------------#
#   Node

####################
class YAMLispNode:
    ''' container for a single file of yamlisp config data '''

    class ProtocolError(Exception):
        ''' Yaml file did not have the correct protocol '''

    class EmptyFileWarning(Exception):
        ''' May wish to ignore blank config files '''

    class SubstitutionValueTypeError(Exception):
        ''' couldn't value the type of the value obtained from token substitution'''

    class TokenExpressionError(Exception):
        ''' $ tokens are scalar substitutions, @ tokens are sequence extensions '''

    class TokenRecursionError(Exception):
        ''' RecursionError occured while performing token substitution '''

    class InheritSelfError(Exception):
        ''' config is its own parent '''

    class InheritLoopError(Exception):
        ''' config has a parent whose parent is config '''

    class ParentNotFound(Exception):
        ''' filepath in __inherit__ list could not be found '''

    class MissingCommandWordError(Exception):
        ''' YAMLispNode s-expressions must contain at least a command word'''

    class YAMLispNodeKwargDuplicate(Exception):
        ''' duplicate keys from dictionaries on the same line of a YAMLispNode script'''

    class DuplicateScriptLineName(Exception):
        ''' two s-expressions in a YAMLispNode command word have the same key '''

    class DelayedEvaluationTokenNotDuringScript( Exception ) :
        ''' avoid infinite substitution loop for delayed tokens'''


    ####################
    __slots__ = (
        'tree',         # boxtree reference
        'filepath',     # node identifier
        '_raw_data',    # dict of dict/list
        '_parse_tree',  # Tree of Section/Value
        '_flat_data',   # Cache for final value
        '_hash',        # check that source hasn't changed
        'is_final',     # make immutable

    )
    def __init__(self, *,
            tree:BoxTree    = None,
            data:dict       = None,
            filepath:Path   = None,
        ):

        self.tree           = tree

        if data is not None:
            self._raw_data      = CommentedMap()
            self._parse_tree    = Tree()
        else:
            self._raw_data      = data
            self._parse_tree    = data2tree(data, config=self)

        self._hash          = None
        self.filepath       = filepath
        if filepath is not None:
            self.hash()

        self.is_final       = False

    ####################
    @classmethod
    def from_file( cls,
            target:Path, *,
            tree=None
        ) :
        ''' load a YAMLispNode from a YAMLispNode file'''

        filepath    = target.resolve()

        data        = load_yaml( target )
        if  data is None:
            raise YAMLispNode.EmptyFileWarning(filepath)

        inst        = cls( tree=tree, data=data, filepath=filepath )
        # inst.load_parents()

        return inst


    ####################
    def hash(self):
        ''' return the hash of the file
            if filepath is set but hash is not,
                calculate and store the hash
        '''
        if  self._hash is None \
        and self.filepath is not None:
            hasher = hashlib.sha1()
            with open(self.filepath, 'rb') as file:
                buffer = file.read()
                hasher.update(buffer)
                self._hash   = hasher.hexdigest()

        return self._hash


    ####################
    @property
    def raw_data(self):
        ''' access to a view on the raw values
            the view should mediate modifications to raw values
        '''
        if self._raw_data is None:
            self._raw_data = CommentedMap()
        return self._raw_data


    @property
    def path(self):
        ''' directory containing the config '''
        return self.filepath.parent


    @property
    def name(self):
        return #self['__yamlisp__']['name']


    ####################
    def new_section(self, dkey):
        ''' add new branch for dkey'''


    ####################
    def __getitem__(self, key):
        ''' access to fully evaluated values
        '''

        if key in self._parse_tree:
            return self._parse_tree[key]

        if key not in self.raw_data:
            self._raw_data[key] = CommentedMap()

        dkey = [key]
        section = YAMLispSection(self, dkey)
        self._parse_tree[key] = section
        return section



    ####################
    def parse_dkey(self, dkey):
        ''' generate the parse subtree for an dkey '''

    ####################
    def parse_all(self):
        ''' resolve the entire parse tree '''

        self.is_final = True


    ####################
    @property
    def parse_tree(self):
        ''' access to fully resolved parse tree'''
        if not self.is_final:
            self.parse_all()
        return self._parse_tree

    ####################
    def items(self):
        ''' return a flattenned parse tree '''


    ####################
    @property
    def exports(self):
        ''' __exports__ '''
        return NotImplemented

    @property
    def imports(self):
        ''' __imports__ '''
        return NotImplemented

    @property
    def scripts(self):
        ''' __scripts__ '''
        return NotImplemented


#----------------------------------------------------------------------------------------------#
#   Section

class YAMLispSection:
    ''' a proxy object to support config[key1][key2][key3] style operations '''
    __slots__ = (
        'config',
        'dkey',
        'mode',
        '_raw',
        '_parse',
        '_flat'
    )
    def __init__(self,
            config, dkey, *,
            mode:type=dict,      # 'dict' or 'list'
        ):
        self.config     = config
        self.dkey       = dkey
        self.mode       = mode
        self._raw       = dict()
        self._parse     = dict()
        self._flat      = dict()

    ####################
    # def __contains__(self, key):
    #     ''' if key is in the parent config's raw data'''
    #     dkey    = [*self.dkey, key]

    ####################
    def __getitem__(self, key):
        ''' look up the key, or pass along to another layer of YAMLispSections
        '''
        if key in self._parse.keys():
            return self._parse[key]

        if key in self._raw.keys():
            return self._raw[key]

        return NotImplementedError

    ####################
    def __setitem__(self, key, value):
        ''' look up the key, or pass along to another layer of YAMLispSections
        '''

        # if key in self:
        self._raw[key] = value


#----------------------------------------------------------------------------------------------#
#   Value

class YAMLispValue:
    ''' a string that might contain substitution or appendation tokens'''
    __slots__ = (
        'config',
        'dkey',
        'value',
        'tokens',
        'comment',
    )
    def __init__( self,
            config, dkey, value, *,
            comment:str = None,
        ):
        self.config     = config
        self.dkey       = dkey
        self.value      = value
        self.comment    = comment

        self.tokens     = dict()

    ####################


#----------------------------------------------------------------------------------------------#
#   Token

class YAMLispToken:
    ''' a string that might contain substitution or appendation tokens'''
    __slots__ = (
        'parent',
        'value',
        'tokens',
    )
    def __init__(self,
            parent, value,
        ):
        self.parent = parent
        self.value  = value
        self.tokens = dict()

    ####################


#----------------------------------------------------------------------------------------------#

