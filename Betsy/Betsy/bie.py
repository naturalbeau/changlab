"""

Glossary:
fact         Starting point.
goal         Desired outcome.
rule         Another word is proposition.
consequent   Second half of a rule.
antecedent   First half of a rule.

Modules "convert" one DataType to another.
Modules "produce" a Data node.


Functions:
backchain
optimize_network
prune_network_by_start
prune_network_by_internal

summarize_moduledb
print_modules

test_bie


Classes:
Attribute
DataType
Data
Module
QueryModule
ModuleDbSummary
Network

"""

# Classes:
# _OptimizeNoCycles
# _OptimizeNoDuplicateData
# _OptimizeNoDuplicateModules
# _OptimizeNoDanglingNodes
# _OptimizeNoOverlappingData
# _OptimizeNoInvalidConsequents
#
#
# Functions:
# _make_goal
# 
# _backchain_to_modules       Given a consequent, find compatible Modules.
# _backchain_to_antecedent    Given a consequent and module, find antecedents.
# _backchain_to_ids
# _make_backchain_dict
#
# _can_module_produce_data
# _can_converting_module_produce_data
# _can_nonconverting_module_produce_data
# _can_module_take_data
#
# _can_reach_by_bc
# _can_reach_by_fc
#
# _find_data_node
# _find_module_node
# _is_compatible_with_start
# _is_compatible_with_internal
# _assign_case_by_type
# _get_attribute_type
# _intersection
# _is_subset
# 
# _print_nothing
# _print_string
# _print_line
# _print_network
# _plot_network_gv
# _pretty_attributes


# The value of an attribute can be:
# NOVALUE   Value is not specified.  Meaning is ambiguous (see below).
#           Can be default or don't care.
# ATOM      e.g. "mean"
# ANYATOM   Value can be any string.  Used for parameters like the
#           number of genes to filter out of a list, which can be any
#           number.  Any string can match ATOM.
# LIST      e.g. ["mean", "median"], ["logged", "not_logged"]
#
# Module Node: Antecedent
# NOVALUE   This attribute is not relevant for the module.
# ATOM      The module requires a specific value.
# ANYATOM   UNDEFINED.  When is this used?
# LIST      The module can take any of these values.
#           E.g. filter_missing_with_zeros    missing=["yes", "unknown"]
# 
# Module Node: Consequent
# NOVALUE   Attribute is irrelevant for the module.  Antecedent must also
#           be NOVALUE.
# ATOM      The module generates a specific value.
# ANYATOM   The module can generate any value to fit the requirements of
#           the next Data node.
# LIST      There are three possibilities here:
#           1.  The module doesn't change this value.  i.e. the LIST
#               is exactly the same in the antecedent.
#               e.g. missing_values=["no", "zero_fill", "median_fill"])
#               in both the antecedent and consequent.
#           2.  The module can generate any one of these values to fit
#               the requirements of the next Data node.
#               e.g. gene_normalize=["mean", "median"]
#           3.  The module produces a specific value, but we won't
#               know what it is until runtime.
#               e.g. logged=["no", "yes"]
#               This is called a QUERY module.  It queries some aspect
#               of the data.
#
# Data Node
# NOVALUE   UNDEFINED.
# ATOM      A specific value.
# ANYATOM   UNDEFINED.  Is this needed?
# LIST      The actual value is unknown, but can be one of these options.


NOVALUE = "___BETSY_NOVALUE___"
ANYATOM = "___BETSY_ANYATOM___"

TYPE_ATOM, TYPE_LIST, TYPE_ANYATOM, TYPE_NOVALUE = range(4)
#LIST_SPECIFIES_ALTERNATES, LIST_SPECIFIES_RESPONSES = range(2)


class Attribute:
    def __init__(self, **keywds):
        # keywds is a dictionary of:
        # <attribute name>  :  value
        # DEFAULT           :  default_value
        name = None
        for x in keywds:
            if x in ["REQUIRED", "DEFAULT"]:
                continue
            assert name is None
            name = x
        assert name is not None
        
        attr_type = _get_attribute_type(keywds, name)
        assert attr_type in [TYPE_ANYATOM, TYPE_LIST], "%s %s" % (name, key)
        assert "DEFAULT" in keywds, "DEFAULT not given for %s." % name

        if attr_type == TYPE_LIST:
            assert keywds["DEFAULT"] in keywds[name], \
                   "DEFAULT [%s] not found in values: %s." % (
                keywds["DEFAULT"], keywds[name])

        self.name = name
        self.values = keywds[name]
        self.REQUIRED = bool(keywds.get("REQUIRED"))
        self.DEFAULT = keywds["DEFAULT"]
    def __cmp__(self, other):
        if not isinstance(other, Attribute):
            return cmp(id(self), id(other))
        x1 = [self.name, self.values, self.REQUIRED, self.DEFAULT]
        x2 = [other.name, other.values, other.REQUIRED, other.DEFAULT]
        return cmp(x1, x2)
        

class DataType:
    def __init__(self, name, *attribute_objects):
        # Make sure the attributes are value.
        for attr in attribute_objects:
            assert isinstance(attr, Attribute)
        attributes = {}  # name -> values
        for attr in attribute_objects:
            attributes[attr.name] = attr.values
        self.name = name
        self.attribute_objects = attribute_objects
        self.attributes = attributes
    def __cmp__(self, other):
        if not isinstance(other, DataType):
            return cmp(id(self), id(other))
        x1 = [self.name, self.attribute_objects, self.attributes]
        x2 = [other.name, other.attribute_objects, other.attributes]
        return cmp(x1, x2)
    def get_required(self):
        # Return a list of the name of the required attributes.
        x = [x for x in self.attribute_objects if x.REQUIRED]
        x = [x.name for x in x]
        return x
    def get_defaults(self):
        # Return a dictionary of the attributes to their default values.
        defaults = {}
        for attr in self.attribute_objects:
            defaults[attr.name] = attr.DEFAULT
        return defaults
    def __call__(self, **attributes):
        # Create a Data object.
        for key in attributes:
            assert key in self.attributes, "Unknown attribute for %s: %s" % (
                self.name, key)
        return Data(self, attributes)


class Data:
    # Members:
    # datatype     Datatype object.
    # attributes   Dict of attribute name -> value.

    def __init__(self, datatype, attributes):
        # Make sure the attributes of this Data object match the
        # attributes of the DataType.
        # 
        # CASE  DATA_TYPE  DATATYPE_TYPE  RESULT
        #   1    NOVALUE     NOVALUE      ERROR.  DATA can't be NOVALUE.
        #   2    NOVALUE     ANYATOM      ERROR.  
        #   3    NOVALUE       ATOM       ERROR.
        #   4    NOVALUE       LIST       ERROR.
        #   5    ANYATOM     NOVALUE      ERROR.
        #   6    ANYATOM     ANYATOM      OK.
        #   7    ANYATOM       ATOM       Bad.
        #   8    ANYATOM       LIST       Bad.
        #   9      ATOM      NOVALUE      ERROR.
        #  10      ATOM      ANYATOM      OK.
        #  11      ATOM        ATOM       OK if ATOMs equal.
        #  12      ATOM        LIST       OK if ATOM in LIST.
        #  13      LIST      NOVALUE      ERROR.
        #  14      LIST      ANYATOM      Bad.
        #  15      LIST        ATOM       Bad.
        #  16      LIST        LIST       OK if DATA LIST is subset.
        data_attr = attributes
        dtyp_attr = datatype.attributes
        for key, values in attributes.iteritems():
            assert key in datatype.attributes, "Unknown key: %s" % key
            
            DATA_VALUE = data_attr.get(key)
            DTYP_VALUE = dtyp_attr.get(key)
            DATA_TYPE = _get_attribute_type(data_attr, key)
            DTYP_TYPE = _get_attribute_type(dtyp_attr, key)
            CASE = _assign_case_by_type(DATA_TYPE, DTYP_TYPE)

            if CASE in [1, 2, 3, 4, 5, 9, 13]:
                raise AssertionError
            elif CASE in [6, 10]:
                pass
            elif CASE in [7, 8, 14, 15]:
                raise AssertionError, "type mismatch"
            elif CASE == 11:
                assert DATA_VALUE == DTYP_VALUE
            elif CASE == 12:
                assert DATA_VALUE in DTYP_VALUE, \
                       "Value [%s] not found in: %s" % (DATA_VALUE, DTYP_VALUE)
            elif CASE == 16:
                for x in DATA_VALUE:
                    assert x in DTYP_VALUE, "Invalid value for %s: %s" % (
                        key, x)
            else:
                raise AssertionError, "%s %s" % (DATA_TYPE, DTYP_TYPE)
        self.datatype = datatype
        self.attributes = attributes.copy()
    def __cmp__(self, other):
        if not isinstance(other, Data):
            return cmp(id(self), id(other))
        x1 = [self.datatype, self.attributes]
        x2 = [other.datatype, other.attributes]
        return cmp(x1, x2)
    def __str__(self):
        return self.__repr__()
    def __repr__(self):
        # Don't print out attributes with default values.
        attributes = {}
        defaults = self.datatype.get_defaults()
        for key, value in self.attributes.iteritems():
            if value == defaults[key]:
                continue
            attributes[key] = value
        x = [
            self.datatype.name,
            _pretty_attributes(attributes),
            ]
        x = [x for x in x if x]
        return "Data(%s)" % ", ".join(x)
    def copy(self):
        return Data(self.datatype, self.attributes)


class Module:
    # A Module can take one or more antecedents.
    def __init__(self, name, ante_datas, cons_data, **parameters):
        import operator

        if not operator.isSequenceType(ante_datas):
            ante_datas = [ante_datas]
        # If a DataType is provided, convert it into a Data object
        # with no attributes.
        for i in range(len(ante_datas)):
            if isinstance(ante_datas[i], DataType):
                ante_datas[i] = ante_datas[i]()
        if isinstance(cons_data, DataType):
            cons_data = cons_data()
            
        self.name = name
        self.ante_datas = ante_datas
        self.cons_data = cons_data
        self.parameters = parameters
    def __cmp__(self, other):
        if not isinstance(other, Module):
            return cmp(id(self), id(other))
        x1 = [self.name, self.ante_datas, self.cons_data, self.parameters]
        x2 = [other.name, other.ante_datas, other.cons_data, other.parameters]
        return cmp(x1, x2)
    def __str__(self):
        return self.__repr__()
    def __repr__(self):
        import operator
        ante_datas = self.ante_datas
        if len(ante_datas) == 1:
            ante_datas = ante_datas[0]
        x = [
            repr(self.name),
            repr(ante_datas),
            repr(self.cons_data),
            ]
        x = "%s(%s)" % (self.__class__.__name__, ", ".join(x))
        return x


class QueryModule(Module):
    pass


class ModuleDbSummary:
    # module_names    List of module names (strings).
    # name2module     Dictionary of module name (string) to Module object.
    # name2datatypes  Dict of module name to (ante Datatype, cons Datatype).
    # datatypes       List of Datatype objects.
    def __init__(
        self, module_names, name2module, name2datatypes, datatypes):
        self.module_names = module_names[:]
        self.name2module = name2module.copy()
        self.name2datatypes = name2datatypes.copy()
        self.datatypes = datatypes[:]
        

class Network:
    def __init__(self, nodes, transitions):
        # nodes should be a list of Data or Module objects.  Data
        # transition to Modules, and Modules transition to Data.
        
        # Make sure nodes are Data or Module objects.
        for n in nodes:
            assert isinstance(n, Data) or isinstance(n, Module)
        # Make sure transitions point to the right types of objects.
        for node_id, next_ids in transitions.iteritems():
            assert node_id >= 0 and node_id < len(nodes)
            for nid in next_ids:
                assert nid >= 0 and nid < len(nodes)
            for nid in next_ids:
                n1 = nodes[node_id]
                n2 = nodes[nid]
                if isinstance(n1, Data):
                    assert isinstance(n2, Module)
                else:
                    assert isinstance(n2, Data)
        
        self.nodes = nodes[:]
        self.transitions = transitions.copy()

    def __cmp__(self, other):
        if not isinstance(other, Network):
            return cmp(id(self), id(other))
        x1 = [self.nodes, self.transitions]
        x2 = [other.nodes, other.transitions]
        return cmp(x1, x2)

    def iterate(self, node_class=None):
        # Yield tuple of (node_id, next_node_ids).  node_class is the
        # class of the node of the network (either Data or Module).  If
        # provided, will only iterate over that kind of nodes.
        assert node_class in [Data, Module, QueryModule]
        for node_id, node in enumerate(self.nodes):
            if node_class and not isinstance(node, node_class):
                continue
            next_ids = self.transitions.get(node_id, [])
            yield node_id, next_ids

    def delete_node(self, node_id):
        """Delete a node and return a new Network object."""
        assert node_id < len(self.nodes)
        nodes = self.nodes[:]
        nodes.pop(node_id)

        transitions = {}
        for nid, next_ids in self.transitions.iteritems():
            if nid == node_id:
                continue
            elif nid > node_id:
                nid = nid - 1
            next_ids = [x for x in next_ids if x != node_id]
            for i in range(len(next_ids)):
                if next_ids[i] > node_id:
                    next_ids[i] = next_ids[i] - 1
            transitions[nid] = next_ids
        return Network(nodes, transitions)

    def delete_nodes(self, node_ids):
        network = Network(self.nodes, self.transitions)
        node_ids = reversed(sorted(node_ids))
        for nid in node_ids:
            network = network.delete_node(nid)
        return network

    def merge_nodes(self, node_ids):
        """node_ids is a list of the indexes of nodes.  Replace all
        these nodes with just a single one.  Returns a new Network
        object."""
        node_ids = sorted(node_ids)

        # Make sure no duplicate node_ids.
        for i in range(len(node_ids)-1):
            assert node_ids[i] != node_ids[i+1], "Duplicate node IDs."

        # Make sure nodes are the same type.
        for i in range(1, len(node_ids)):
            n1 = self.nodes[node_ids[0]]
            n2 = self.nodes[node_ids[i]]
            assert n1.__class__ == n2.__class__

        # Keep the first node, and delete the rest.

        # Make transitions to any node_ids point to the first one.
        node_id = node_ids[0]
        prev_ids = []
        for nid in node_ids[1:]:
            x = _backchain_to_ids(self, nid)
            prev_ids.extend(x)
        transitions = self.transitions.copy()
        for prev_id in prev_ids:
            x = transitions[prev_id]
            if node_id not in x:
                x = x + [node_id]
            transitions[prev_id] = x

        # Make the first node point to all the next_nodes of the other
        # node_ids.
        nid0 = node_ids[0]
        for nidi in node_ids[1:]:
            x = transitions.get(nid0, []) + transitions.get(nidi, [])
            x = sorted({}.fromkeys(x))
            transitions[nid0] = x

        merged = Network(self.nodes, transitions)
        merged = merged.delete_nodes(node_ids[1:])
        return merged


class _OptimizeNoCycles:
    # Methods:
    # optimize
    #
    # _find_cycles         Find all the cycles in a network.
    # _find_cycles_from_one_node
    # _find_cycles_from_all_nodes
    # _choose_breakpoints  Given a list of cycles, choose the best breakpoints.
    # _break_cycles        Break a list of cycles.
    def __init__(self):
        pass
    def optimize(self, network):
        # Do backwards chaining.  If I encounter a cycle, then break it.

        # Length of cycles:
        # 5     168,081   67%
        # 7      84,056   33%
        # 9-17      318    0%

        # Optimization.  Since may cycles are short, break the
        # 5-cycles first to speed up the search.
        cycles = self._find_cycles(network, 5)
        bad_transitions = self._choose_breakpoints(network, cycles)
        network = self._break_cycles(network, bad_transitions)

        cycles = self._find_cycles(network, 0)
        bad_transitions = self._choose_breakpoints(network, cycles)
        network = self._break_cycles(network, bad_transitions)

        return network

    def _find_cycles(self, network, max_path_length):
        assert max_path_length >= 0
        if max_path_length:
            cycles = self._find_cycles_from_all_nodes(network, max_path_length)
        else:
            cycles = self._find_cycles_from_one_node(
                network, 0, max_path_length)
        return cycles

    def _find_cycles_from_one_node(self, network, start_id, max_path_length):
        # Do a breadth first search and look for cycles.  Return a
        # list of cycles found, where each cycle is a list of
        # node_ids.

        nodeid2previds = _make_backchain_dict(network)

        cycles = []
        # list of (node_id, path (not including node_id))
        stack = [(start_id, [])]
        while stack:
            node_id, path = stack.pop(0)
            if max_path_length and len(path) > max_path_length:
                continue
            if node_id in path:
                # If this node_id is already in the path, then this is
                # a cycle.
                i = path.index(node_id)
                x = path[i:] + [node_id]
                cycles.append(x)
                continue
            path = path + [node_id]
            for prev_id in nodeid2previds.get(node_id, []):
                stack.append((prev_id, path))
        return cycles

    def _find_cycles_from_all_nodes(self, network, max_path_length):
        cycles = []
        for start_id in range(len(network.nodes)):
            x = self._find_cycles_from_one_node(
                network, start_id, max_path_length)
            cycles.extend(x)
        x = [tuple(x) for x in cycles]
        cycles = sorted({}.fromkeys(x))
        return cycles
    
    def _choose_breakpoints(self, network, cycles):
        # Return list of (node_id, next_id).  Count the number of
        # cycles each transition is in.  Break the transitions that
        # are in the most cycles.

        # Break at Module -> Data transitions.  Otherwise, will leave
        # both the Data and Module dangling.

        counts = {}   # (node_id, next_id) -> count
        for cycle in cycles:
            for i in range(len(cycle)-1):
                next_id, node_id = cycle[i], cycle[i+1]
                key = node_id, next_id
                if key not in counts:
                    counts[key] = 0
                counts[key] += 1

        bad_transitions = {}  # (node_id, next_id) -> 1
        for cycle in cycles:
            ## Break the cycle at the lowest node_id.
            #i = cycle.index(min(cycle))
            #assert i < len(cycle)-1

            # If this cycle is already broken, then ignore it.
            broken = False
            for i in range(len(cycle)-1):
                next_id, node_id = cycle[i], cycle[i+1]
                key = node_id, next_id
                if key in bad_transitions:
                    broken = True
            if broken:
                continue

            # Find the transition with the highest counts.  If there
            # are ties, use the key with lowest node_id.
            keys = []
            for i in range(len(cycle)-1):
                next_id, node_id = cycle[i], cycle[i+1]
                if not isinstance(network.nodes[node_id], Module):
                    continue
                x = node_id, next_id
                keys.append(x)
            schwartz = [(-counts[x], x) for x in keys]
            schwartz.sort()
            keys = [x[-1] for x in schwartz]
            bad_transitions[keys[0]] = 1
        return bad_transitions.keys()

    def _break_cycles(self, network, bad_transitions):
        import copy
        
        transitions = network.transitions.copy()
        for node_id, next_id in bad_transitions:
            x = transitions.get(node_id, [])
            assert next_id in x
            i = x.index(next_id)
            assert i >= 0
            x = x[:i] + x[i+1:]
            transitions[node_id] = x
        return Network(network.nodes, transitions)


class _OptimizeNoDuplicateData:
    def __init__(self):
        pass
    
    def optimize(self, network):
        # This could be made much more efficient with a better way of
        # finding duplicates.
        while True:
            duplicates = self.find_duplicate_data(network)
            if not duplicates:
                break
            network = network.merge_nodes(duplicates)
        return network
    
    def find_duplicate_data(self, network):
        # Return list of node_ids for Data objects that are
        # duplicated.  If no duplicates found, return an empty list.
        import itertools

        # Make a list of all pairs of Data objects.
        data_nodes = [
            node_id for (node_id, node) in enumerate(network.nodes)
            if isinstance(node, Data)]
        data_pairs = itertools.product(data_nodes, data_nodes)

        # Can optimize this by sorting.
        for (node_id1, node_id2) in data_pairs:
            if node_id1 == node_id2:
                continue
            data1, data2 = network.nodes[node_id1], network.nodes[node_id2]
            if data1 == data2:
                return [node_id1, node_id2]
        return []


class _OptimizeNoDuplicateModules:
    def __init__(self):
        pass
    
    def optimize(self, network):
        while 1:
            duplicates = self.find_duplicate_modules(network)
            if not duplicates:
                break
            network = network.merge_nodes(duplicates)
            assert isinstance(network, Network)
        return network
    
    def find_duplicate_modules(self, network):
        # Return list of module_ids for modules that are duplicated.  If
        # no duplicates found, return an empty list.

        # If the same data node points to two of the same module nodes,
        # then those modules are duplicated.
        duplicates = []
        for data_id, next_ids in network.iterate(node_class=Data):
            if len(next_ids) < 2:
                continue

            all_same = True
            for i in range(1, len(next_ids)):
                if network.nodes[next_ids[0]] != network.nodes[ next_ids[i]]:
                    all_same = False
                    break
            if all_same:
                duplicates = next_ids
                break
        return duplicates


class _OptimizeNoDanglingNodes:
    def __init__(self):
        pass
    def optimize(self, network):
        # Remove nodes that are extraneous to the network (e.g. don't
        # point to anything).  These situations can arise when
        # optimizing.
        while True:
            dangling = self.find_dangling_nodes(network)
            if not dangling:
                break
            network = network.delete_nodes(dangling)
        return network
    def find_dangling_nodes(self, network):
        dangling = []
        for (node_id, node) in enumerate(network.nodes):
            if self.is_dangling_node(network, node_id, node):
                dangling.append(node_id)
        return dangling
    def is_dangling_node(self, network, node_id, node):
        # 1.  Module nodes with no antecedents.
        # 2.  Module nodes with no consequents.
        # 3.  Data nodes (except for node 0) that don't point to any
        #     Modules.
        if isinstance(node, Module):
            if not network.transitions.get(node_id, []):
                return True
            prev_ids = _backchain_to_ids(network, node_id)
            if not prev_ids:
                return True
        elif isinstance(node, Data):
            if node_id != 0 and not network.transitions.get(node_id, []):
                return True
        else:
            raise AssertionError
        return False


class _OptimizeNoOverlappingData:
    # Some data objects may have overlapping attributes.
    # 1.  Data(SignalFile, format=['tdf', 'pcl', 'gct'], preprocess='rma')
    # 2.  Data(SignalFile, format=['tdf', 'res', 'pcl', 'jeffs', 'unknown',
    #       'xls'], preprocess='rma')
    #
    # Modules that point to 1 can generate 3 different formats.  Those
    # that point to 2 can generate 6.  To resolve this, split the Data
    # objects and rewire the Modules.
    # 3.  Data(SignalFile, format=['tdf', 'pcl'], preprocess='rma')
    # 4.  Data(SignalFile, format='gct', preprocess='rma')
    # 5.  Data(SignalFile, format=['res', 'jeffs', 'unknown', 'xls'],
    #       preprocess='rma')

    # Methods:
    # optimize
    # 
    # _find_overlapping_data
    # _find_overlapping_attribute
    # 
    # _fix_overlapping_data
    # _remove_atom_from_list
    # _remove_list_from_list
    # _split_list
    
    def __init__(self):
        pass

    def optimize(self, network):
        # Look for pairs of Data objects (Data_1, Data_2) where an
        # attribute is overlapping.
        import copy

        # Make a copy of the network now.  All changes to the network
        # will be done in place.
        network = copy.deepcopy(network)
        while True:
            x = self._find_overlapping_data(network)
            if not x:
                break
            node_id1, node_id2, attr_name = x
            self._fix_overlapping_data(network, node_id1, node_id2, attr_name)
            
        return network

    def _find_overlapping_data(self, network):
        # Return (node_id1, node_id2, name of overlapping attribute)
        # or None.
        for node_id1 in range(len(network.nodes)-1):
            node_1 = network.nodes[node_id1]
            if not isinstance(node_1, Data):
                continue
            for node_id2 in range(node_id1+1, len(network.nodes)):
                node_2 = network.nodes[node_id2]
                if not isinstance(node_2, Data):
                    continue
                attr = self._find_overlapping_attribute(node_1, node_2)
                if attr:
                    return node_id1, node_id2, attr
        return None

    def _find_overlapping_attribute(self, data1, data2):
        # Return the name of the single overlapping attribute or None.
        # 
        # data1 and data2 should be exactly the same, except for one
        # attribute with overlapping values.
        assert isinstance(data1, Data)
        assert isinstance(data2, Data)
        if data1.datatype != data2.datatype:
            return False
        
        # CASE    DATA1      DATA2     RESULT
        #   1    NOVALUE    NOVALUE    OK.
        #   2    NOVALUE    ANYATOM    Mismatch.
        #   3    NOVALUE      ATOM     Mismatch.
        #   4    NOVALUE      LIST     Mismatch.
        #   5    ANYATOM    NOVALUE    Mismatch.
        #   6    ANYATOM    ANYATOM    OK.
        #   7    ANYATOM      ATOM     Mismatch.
        #   8    ANYATOM      LIST     Mismatch.
        #   9      ATOM     NOVALUE    Mismatch.
        #  10      ATOM     ANYATOM    Mismatch.
        #  11      ATOM       ATOM     OK if ATOMs are equal.
        #  12      ATOM       LIST     OVERLAP if ATOM in LIST.
        #  13      LIST     NOVALUE    Mismatch.
        #  14      LIST     ANYATOM    Mismatch.
        #  15      LIST       ATOM     OVERLAP if ATOM in LIST.
        #  16      LIST       LIST     OVERLAP if LISTs have shared ATOMs.
        data1_attr = data1.attributes
        data2_attr = data2.attributes

        mismatch = False
        overlapping = []   # list of attribute names

        x = data1_attr.keys() + data2_attr.keys()
        all_attributes = sorted({}.fromkeys(x))
        for key in all_attributes:
            DATA1_VALUE = data1_attr.get(key)
            DATA2_VALUE = data2_attr.get(key)
            DATA1_TYPE = _get_attribute_type(data1_attr, key)
            DATA2_TYPE = _get_attribute_type(data2_attr, key)
            case = _assign_case_by_type(DATA1_TYPE, DATA2_TYPE)

            if case in [2, 3, 4, 5, 7, 8, 9, 10, 13, 14]:  # Mismatch
                mismatch = True
            elif case in [1, 6]:  # OK
                pass
            elif case == 11:
                if DATA1_VALUE != DATA2_VALUE:
                    mismatch = True
            elif case == 12:
                if len(DATA2_VALUE) == 1 and DATA1_VALUE == DATA2_VALUE[0]:
                    pass
                elif DATA1_VALUE in DATA2_VALUE:
                    overlapping.append(key)
                else:
                    mismatch = True
            elif case == 15:
                if len(DATA1_VALUE) == 1 and DATA2_VALUE == DATA1_VALUE[0]:
                    pass
                elif DATA2_VALUE in DATA1_VALUE:
                    overlapping.append(key)
                else:
                    mismatch = True
            elif case == 16:
                if sorted(DATA1_VALUE) == sorted(DATA2_VALUE):  # OK
                    pass
                elif _intersection(DATA1_VALUE, DATA2_VALUE):
                    overlapping.append(key)
                else:
                    mismatch = True
            else:
                raise AssertionError

        if mismatch:
            return None
        if len(overlapping) != 1:
            return None
        return overlapping[0]

    def _fix_overlapping_data(self, network, data_id1, data_id2, attr_name):
        # Changes network in place.

        data1 = network.nodes[data_id1]
        data2 = network.nodes[data_id2]
        DATA1_TYPE = _get_attribute_type(data1.attributes, attr_name)
        DATA2_TYPE = _get_attribute_type(data2.attributes, attr_name)
        DATA1_VALUE = data1.attributes[attr_name]
        DATA2_VALUE = data2.attributes[attr_name]
        if DATA1_TYPE is TYPE_LIST and DATA2_TYPE is TYPE_LIST:
            COMMON_VALUES = _intersection(DATA1_VALUE, DATA2_VALUE)

        if DATA1_TYPE is TYPE_ATOM:
            assert DATA2_TYPE is TYPE_LIST
            self._remove_atom_from_list(network, data_id2, data_id1, attr_name)
        elif DATA2_TYPE is TYPE_ATOM:
            assert DATA1_TYPE is TYPE_LIST
            self._remove_atom_from_list(network, data_id1, data_id2, attr_name)
        elif sorted(DATA1_VALUE) == sorted(COMMON_VALUES):
            self._remove_list_from_list(network, data_id2, data_id1, attr_name)
        elif sorted(DATA2_VALUE) == sorted(COMMON_VALUES):
            self._remove_list_from_list(network, data_id1, data_id2, attr_name)
        else:
            self._split_list(network, data_id1, data_id2, attr_name)

    def _remove_atom_from_list(self, network, data_id1, data_id2, attr_name):
        # Changes network in place.  data1 is a LIST and data2 is an
        # ATOM.  The values of data2 is in data1.

        data1 = network.nodes[data_id1]
        data2 = network.nodes[data_id2]
        DATA1_TYPE = _get_attribute_type(data1.attributes, attr_name)
        DATA2_TYPE = _get_attribute_type(data2.attributes, attr_name)
        DATA1_VALUE = data1.attributes[attr_name]
        DATA2_VALUE = data2.attributes[attr_name]
        assert DATA1_TYPE == TYPE_LIST and DATA2_TYPE == TYPE_ATOM
        assert DATA2_VALUE in DATA1_VALUE
        
        # Remove the ATOM from the LIST.
        DATA1_VALUE = DATA1_VALUE[:]
        i = DATA1_VALUE.index(DATA2_VALUE)
        DATA1_VALUE.pop(i)
        if len(DATA1_VALUE) == 1:
            DATA1_VALUE = DATA1_VALUE[0]
        data1.attributes[attr_name] = DATA1_VALUE

        # Every module that pointed to data_id1 should now also point
        # to data_id2.
        module_ids = _backchain_to_ids(network, data_id1)
        for node_id in module_ids:
            if data_id2 not in network.transitions[node_id]:
                network.transitions[node_id].append(data_id2)
                
        # Since some of the workflow from data1 is being rerouted to
        # data2, data2 should point to the children of data1.
        for node_id in network.transitions[data_id1]:
            if node_id not in network.transitions.get(data_id2, []):
                if data_id2 not in network.transitions:
                    network.transitions[data_id2] = []
                network.transitions[data_id2].append(node_id)


    def _remove_list_from_list(self, network, data_id1, data_id2, attr_name):
        # Changes network in place.  data1 and data2 are both a LISTs.
        # The values of data2 is a subset of data1.

        data1 = network.nodes[data_id1]
        data2 = network.nodes[data_id2]
        DATA1_TYPE = _get_attribute_type(data1.attributes, attr_name)
        DATA2_TYPE = _get_attribute_type(data2.attributes, attr_name)
        DATA1_VALUE = data1.attributes[attr_name]
        DATA2_VALUE = data2.attributes[attr_name]
        assert DATA1_TYPE == TYPE_LIST and DATA2_TYPE == TYPE_LIST
        assert sorted(DATA1_VALUE) != sorted(DATA2_VALUE)
        assert _is_subset(DATA2_VALUE, DATA1_VALUE)
        
        # Remove the ATOM from the LIST.
        DATA1_VALUE = DATA1_VALUE[:]
        for value in DATA2_VALUE:
            i = DATA1_VALUE.index(value)
            DATA1_VALUE.pop(i)
        if len(DATA1_VALUE) == 1:
            DATA1_VALUE = DATA1_VALUE[0]
        data1.attributes[attr_name] = DATA1_VALUE

        # Every module that pointed to data_id1 should now also point
        # to data_id2.
        module_ids = _backchain_to_ids(network, data_id1)
        for node_id in module_ids:
            if data_id2 not in network.transitions[node_id]:
                network.transitions[node_id].append(data_id2)

        # Since some of the workflow from data1 is being rerouted to
        # data2, data2 should point to the children of data1.
        for node_id in network.transitions[data_id1]:
            if node_id not in network.transitions.get(data_id2, []):
                if data_id2 not in network.transitions:
                    network.transitions[data_id2] = []
                network.transitions[data_id2].append(node_id)


    def _split_list(self, network, data_id1, data_id2, attr_name):
        # Changes network in place.  data1 and data2 are both a LISTs.

        data1 = network.nodes[data_id1]
        data2 = network.nodes[data_id2]
        DATA1_TYPE = _get_attribute_type(data1.attributes, attr_name)
        DATA2_TYPE = _get_attribute_type(data2.attributes, attr_name)
        DATA1_VALUE = data1.attributes[attr_name]
        DATA2_VALUE = data2.attributes[attr_name]
        assert DATA1_TYPE == TYPE_LIST and DATA2_TYPE == TYPE_LIST
        COMMON_VALUE = _intersection(DATA1_VALUE, DATA2_VALUE)
        assert len(COMMON_VALUE) < len(DATA1_VALUE)
        assert len(COMMON_VALUE) < len(DATA2_VALUE)

        # Remove the common values from the two LISTs.
        DATA1_VALUE = DATA1_VALUE[:]
        DATA2_VALUE = DATA2_VALUE[:]
        for value in COMMON_VALUE:
            i1 = DATA1_VALUE.index(value)
            i2 = DATA2_VALUE.index(value)
            DATA1_VALUE.pop(i1)
            DATA2_VALUE.pop(i2)
        if len(DATA1_VALUE) == 1:
            DATA1_VALUE = DATA1_VALUE[0]
        if len(DATA2_VALUE) == 1:
            DATA2_VALUE = DATA2_VALUE[0]
        data1.attributes[attr_name] = DATA1_VALUE
        data2.attributes[attr_name] = DATA2_VALUE

        # Make a new Data object that contains the common values.
        data3 = data1.copy()
        data3.attributes[attr_name] = COMMON_VALUE
        network.nodes.append(data3)
        data_id3 = len(network.nodes)-1
            
        # Every module that pointed to data_id1 or data_id2 should now
        # also point to data_id3.
        x1 = _backchain_to_ids(network, data_id1)
        x2 = _backchain_to_ids(network, data_id2)
        module_ids = x1 + x2
        for node_id in module_ids:
            if data_id3 not in network.transitions[node_id]:
                network.transitions[node_id].append(data_id3)

        # data_id3 should now point to everywhere that data_id1 and
        # data_id2 point to, if data_id3 is compatible with the
        # module.
        
        # XXX NOT IMPLEMENTED: MAKE SURE THIS IS A PROPER ANTECEDENT.
        x1 = network.transitions.get(data_id1, [])
        x2 = network.transitions.get(data_id2, [])
        all_modules = sorted({}.fromkeys(x1+x2))
        for module_id in all_modules:
            module = network.nodes[module_id]
            if _can_module_take_data(module, [data3]):
                if data_id3 not in network.transitions:
                    network.transitions[data_id3] = []
                network.transitions[data_id3].append(module_id)
        

class _OptimizeNoInvalidConsequents:
    # Fixing overlapping data can lead to a situation where a Module
    # points to Data that it can't generate.  E.g.
    # convert_signal_to_tdf -> format=["tdf", "pcl"]
    #   changed to:
    # convert_signal_to_tdf -> format=["tdf"]
    # convert_signal_to_tdf -> format=["pcl"]
    #
    # Since one of these is now incorrect, remove it.
    def __init__(self):
        pass
    def optimize(self, network):
        import copy

        bad_transitions = {}  # (node_id, next_id) -> 1
        for (node_id, next_ids) in network.iterate(node_class=Module):
            module = network.nodes[node_id]
            for next_id in next_ids:
                node = network.nodes[next_id]
                assert isinstance(node, Data)
                if not _can_module_produce_data(module, node):
                    bad_transitions[(node_id, next_id)] = 1

        network = copy.deepcopy(network)
        for node_id, next_id in bad_transitions:
            x = network.transitions.get(node_id, [])
            assert next_id in x
            i = x.index(next_id)
            assert i >= 0
            x.pop(i)
            network.transitions[node_id] = x
        return network
    

## class _OptimizeMergeSimilarData:
##     def __init__(self):
##         pass
##     def optimize(self, network):
##         # Look for pairs of Data objects (Data_1, Data_2) where:
##         # o Data_1 is more general than Data_2.
##         # o Data_2 has a subset of the parents as Data_1.
##         # o If Data_1 and Data_2 have the same parents, then Data_1
##         #   should have a lower node_id.
##         #
##         # Move overlapping attributes from Data_2 to Data_1.  (e.g. If
##         # Data_1 and Data_2 both take PCL format, remove PCL format
##         # from Data_2).
##         import itertools
##         import copy

##         # Make a list of all pairs of Data objects.
##         data_pairs = self.list_data_siblings(network)
        
##         similar = []
##         for (node_id1, node_id2) in data_pairs:
##             assert node_id1 != node_id2
##             data1, data2 = network.nodes[node_id1], network.nodes[node_id2]
##             # Optimization: check this datatype here to reduce
##             # function calls to is_data_compatible.
##             if data1.datatype != data2.datatype:
##                 continue
##             if not self.is_data_compatible(data1, data2):
##                 continue
##             if not self.is_topology_compatible(network, node_id1, node_id2):
##                 continue
##             similar.append((node_id1, node_id2))
##         data_pairs = similar

##         # For each of the pairs whose lists have overlapping options,
##         # remove the overlapping options from data2.
##         # For each of the pairs where data1 has a LIST and data2 has a
##         # ATOM in the LIST, merge data1 and data2.
##         merge_pairs = []
##         network = copy.deepcopy(network)
##         for (node_id1, node_id2) in data_pairs:
##             data1, data2 = network.nodes[node_id1], network.nodes[node_id2]
##             data1_attr = data1.attributes
##             data2_attr = data2.attributes

##             attributes = data2.attributes.copy()
##             for key in data1.attributes:
##                 DATA1_VALUE = data1_attr.get(key)
##                 DATA2_VALUE = data2_attr.get(key)
##                 DATA1_TYPE = _get_attribute_type(data1_attr, key)
##                 DATA2_TYPE = _get_attribute_type(data2_attr, key)

##                 if DATA1_TYPE == TYPE_LIST and DATA2_TYPE == TYPE_ATOM:
##                     if DATA2_VALUE in DATA1_VALUE:
##                         merge_pairs.append((node_id1, node_id2))
##                 elif DATA1_TYPE == TYPE_LIST and DATA2_TYPE == TYPE_LIST:
##                     if sorted(DATA1_VALUE) != sorted(DATA2_VALUE):
##                         DATA2_VALUE = [
##                             x for x in DATA2_VALUE if x not in DATA1_VALUE]
                        
##                         # If DATA2_VALUE is subset of DATA1_VALUE,
##                         # then merge these nodes.
##                         if not DATA2_VALUE:
##                             merge_pairs.append((node_id1, node_id2))
##                         else:
##                             attributes[key] = DATA2_VALUE
##             data2 = Data(data2.datatype, attributes)
##             network.nodes[node_id2] = data2
            
##         while merge_pairs:
##             node_id1, node_id2 = merge_pairs.pop(0)
##             network = network.merge_nodes([node_id1, node_id2])
##             for i in range(len(merge_pairs)):
##                 nid1, nid2 = merge_pairs[i]
##                 assert nid1 != node_id2 and nid2 != node_id2
##                 if nid1 > node_id2:
##                     nid1 -= 1
##                 if nid2 > node_id2:
##                     nid2 -= 1
##                 merge_pairs[i] = nid1, nid2
##         return network

##     def list_data_siblings(self, network):
##         # Return list of (node_id1, node_id2) where node_id1 and
##         # node_id2 have the same parents.  Will give node_id1 and
##         # node_id2 in both orders.
##         import itertools

##         siblings = {}
##         has_parents = {}
##         for node_id, next_ids in network.transitions.iteritems():
##             for nid in next_ids:
##                 has_parents[nid] = 1
##             # Make sure the parent is a Module.  Children should be
##             # Data objects.
##             if not isinstance(network.nodes[node_id], Module):
##                 continue
##             for id1, id2 in itertools.product(next_ids, next_ids):
##                 siblings[(id1, id2)] = 1
##         # Also list nodes with no parents.
##         no_parents = []
##         for node_id in range(len(network.nodes)):
##             if node_id in has_parents:
##                 continue
##             if not isinstance(network.nodes[node_id], Data):
##                 continue
##             no_parents.append(node_id)
##         for id1, id2 in itertools.product(no_parents, no_parents):
##             siblings[(id1, id2)] = 1

##         # Filter out nodes that are not different.
##         siblings = [x for x in sorted(siblings) if x[0] != x[1]]
##         return siblings
    

##     def is_data_compatible(self, data1, data2):
##         # data1 should be more general then data2.
##         assert isinstance(data1, Data)
##         assert isinstance(data2, Data)
##         if data1.datatype != data2.datatype:
##             return False
        
##         # CASE    DATA1      DATA2     RESULT
##         #   1    NOVALUE    NOVALUE    OK.
##         #   2    NOVALUE    ANYATOM    No.
##         #   3    NOVALUE      ATOM     No.
##         #   4    NOVALUE      LIST     No.
##         #   5    ANYATOM    NOVALUE    No.  Not sure about this one.
##         #   6    ANYATOM    ANYATOM    OK.
##         #   7    ANYATOM      ATOM     OK.
##         #   8    ANYATOM      LIST     No.
##         #   9      ATOM     NOVALUE    No.  Not sure.
##         #  10      ATOM     ANYATOM    No.
##         #  11      ATOM       ATOM     OK if ATOMs are equal.
##         #  12      ATOM       LIST     No.
##         #  13      LIST     NOVALUE    No.  Not sure.
##         #  14      LIST     ANYATOM    No.
##         #  15      LIST       ATOM     OK if ATOM in LIST.
##         #  16      LIST       LIST     OK if DATA2 LIST overlaps with DATA1.
##         #
##         # For case 16, DATA2 LIST doesn't have to be a subset of DATA1
##         # LIST, because we will remove the overlapping elements.
##         data1_attr = data1.attributes
##         data2_attr = data2.attributes

##         x = data1_attr.keys() + data2_attr.keys()
##         all_attributes = sorted({}.fromkeys(x))
##         compatible = True
##         for key in all_attributes:
##             DATA1_VALUE = data1_attr.get(key)
##             DATA2_VALUE = data2_attr.get(key)
##             DATA1_TYPE = _get_attribute_type(data1_attr, key)
##             DATA2_TYPE = _get_attribute_type(data2_attr, key)
##             case = _assign_case_by_type(DATA1_TYPE, DATA2_TYPE)

##             if case in [2, 3, 4, 5, 8, 9, 10, 12, 13, 14]:  # No
##                 compatible = False
##             elif case in [1, 6, 7]:  # OK
##                 pass
##             elif case == 11:
##                 if DATA1_VALUE != DATA2_VALUE:
##                     compatible = False
##             elif case == 15:
##                 if DATA2_VALUE not in DATA1_VALUE:
##                     compatible = False
##             elif case == 16:
##                 if not _intersection(DATA1_VALUE, DATA2_VALUE):
##                     compatible = False
##             else:
##                 raise AssertionError

##         return compatible


##     def is_topology_compatible(self, network, node_id1, node_id2):
##         # The parents of node_id2 should be a subset of the parents of
##         # node_id1.  If the parents are the same, then node_id1 should
##         # have a lower node_id than node_id2.
##         prev_ids1 = _backchain_to_ids(network, node_id1)
##         prev_ids2 = _backchain_to_ids(network, node_id2)
##         if sorted(prev_ids1) == sorted(prev_ids2):
##             return node_id1 < node_id2
##         return _is_subset(prev_ids2, prev_ids1)


## class _OptimizeNoAmbiguousPaths:
##     def __init__(self):
##         pass
##     def optimize(self, network):
##         # If a Module points to more than one of the same Data
##         # objects, remove the link to one of them.
##         # - If they're identical, keep the one with the lower node_id.
##         # - Otherwise, keep the one with the more general attributes.
##         #
##         # E.g. check_for_log -> Data(SignalFile, format="tdf")
##         #                    -> Data(SignalFile, format=["tdf", "pcl"])
##         import copy
##         import itertools

##         jobs = []  # node_id, data_id1, data_id2.  data_id1 < data_id2
##         for node_id, next_ids in network.iterate(node_class=Module):
##             for i in range(len(next_ids)-1):
##                 for j in range(i+1, len(next_ids)):
##                     data_id1 = next_ids[i]
##                     data_id2 = next_ids[j]
##                     x = node_id, data_id1, data_id2
##                     jobs.append(x)

##         remove_links = {}  # node_id -> data_id
##         for x in jobs:
##             node_id, data_id1, data_id2 = x
##             data1, data2 = network.nodes[data_id1], network.nodes[data_id2]

##             # If I've already removed one of these links for this
##             # module, then these are no longer ambiguous.
##             if remove_links.get(node_id) in [data_id1, data_id2]:
##                 pass
##             elif data1.datatype != data2.datatype:
##                 pass
##             elif data1 == data2:
##                 remove_links[node_id] = max(data_id1, data_id2)
##             elif self.is_more_general(data1, data2):
##                 remove_links[node_id] = data_id2
##             elif self.is_more_general(data2, data1):
##                 remove_links[node_id] = data_id1

##         if remove_links:
##             network = copy.deepcopy(network)
##         for node_id, data_id in remove_links.iteritems():
##             x = network.transitions[node_id]
##             i = x.index(data_id)
##             x.pop(i)

##         return network


##     def is_more_general(self, data1, data2):
##         # Is data1 more general then data2.
##         assert isinstance(data1, Data)
##         assert isinstance(data2, Data)
##         if data1.datatype != data2.datatype:
##             return False
        
##         # CASE    DATA1      DATA2     RESULT
##         #   1    NOVALUE    NOVALUE    OK.
##         #   2    NOVALUE    ANYATOM    No.
##         #   3    NOVALUE      ATOM     No.
##         #   4    NOVALUE      LIST     No.
##         #   5    ANYATOM    NOVALUE    No.  Not sure about this one.
##         #   6    ANYATOM    ANYATOM    OK.
##         #   7    ANYATOM      ATOM     OK.
##         #   8    ANYATOM      LIST     No.
##         #   9      ATOM     NOVALUE    No.  Not sure.
##         #  10      ATOM     ANYATOM    No.
##         #  11      ATOM       ATOM     OK if ATOMs are equal.
##         #  12      ATOM       LIST     No.
##         #  13      LIST     NOVALUE    No.  Not sure.
##         #  14      LIST     ANYATOM    No.
##         #  15      LIST       ATOM     OK if ATOM in LIST.
##         #  16      LIST       LIST     OK if DATA2 LIST is subset of DATA1.
##         data1_attr = data1.attributes
##         data2_attr = data2.attributes

##         x = data1_attr.keys() + data2_attr.keys()
##         all_attributes = sorted({}.fromkeys(x))
##         more_general = True
##         for key in all_attributes:
##             DATA1_VALUE = data1_attr.get(key)
##             DATA2_VALUE = data2_attr.get(key)
##             DATA1_TYPE = _get_attribute_type(data1_attr, key)
##             DATA2_TYPE = _get_attribute_type(data2_attr, key)
##             case = _assign_case_by_type(DATA1_TYPE, DATA2_TYPE)

##             if case in [2, 3, 4, 5, 8, 9, 10, 12, 13, 14]:  # No
##                 more_general = False
##             elif case in [1, 6, 7]:  # OK
##                 pass
##             elif case == 11:
##                 if DATA1_VALUE != DATA2_VALUE:
##                     more_general = False
##             elif case == 15:
##                 if DATA2_VALUE not in DATA1_VALUE:
##                     more_general = False
##             elif case == 16:
##                 if not _is_subset(DATA2_VALUE, DATA1_VALUE):
##                     more_general = False
##             else:
##                 raise AssertionError

##         return more_general


## class _OptimizeReconvert:
##     def __init__(self):
##         pass
    
##     def optimize(self, network):
##         # Look for topology:
##         # Data_1 -> Module_2 -> Data_3 -> Module_4 -> Data_5
##         # Data_1 is compatible with Data_5.
##         #
##         # Delete Data_1.  Can happen when a SignalFile's format gets
##         # converted to another format, and then recoverted back to the
##         # original one.
##         topologies = self.extract_topology(network)

##         # Data_1 and Data_5 must be compatible.
##         good = []
##         for topology in topologies:
##             assert len(topology) == 5
##             node_id1, node_id5 = topology[0], topology[-1]
##             data1, data5 = network.nodes[node_id1], network.nodes[node_id5]
##             if not self.is_data_compatible(data1, data5):
##                 continue
##             if not self.is_topology_compatible(network, node_id1, node_id5):
##                 continue
##             good.append(topology)
##         topologies = good

##         # The head nodes of the topologies are redundant.  Delete them.
##         node_ids = [x[0] for x in topologies]
##         network = network.delete_nodes(node_ids)

##         # Delete any dangling modules.
##         network = _delete_dangling_modules(network)
##         return network
    
##     def extract_topology(self, network):
##         # Pull out all the nodes that fit the required topology.  (5 node
##         # linear.)

##         data_nodes = [
##             node_id for (node_id, node) in enumerate(network.nodes)
##             if isinstance(node, Data)]

##         # (node_id1, node_id2, node_id3, node_id4, node_id5) -> 1
##         topologies = {}
        
##         stack = []  # list of (list of topologies)
##         for node_id in data_nodes:
##             stack.append([node_id])
##         while stack:
##             topology = stack.pop()
##             if len(topology) >= 5:
##                 topologies[tuple(topology)] = 1
##                 continue
##             for next_id in network.transitions.get(topology[-1], []):
##                 stack.append(topology + [next_id])
##         return sorted(topologies)

##     def is_data_compatible(self, data1, data5):
##         assert isinstance(data1, Data)
##         assert isinstance(data5, Data)
##         if data1.datatype != data5.datatype:
##             return False

##         # Upstream (data1) should be more general than downstream (data5).
##         # Since we will be removing data1 and replacing with data5, we can
##         # replace with a more specific data (because it can definitely be
##         # generated by the upstream modules).  XXX THIS LOGIC IS
##         # WRONG.  UPSTREAM MAY ONLY BE ABLE TO GENERATE ONE OF THESE!
##         #
##         # CASE    DATA1      DATA5     RESULT
##         #   1    NOVALUE    NOVALUE    OK.
##         #   2    NOVALUE    ANYATOM    No.
##         #   3    NOVALUE      ATOM     No.
##         #   4    NOVALUE      LIST     No.
##         #   5    ANYATOM    NOVALUE    No.  Not sure about this one.
##         #   6    ANYATOM    ANYATOM    OK.
##         #   7    ANYATOM      ATOM     OK.
##         #   8    ANYATOM      LIST     No.
##         #   9      ATOM     NOVALUE    No.  Not sure.
##         #  10      ATOM     ANYATOM    No.
##         #  11      ATOM       ATOM     OK if ATOMs equal.
##         #  12      ATOM       LIST     No.
##         #  13      LIST     NOVALUE    No.  Not sure.
##         #  14      LIST     ANYATOM    No.
##         #  15      LIST       ATOM     OK if ATOM in LIST.
##         #  16      LIST       LIST     OK if DATA5 LIST is subset of DATA1 LIST.
##         data1_attr = data1.attributes
##         data5_attr = data5.attributes

##         x = data1_attr.keys() + data5_attr.keys()
##         all_attributes = sorted({}.fromkeys(x))
##         compatible = True
##         for key in all_attributes:
##             DATA1_VALUE = data1_attr.get(key)
##             DATA5_VALUE = data5_attr.get(key)
##             DATA1_TYPE = _get_attribute_type(data1_attr, key)
##             DATA5_TYPE = _get_attribute_type(data5_attr, key)

##             case = _assign_case_by_type(DATA1_TYPE, DATA5_TYPE)

##             if case in [2, 3, 4, 5, 8, 9, 10, 12, 13, 14]:  # No
##                 compatible = False
##             elif case in [1, 6, 7]:  # OK
##                 pass
##             elif case == 11:
##                 if DATA1_VALUE != DATA5_VALUE:
##                     compatible = False
##             elif case == 15:
##                 if not DATA5_VALUE in DATA1_VALUE:
##                     compatible = False
##             elif case == 16:
##                 if not _is_subset(DATA5_VALUE, DATA1_VALUE):
##                     compatible = False
##             else:
##                 raise AssertionError

##         return compatible
    
##     def is_topology_compatible(self, network, node_id1, node_id5):
##         # The nodes that point to data1 should be a subset of the nodes
##         # that point to data5.
##         prev_ids1 = _backchain_to_ids(network, node_id1)
##         prev_ids5 = _backchain_to_ids(network, node_id5)
##         return _is_subset(prev_ids1, prev_ids5)


def backchain(moduledb, goal_datatype, goal_attributes):
    # Return a Network object.
    assert isinstance(goal_datatype, DataType)
    assert type(goal_attributes) is type({})

    goal_data = _make_goal(goal_datatype, goal_attributes)
    
    nodes = []        # list of Data or Module objects.
    transitions = {}  # list of index -> list of indexes

    MAX_NETWORK_SIZE = 4096
    nodes.append(goal_data)
    stack = [0]
    seen = {}
    while stack:
        assert len(nodes) < MAX_NETWORK_SIZE, "network too large"

        # Pop the next node off the stack.
        node_id = stack.pop()
        assert node_id < len(nodes)
        node = nodes[node_id]

        # If I've already seen this node, then don't process it again.
        if node_id in seen:
            continue
        seen[node_id] = 1

        if isinstance(node, Data):
            # Backwards chain to the previous module.
            modules = _backchain_to_modules(moduledb, node)
            for m in modules:
                nodes.append(m)
                m_id = len(nodes) - 1
                stack.append(m_id)
                transitions[m_id] = transitions.get(m_id, [])
                transitions[m_id].append(node_id)
        elif isinstance(node, Module):
            cons_id = transitions[node_id][0]
            cons = nodes[cons_id]
            for ante_num in range(len(node.ante_datas)):
                d = _backchain_to_antecedent(
                    node, ante_num, cons, goal_attributes)
                d_id = _find_data_node(nodes, d)
                if d_id == -1:
                    nodes.append(d)
                    d_id = len(nodes)-1
                stack.append(d_id)
                transitions[d_id] = transitions.get(d_id, [])
                transitions[d_id].append(node_id)
        else:
            raise AssertionError, "Unknown node type: %s" % node

    # Remove the duplicates from transitions.
    for nid in transitions:
        next_ids = sorted({}.fromkeys(transitions[nid]))
        transitions[nid] = next_ids
        
    network = Network(nodes, transitions)
    return network


def optimize_network(network):
    optimizers = [
        _OptimizeNoCycles(),
        _OptimizeNoDanglingNodes(),
        _OptimizeNoDuplicateModules(),
        _OptimizeNoDuplicateData(),
        _OptimizeNoOverlappingData(),
        _OptimizeNoInvalidConsequents(),

        # OBSOLETE?
        #_OptimizeMergeSimilarData(),
        #_OptimizeNoAmbiguousPaths(),
        ]

    old_network = None
    while old_network != network:
        old_network = network
        for opt in optimizers:
            network = opt.optimize(network)

    return network

def prune_network_by_start(network, start_data):
    # start_data may be a single Data object or a list of Data
    # objects.  DataTypes are also allowed in lieu of Data objects.
    import operator

    start_datas = start_data
    if not operator.isSequenceType(start_data):
        start_datas = [start_data]
    for i, x in enumerate(start_datas):
        if isinstance(x, DataType):
            x = x()  # convert to Data
        assert isinstance(x, Data)
        start_datas[i] = x
    
    # Look for the nodes that are compatible with start_data.
    node_ids = []  # list of node_ids.
    for node_id, next_ids in network.iterate(node_class=Data):
        # See if this node is compatible with any of the start nodes.
        x = [x for x in start_datas
             if _is_compatible_with_start(network.nodes[node_id], x)]
        if x:
            node_ids.append(node_id)

    # Strategy:
    # 1.  Include all nodes that can reach both a start and end node.
    # 2.  Remove modules that are missing any antecedents.
    # 3.  Repeat steps 1-2 until convergence.

    good_ids = {}.fromkeys(range(len(network.nodes)))

    while good_ids:
        # If any of the nodes can't reach both the start and the end,
        # then delete it.
        delete_ids = {}
        for node_id in good_ids:
            good_by_bc = _can_reach_by_bc(network, node_id, good_ids)
            good_by_fc = _can_reach_by_fc(network, node_id, good_ids)
            # If it can't reach the goal, then delete it.
            if 0 not in good_by_fc:
                delete_ids[node_id] = 1
            # If it can't reach any starts, then delete it.
            x = [x for x in node_ids if x in good_by_bc]
            if not x:
                delete_ids[node_id] = 1
            
        # If a module requires multiple inputs, make sure each of the
        # inputs are in the network.  If not, remove the module.
        for node_id in good_ids:
            node = network.nodes[node_id]
            if not isinstance(node, Module):
                continue
            assert len(node.ante_datas) > 0
            if len(node.ante_datas) <= 1:
                continue
            ante_ids = _backchain_to_ids(network, node_id)
            nid = [x for x in ante_ids if x in good_ids]
            if len(nid) != len(ante_ids):
                delete_ids[node_id] = 1

        for node_id in delete_ids:
            del good_ids[node_id]
        if not delete_ids:
            break
        
    # Delete all the IDs that aren't in good_ids.
    bad_ids = [x for x in range(len(network.nodes)) if x not in good_ids]
    network = network.delete_nodes(bad_ids)
    return network


def prune_network_by_internal(network, internal_data):
    if isinstance(internal_data, DataType):
        internal_data = internal_data()  # convert to Data
    assert isinstance(internal_data, Data)
    
    # Look for the nodes that are compatible with internal_data.
    node_ids = []  # list of node_ids.
    for node_id, next_ids in network.iterate(node_class=Data):
        if _is_compatible_with_internal(network.nodes[node_id], internal_data):
            node_ids.append(node_id)

    # For each of these node_ids, do forward chaining to find all
    # nodes that these ones can connect to.
    fc_ids = {}
    stack = node_ids[:]
    while stack:
        node_id = stack.pop(0)
        if node_id in fc_ids:
            continue
        fc_ids[node_id] = 1
        x = network.transitions.get(node_id, [])
        stack.extend(x)

    # For each of the ids found by forward chaining, do backward
    # chaining to find all the ones that it can start from.
    bc_ids = {}
    stack = node_ids[:]
    while stack:
        node_id = stack.pop(0)
        if node_id in bc_ids:
            continue
        bc_ids[node_id] = 1
        x = _backchain_to_ids(network, node_id)
        stack.extend(x)

    # The good IDs are all the ones found by either forward or
    # backward chaining.
    good_ids = fc_ids.copy()
    good_ids.update(bc_ids)

    # Delete all the IDs that aren't in good_ids.
    bad_ids = [x for x in range(len(network.nodes)) if x not in good_ids]
    network = network.delete_nodes(bad_ids)
    return network


def summarize_moduledb(moduledb):
    """Take a list of Modules and return a ModuleDbSummary object."""
    name2module = {}   # module_name -> Module
    for module in moduledb:
        assert module.name not in name2module
        name2module[module.name] = module
    module_names = sorted(name2module)

    # module_name -> (list of ante Datatypes, cons Datatype)
    name2datatypes = {}
    for name, module in name2module.iteritems():
        ante_datatypes = [x.datatype for x in module.ante_datas]
        cons_datatype = module.cons_data.datatype
        name2datatypes[name] = ante_datatypes, cons_datatype

    # list of all Data objects in moduledb.
    all_data = []
    for name, module in name2module.iteritems():
        for data in module.ante_datas + [module.cons_data]:
            if data not in all_data:
                all_data.append(data)

    datatype2data = {}   # Datatype -> list of Data
    for data in all_data:
        if data.datatype not in datatype2data:
            datatype2data[data.datatype] = []
        datatype2data[data.datatype].append(data)
    datatypes = sorted(datatype2data)

    x = ModuleDbSummary(module_names, name2module, name2datatypes, datatypes)
    return x


def print_modules(moduledb):
    summary = summarize_moduledb(moduledb)

    for name in summary.module_names:
        ante_datatypes, cons_datatype = summary.name2datatypes[name]
        ante_names = [x.name for x in ante_datatypes]
        x = ", ".join(ante_names)
        x = name, x, cons_datatype.name
        print "\t".join(x)

    for datatype in summary.datatypes:
        print datatype.name
        for attr in sorted(datatype.attributes):
            values = datatype.attributes[attr]
            if type(values) is type(""):
                values = [values]
            print "  %s : %s" % (attr, ", ".join(map(str, values)))
        print


def _make_goal(datatype, attributes):
    # Make a Data object that can represent a goal.  Use the
    # attributes provided by the user that are appropriate for this
    # datatype.  If anything is not given, use the defaults.
    defaults = datatype.get_defaults()
    attrs = {}
    for key in datatype.attributes:
        attrs[key] = attributes.get(key, defaults[key])
    return Data(datatype, attrs)


def _backchain_to_modules(moduledb, data):
    # Return list of modules that that can generate a consequent that
    # is compatible with data.  The modules will be sorted in
    # decreasing order of the number of attributes that are
    # compatible.

    matches = []  # list of (module, num compatible attributes)
    for module in moduledb:
        num_attributes = _can_module_produce_data(module, data)
        if not num_attributes:
            continue
        x = module, num_attributes
        matches.append(x)

    # Sort by decreasing number of attributes provided.
    matches.sort(key=lambda x: -x[-1])
    modules = [x[0] for x in matches]
    return modules


def _backchain_to_antecedent(module, ante_num, data, goal_attributes):
    # Return the Data object that is the antecedent of the module and
    # the consequent (data).  goal_attributes are attributes provided
    # by the user for the goal.  This is necessary because some of
    # these attributes may be relevant to new data types.  E.g. The
    # goal datatype is a signal_file, but some of the attributes are
    # relevant for illu_folder.
    assert ante_num < len(module.ante_datas)

    # Back chain the attributes.  Possibilities:
    #
    # DATA_VALUE  Value of attribute in data.
    # ANTE_VALUE  Value of attribute in antecedent.
    # CONS_VALUE  Value of attribute in consequent.
    # ANTE_TYPE   Type of attribute in antecedent.
    # CONS_TYPE   Type of attribute in consequent.
    #
    # CASE  ANTE_TYPE  CONS_TYPE   RESULT
    #   1    NOVALUE    NOVALUE    DATA_VALUE.  Irrelevant for module.
    #   2    NOVALUE    ANYATOM    Ignore (NOVALUE).
    #   3    NOVALUE      ATOM     Ignore (NOVALUE).
    #   4    NOVALUE      LIST     Ignore (NOVALUE).
    #   5    ANYATOM    NOVALUE    NotImplementedError. When does this happen?
    #   6    ANYATOM    ANYATOM    NotImplementedError. When does this happen?
    #   7    ANYATOM      ATOM     NotImplementedError. When does this happen?
    #   8    ANYATOM      LIST     NotImplementedError. When does this happen?
    #   9      ATOM     NOVALUE    ANTE_VALUE.  cel_version="v3_4"
    #  10      ATOM     ANYATOM    ANTE_VALUE.
    #  11      ATOM       ATOM     ANTE_VALUE.  logged="no"->"yes"
    #  12      ATOM       LIST     ANTE_VALUE.
    #  13      LIST     NOVALUE    ANTE_VALUE.
    #  14      LIST     ANYATOM    ANTE_VALUE.
    #  15      LIST       ATOM     ANTE_VALUE.
    #  16      LIST       LIST     DATA_VALUE or ANTE_VALUE (see below).
    data_attr = data.attributes
    ante_attr = module.ante_datas[ante_num].attributes
    cons_attr = module.cons_data.attributes

    x = data_attr.keys() + ante_attr.keys() + cons_attr.keys()
    all_attributes = sorted({}.fromkeys(x))

    attributes = {}
    for key in all_attributes:
        DATA_VALUE = data_attr.get(key)
        ANTE_VALUE = ante_attr.get(key)
        CONS_VALUE = cons_attr.get(key)
        DATA_TYPE = _get_attribute_type(data_attr, key)
        ANTE_TYPE = _get_attribute_type(ante_attr, key)
        CONS_TYPE = _get_attribute_type(cons_attr, key)
        CASE = _assign_case_by_type(ANTE_TYPE, CONS_TYPE)

        if CASE == 1:
            assert DATA_TYPE is not TYPE_NOVALUE
            attributes[key] = DATA_VALUE
        elif CASE in [2, 3, 4]:
            pass
        elif CASE in [5, 6, 7, 8]:
            raise NotImplementedError
        elif CASE in [9, 10, 11, 12, 13, 14, 15]:
            attributes[key] = ANTE_VALUE
        elif CASE == 16:
            # This can happen if:
            # 1.  The module doesn't change the value.
            # 2.  The module can generate multiple values to fit the
            #     next Data object.
            # If it's the first case, use DATA_VALUE, otherwise use
            # ANTE_VALUE.
            assert DATA_TYPE in [TYPE_ATOM, TYPE_LIST]
            if DATA_TYPE == TYPE_ATOM:
                assert DATA_VALUE in CONS_VALUE
            else:
                assert sorted(DATA_VALUE) == sorted(CONS_VALUE)
            
            # Case 1.
            if sorted(ANTE_VALUE) == sorted(CONS_VALUE):
                # DATA_VALUE is a subset of CONS_VALUE.
                attributes[key] = DATA_VALUE
            # Case 2.
            else:
                attributes[key] = ANTE_VALUE
        else:
            raise AssertionError

    # If we are converting to a different data type, then add the
    # relevant attributes from the goal_attributes.
    datatype = module.ante_datas[ante_num].datatype
    if module.ante_datas[ante_num].datatype == module.cons_data.datatype:
        data = Data(datatype, attributes)
    else:
        attrs = goal_attributes
        attrs.update(attributes)
        data = _make_goal(datatype, attrs)

    return data


def _backchain_to_ids(network, node_id):
    # Return a list of IDs that point to this node_id.
    assert node_id < len(network.nodes)
    ids = {}
    for nid, next_ids in network.transitions.iteritems():
        if node_id in next_ids:
            ids[nid] = 1
    return sorted(ids)


def _make_backchain_dict(network):
    # Return a dictionary of node_id -> prev_node_ids
    nodeid2previds = {}
    for prev_id, node_ids in network.transitions.iteritems():
        for node_id in node_ids:
            if node_id not in nodeid2previds:
                nodeid2previds[node_id] = []
            nodeid2previds[node_id].append(prev_id)
    return nodeid2previds


def _can_module_produce_data(module, data):
    # Return the number of attributes in data that this module can
    # generate.  Look for attributes in consequent that match
    # attributes in data.  0 means that module can not produce this
    # data object.
    
    # A module can produce this data if:
    # - The consequent has an attribute value that matches the value
    #   of the attribute in the data.
    # - The consequents and antecedents have no values, and their data
    #   types are different.
    #   e.g. download_geo_GSEID  gseid -> expression_files  (no attributes)
    #
    # A module is incompatible if:
    # - None of the attribute values are the same.
    # - One or more of the attribute values conflict.

    # If this module doesn't produce the same data type, then it can't
    # produce this data object.
    if module.cons_data.datatype != data.datatype:
        return 0

    # Is a converting module if none of the antecedents are the same
    # datatype as the consequent.  Otherwise, is a non-converting
    # module.
    #if len(module.ante_datas) == 1 and \
    #       module.ante_datas[0].datatype == module.cons_data.datatype:
    x = [x for x in module.ante_datas
         if x.datatype == module.cons_data.datatype]
    if x:
        return _can_nonconverting_module_produce_data(module, data)
    return _can_converting_module_produce_data(module, data)
    

def _can_converting_module_produce_data(module, data):
    p = _print_nothing
    #p = _print_string
    
    p("Checking if module %s can produce data." % module.name)

    data_attr = data.attributes
    cons_attr = module.cons_data.attributes

    # If there are no attributes to match, then this matches by
    # default.
    # E.g. extract_CEL_files converts ExpressionFiles to GSEID.

    if not cons_attr and not data_attr:
        p("Match by no attributes.")
        return 1

    # Fill in default values for the consequent.
    defaults = module.cons_data.datatype.get_defaults()
    cons_attr = cons_attr.copy()
    for key in module.cons_data.datatype.attributes:
        if key not in cons_attr:
            cons_attr[key] = defaults[key]


    # CASE  CONS_TYPE  DATA_TYPE   RESULT
    #   1    NOVALUE    NOVALUE    ERROR.
    #   2    NOVALUE    ANYATOM    ERROR.
    #   3    NOVALUE      ATOM     ERROR.
    #   4    NOVALUE      LIST     ERROR.
    #   5    ANYATOM    NOVALUE    DQ.  Must match now.
    #   6    ANYATOM    ANYATOM    DQ.  Must be provided.
    #   7    ANYATOM      ATOM     +1.
    #   8    ANYATOM      LIST     DQ.  ANYATOM can't match LIST.
    #   9      ATOM     NOVALUE    DQ.  Must match now.
    #  10      ATOM     ANYATOM    NotImplementedError.
    #  11      ATOM       ATOM     +1 if same, otherwise DQ.
    #  12      ATOM       LIST     +1 if ATOM in LIST, otherwise DQ.
    #  13      LIST     NOVALUE    DQ.  Must match now.
    #  14      LIST     ANYATOM    NotImplementedError.
    #  15      LIST       ATOM     +1 is ATOM in LIST, otherwise DQ.
    #  16      LIST       LIST     +1 if intersect, otherwise DQ.

    num_attributes = 0
    for key in cons_attr:
        p("  Evaluating attribute %s." % key)

        DATA_VALUE = data_attr.get(key)
        CONS_VALUE = cons_attr.get(key)
        DATA_TYPE = _get_attribute_type(data_attr, key)
        CONS_TYPE = _get_attribute_type(cons_attr, key)
        CASE = _assign_case_by_type(CONS_TYPE, DATA_TYPE)

        disqualify = False
        if CASE in [1, 2, 3, 4]:
            raise AssertionError, "Should not have NOVALUES."
        elif CASE == 7:
            num_attributes += 1
        elif CASE in [5, 6, 8, 9, 13]:
            disqualify = True
        elif CASE in [10, 14]:
            raise NotImplementedError
        elif CASE == 11:
            if CONS_VALUE == DATA_VALUE:
                num_attributes += 1
            else:
                disqualify = True
        elif CASE == 12:
            if CONS_VALUE in DATA_VALUE:
                num_attributes += 1
            else:
                disqualify = True
        elif CASE == 15:
            if DATA_VALUE in CONS_VALUE:
                num_attributes += 1
            else:
                disqualify = True
        elif CASE == 16:
            if _intersection(CONS_VALUE, DATA_VALUE):
                num_attributes += 1
            else:
                disqualify = True
        else:
            raise AssertionError
                
        if disqualify:
            p("    Attribute is disqualified.")
            num_attributes = 0
            break

    if not num_attributes:
        p("  No attributes compatible.")
    else:
        p("  %d attributes compatible." % num_attributes)
    return num_attributes


def _can_nonconverting_module_produce_data(module, data):
    p = _print_nothing
    #p = _print_string
    
    p("Checking if module %s can produce data." % module.name)

    x = [x for x in module.ante_datas if x.datatype == data.datatype]
    assert len(x) == 1
    ante_data = x[0]

    data_attr = data.attributes
    ante_attr = ante_data.attributes
    cons_attr = module.cons_data.attributes


    # CASE  CONS_TYPE  DATA_TYPE   RESULT
    #   1    NOVALUE    NOVALUE    +0.
    #   2    NOVALUE    ANYATOM    +0.
    #   3    NOVALUE      ATOM     +0.
    #   4    NOVALUE      LIST     +0.
    #   5    ANYATOM    NOVALUE    +0.
    #   6    ANYATOM    ANYATOM    +1.
    #   7    ANYATOM      ATOM     +1 if ANTE_VALUE != DATA_VALUE, otherwise DQ
    #   8    ANYATOM      LIST     DQ.  ANYATOM doesn't match LIST.
    #   9      ATOM     NOVALUE    +0.
    #  10      ATOM     ANYATOM    NotImplementedError.
    #  11      ATOM       ATOM     +1 if same, otherwise DQ.
    #  12      ATOM       LIST     +1 if ATOM in LIST, otherwise DQ.
    #  13      LIST     NOVALUE    +0.
    #  14      LIST     ANYATOM    NotImplementedError.
    #  15      LIST       ATOM     +1 is ATOM in LIST, otherwise DQ.
    #  16      LIST       LIST     +1 if intersect, otherwise DQ.
    #
    # *** The +1 only counts if module changes this attribute.
    # Otherwise, +0.

    num_attributes = 0
    for key in module.cons_data.datatype.attributes:
        p("  Evaluating attribute %s." % key)
        DATA_VALUE = data_attr.get(key)
        ANTE_VALUE = ante_attr.get(key)
        CONS_VALUE = cons_attr.get(key)
        DATA_TYPE = _get_attribute_type(data_attr, key)
        ANTE_TYPE = _get_attribute_type(ante_attr, key)
        CONS_TYPE = _get_attribute_type(cons_attr, key)
        CASE = _assign_case_by_type(CONS_TYPE, DATA_TYPE)
        
        module_changes_value = ANTE_VALUE != CONS_VALUE
        if ANTE_TYPE == TYPE_LIST and CONS_TYPE == TYPE_LIST:
            module_changes_value = sorted(ANTE_VALUE) != sorted(CONS_VALUE)


        disqualify = False
        if CASE in [1, 2, 3, 4]:
            assert ANTE_TYPE == TYPE_NOVALUE
        elif CASE in [5, 9, 13]:
            pass
        elif CASE in [10, 14]:
            raise NotImplementedError
        elif CASE == 6:
            if module_changes_value:
                p("    Attribute is compatible.")
                num_attributes += 1
        elif CASE == 7:
            if ANTE_TYPE == TYPE_NOVALUE:
                # Why disqualify this?
                disqualify = True
            elif ANTE_TYPE == TYPE_ANYATOM:
                raise NotImplementedError
            elif ANTE_TYPE == TYPE_ATOM:
                if DATA_VALUE == ANTE_VALUE:
                    disqualify = True
                else:
                    p("    Attribute is compatible.")
                    num_attributes += 1
            elif ANTE_TYPE == TYPE_LIST:
                if DATA_VALUE in ANTE_VALUE:
                    disqualify = True
                else:
                    p("    Attribute is compatible.")
                    num_attributes += 1
        elif CASE == 8:
            disqualify = True
        elif CASE == 11:
            if CONS_VALUE == DATA_VALUE:
                if module_changes_value:
                    p("    Attribute is compatible [ATOM %s ATOM %s]." % (
                        CONS_VALUE, DATA_VALUE))
                    num_attributes += 1
            else:
                disqualify = True
        elif CASE == 12:
            if CONS_VALUE in DATA_VALUE:
                if module_changes_value:
                    num_attributes += 1
            else:
                disqualify = True
        elif CASE == 15:
            if DATA_VALUE in CONS_VALUE:
                if module_changes_value:
                    p("    Attribute is compatible [LIST %s ATOM %s]." % (
                        str(CONS_VALUE), DATA_VALUE))
                    num_attributes += 1
            else:
                disqualify = True
        elif CASE == 16:
            if _intersection(CONS_VALUE, DATA_VALUE):
                if module_changes_value:
                    p("    Attribute is compatible.")
                    num_attributes += 1
            else:
                disqualify = True
        else:
            raise AssertionError
                
        if disqualify:
            p("    Attribute is disqualified.")
            num_attributes = 0
            break

    if not num_attributes:
        p("  No attributes compatible.")
    else:
        p("  %d attributes compatible." % num_attributes)
    return num_attributes


def _can_module_take_data(module, datas):
    # Return True/False if a module can take this Data as an
    # antecedent.

    if len(datas) > 1:
        raise NotImplementedError
    if len(module.ante_datas) != len(datas):
        return False
    data = datas[0]
    if data.datatype != module.ante_datas[0].datatype:
        return False

    data_attr = data.attributes
    ante_attr = module.ante_datas[0].attributes

    # If no attributes to match, then this matches by default.
    if not data_attr and not ante_attr:
        return True

    # CASE  DATA_TYPE  ANTE_TYPE   RESULT
    #   1    NOVALUE    NOVALUE    OK.
    #   2    NOVALUE    ANYATOM    No.
    #   3    NOVALUE      ATOM     No.
    #   4    NOVALUE      LIST     No.
    #   5    ANYATOM    NOVALUE    OK.
    #   6    ANYATOM    ANYATOM    OK.
    #   7    ANYATOM      ATOM     NotImplementedError.
    #   8    ANYATOM      LIST     No.
    #   9      ATOM     NOVALUE    OK.
    #  10      ATOM     ANYATOM    NotImplementedError.
    #  11      ATOM       ATOM     OK if ATOMs are the same.
    #  12      ATOM       LIST     OK if ATOM in LIST.
    #  13      LIST     NOVALUE    OK.
    #  14      LIST     ANYATOM    NotImplementedError.
    #  15      LIST       ATOM     No.
    #  16      LIST       LIST     OK if DATA LIST is subset of ANTE LIST.

    compatible = True
    all_attr = {}.fromkeys(data_attr.keys() + ante_attr.keys())
    for key in all_attr:
        DATA_VALUE = data_attr.get(key)
        ANTE_VALUE = ante_attr.get(key)
        DATA_TYPE = _get_attribute_type(data_attr, key)
        ANTE_TYPE = _get_attribute_type(ante_attr, key)
        CASE = _assign_case_by_type(DATA_TYPE, ANTE_TYPE)

        if CASE in [1, 5, 6, 9, 13]:  # OK
            pass
        elif CASE in [7, 10, 14]:
            raise NotImplementedError
        elif CASE in [2, 3, 4, 8, 15]:
            compatible = False
        elif CASE == 11:
            if DATA_VALUE != ANTE_VALUE:
                compatible = False
        elif CASE == 12:
            if DATA_VALUE not in ANTE_VALUE:
                compatible = False
        elif CASE == 16:
            if not _is_subset(DATA_VALUE, ANTE_VALUE):
                compatible = False
        else:
            raise AssertionError
                
    return compatible


def _can_reach_by_bc(network, node_id, good_ids):
    # Return a dictionary of all the node IDs that can be reached by
    # backwards chaining.
    reachable_ids = {}
    stack = [node_id]
    while stack:
        nid = stack.pop(0)
        if nid in reachable_ids:
            continue
        if nid not in good_ids:
            continue
        reachable_ids[nid] = 1
        ids = _backchain_to_ids(network, nid)
        stack.extend(ids)
    return reachable_ids


def _can_reach_by_fc(network, node_id, good_ids):
    # Return a dictionary of all the node IDs that can be reached by
    # forward chaining.
    reachable_ids = {}
    stack = [node_id]
    while stack:
        nid = stack.pop(0)
        if nid in reachable_ids:
            continue
        if nid not in good_ids:
            continue
        reachable_ids[nid] = 1
        ids = network.transitions.get(nid, [])
        stack.extend(ids)
    return reachable_ids


def _find_data_node(nodes, node):
    assert isinstance(node, Data)

    # CASE   N1_TYPE    N2_TYPE    RESULT
    #   1    NOVALUE    NOVALUE    OK.
    #   2    NOVALUE    ANYATOM    No.
    #   3    NOVALUE      ATOM     No.
    #   4    NOVALUE      LIST     No.
    #   5    ANYATOM    NOVALUE    No.
    #   6    ANYATOM    ANYATOM    OK.
    #   7    ANYATOM      ATOM     No.
    #   8    ANYATOM      LIST     No.
    #   9      ATOM     NOVALUE    No.
    #  10      ATOM     ANYATOM    No.
    #  11      ATOM       ATOM     OK if ATOM equal.
    #  12      ATOM       LIST     No.
    #  13      LIST     NOVALUE    No.
    #  14      LIST     ANYATOM    No.
    #  15      LIST       ATOM     No.
    #  16      LIST       LIST     OK if LIST equal.
    
    for i, n in enumerate(nodes):
        if not isinstance(n, Data):
            continue
        if n.datatype != node.datatype:
            continue

        n1_attr = n.attributes
        n2_attr = node.attributes
        x1 = n1_attr.keys()
        x2 = n2_attr.keys()
        all_attributes = {}.fromkeys(x1 + x2)

        is_equal = True
        for key in all_attributes:
            N1_VALUE = n1_attr.get(key)
            N2_VALUE = n2_attr.get(key)
            N1_TYPE = _get_attribute_type(n1_attr, key)
            N2_TYPE = _get_attribute_type(n2_attr, key)

            attr_equal = False
            # Case 1.
            if N1_TYPE == TYPE_NOVALUE and N2_TYPE == TYPE_NOVALUE:
                attr_equal = True
            # Case 6.
            elif N1_TYPE == TYPE_ANYATOM and N2_TYPE == TYPE_ANYATOM:
                attr_equal = True
            # Case 11.
            elif N1_TYPE == TYPE_ATOM and N2_TYPE == TYPE_ATOM:
                if N1_VALUE == N2_VALUE:
                    attr_equal = True
            # Case 16.
            elif N1_TYPE == TYPE_LIST and N2_TYPE == TYPE_LIST:
                if sorted(N1_VALUE) == sorted(N2_VALUE):
                    attr_equal = True
            if not attr_equal:
                is_equal = False
        if is_equal:
            return i
    return -1


def _find_module_node(nodes, node):
    assert isinstance(node, Module)

    for i, n in enumerate(nodes):
        if not isinstance(n, Module):
            continue
        if node == n:
            return i
    return -1


def _is_compatible_with_start(data, start_data):
    # data is a Data node in the network.  start_data is the Data that
    # the user wants to start on.
    if data.datatype != start_data.datatype:
        return False

    # Start Data
    # ATOM      Must match a specific value.
    # LIST      UNDEFINED.
    # ANYATOM   Can match any value.
    # NOVALUE   Use default value.
    # 
    # CASE START_TYPE  DATA_TYPE   RESULT
    #   1    NOVALUE    NOVALUE    ERROR.  START should have default values.
    #   2    NOVALUE    ANYATOM    ERROR.  START should have default values.
    #   3    NOVALUE      ATOM     ERROR.  START should have default values.
    #   4    NOVALUE      LIST     ERROR.  START should have default values.
    #   5    ANYATOM    NOVALUE    No.
    #   6    ANYATOM    ANYATOM    OK.
    #   7    ANYATOM      ATOM     OK.
    #   8    ANYATOM      LIST     No.
    #   9      ATOM     NOVALUE    No.
    #  10      ATOM     ANYATOM    OK.
    #  11      ATOM       ATOM     Check if items are equal.
    #  12      ATOM       LIST     Check if ATOM in LIST.
    #  13      LIST     NOVALUE    NotImplementedError.
    #  14      LIST     ANYATOM    NotImplementedError.
    #  15      LIST       ATOM     NotImplementedError.
    #  16      LIST       LIST     NotImplementedError.

    data_attr = data.attributes
    strt_attr = start_data.attributes

    # Fill in default values for the start.
    defaults = start_data.datatype.get_defaults()
    strt_attr = strt_attr.copy()
    for key in start_data.datatype.attributes:
        if key not in strt_attr:
            strt_attr[key] = defaults[key]
    
    compatible = True
    for key in strt_attr:
        DATA_VALUE = data_attr.get(key)
        STRT_VALUE = strt_attr.get(key)
        DATA_TYPE = _get_attribute_type(data_attr, key)
        STRT_TYPE = _get_attribute_type(strt_attr, key)
        CASE = _assign_case_by_type(STRT_TYPE, DATA_TYPE)

        if CASE in [1, 2, 3, 4]:
            raise AssertionError
        elif CASE in [13, 14, 15, 16]:
            raise NotImplementedError
        elif CASE in [5, 8, 9]:
            compatible = False
        elif CASE in [6, 7, 10]:
            pass
        elif CASE == 11:
            if DATA_VALUE != STRT_VALUE:
                compatible = False
        elif CASE == 12:
            if STRT_VALUE not in DATA_VALUE:
                compatible = False
        else:
            raise AssertionError
    return compatible
            
        
def _is_compatible_with_internal(data, internal_data):
    # data is a Data node in the network.  internal_data is the Data
    # node that the user wants to include in the network.
    if data.datatype != internal_data.datatype:
        return False

    # Internal data.
    # ATOM      Must match a specific value.
    # LIST      UNDEFINED.
    # ANYATOM   UNDEFINED.
    # NOVALUE   User doesn't care.
    # 
    # CASE  INTL_TYPE   DATA_TYPE  RESULT
    #   1    NOVALUE    NOVALUE    OK.
    #   2    NOVALUE    ANYATOM    OK.
    #   3    NOVALUE      ATOM     OK.
    #   4    NOVALUE      LIST     OK.
    #   5    ANYATOM    NOVALUE    NotImplementedError.
    #   6    ANYATOM    ANYATOM    NotImplementedError.
    #   7    ANYATOM      ATOM     NotImplementedError.
    #   8    ANYATOM      LIST     NotImplementedError.
    #   9      ATOM     NOVALUE    No.
    #  10      ATOM     ANYATOM    OK.
    #  11      ATOM       ATOM     Check if items are equal.
    #  12      ATOM       LIST     No.  Actual value is unknown.
    #  13      LIST     NOVALUE    NotImplementedError.
    #  14      LIST     ANYATOM    NotImplementedError.
    #  15      LIST       ATOM     NotImplementedError.
    #  16      LIST       LIST     NotImplementedError.

    data_attr = data.attributes
    intl_attr = internal_data.attributes

    compatible = True
    for key in intl_attr:
        INTL_VALUE = intl_attr.get(key)
        DATA_VALUE = data_attr.get(key)
        INTL_TYPE = _get_attribute_type(intl_attr, key)
        DATA_TYPE = _get_attribute_type(data_attr, key)
        CASE = _assign_case_by_type(INTL_TYPE, DATA_TYPE)

        if CASE in [1, 2, 3, 4, 10]:
            pass
        elif CASE in [5, 6, 7, 8, 13, 14, 15, 16]:
            raise NotImplementedError
        elif CASE in [9, 12]:
            compatible = False
        elif CASE == 11:
            if INTL_VALUE != DATA_VALUE:
                compatible = False
        else:
            raise AssertionError
    return compatible
            
        
def _assign_case_by_type(type1, type2):
    types = [
        (TYPE_NOVALUE, TYPE_NOVALUE),
        (TYPE_NOVALUE, TYPE_ANYATOM),
        (TYPE_NOVALUE, TYPE_ATOM),
        (TYPE_NOVALUE, TYPE_LIST),
        (TYPE_ANYATOM, TYPE_NOVALUE),
        (TYPE_ANYATOM, TYPE_ANYATOM),
        (TYPE_ANYATOM, TYPE_ATOM),
        (TYPE_ANYATOM, TYPE_LIST),
        (TYPE_ATOM, TYPE_NOVALUE),
        (TYPE_ATOM, TYPE_ANYATOM),
        (TYPE_ATOM, TYPE_ATOM),
        (TYPE_ATOM, TYPE_LIST),
        (TYPE_LIST, TYPE_NOVALUE),
        (TYPE_LIST, TYPE_ANYATOM),
        (TYPE_LIST, TYPE_ATOM),
        (TYPE_LIST, TYPE_LIST),
        ]
    x = (type1, type2)
    assert x in types, "Unknown types: %s %s" % (type1, type2)
    i = types.index(x)
    return i+1


def _get_attribute_type(attributes, name):
    import operator

    x = attributes.get(name)

    if name not in attributes:
        return TYPE_NOVALUE
    elif x == ANYATOM:
        return TYPE_ANYATOM
    elif type(x) is type(""):
        return TYPE_ATOM
    elif operator.isSequenceType(x):
        return TYPE_LIST
    raise AssertionError, "Unknown attribute type: %s" % str(x)


def _intersection(x, y):
    return list(set(x).intersection(y))


def _is_subset(x, y):
    # Return whether x is a subset of y.
    for i in range(len(x)):
        if x[i] not in y:
            return False
    return True


def _print_nothing(s):
    pass


def _print_string(s):
    print s


def _print_line(line, prefix0, prefixn, width):
    lines = []
    p = prefix0
    while line:
        x = line[:(width-len(p))]
        line = line[len(x):]
        lines.append(x)
        p = prefixn
        
    for i in range(len(lines)):
        p = prefixn
        if i == 0:
            p = prefix0
        print "%s%s" % (p, lines[i])


def _print_network(network):
    line_width = 72
    for i in range(len(network.nodes)):
        p_step = "%2d.  " % i
        p_space = " " * (len(p_step)+2)
        _print_line(str(network.nodes[i]), p_step, p_space, line_width)
    print

    for i in sorted(network.transitions):
        x = [i, "->"] + network.transitions[i]
        print "\t".join(map(str, x))
    

def _plot_network_gv(filename, network):
    from genomicode import graphviz
    
    gv_nodes = []
    gv_edges = []
    gv_node2attr = {}

    id2name = {}
    for node_id, n in enumerate(network.nodes):
        node2attr = {}
        node2attr["style"] = "filled"
        if n.__class__.__name__ == "Data":
            x = n.datatype.name
            node2attr["shape"] = "note"
            node2attr["fillcolor"] = "#EEEEEE"
        else:
            x = n.name
            node2attr["shape"] = "box"
            node2attr["fillcolor"] = "#80E0AA"
            
        node_name = "%s [%d]" % (x, node_id)
        id2name[node_id] = node_name
        gv_nodes.append(node_name)
        gv_node2attr[node_name] = node2attr

    for node_id, next_ids in network.transitions.iteritems():
        for nid in next_ids:
            x1 = id2name[node_id]
            x2 = id2name[nid]
            gv_edges.append((x1, x2))

    graphviz.draw(
        filename, gv_nodes, gv_edges, node2attributes=gv_node2attr, prog="dot",
        directed=True)

    
def _pretty_attributes(attributes):
    import re

    if not attributes:
        return ""

    all_attributes = sorted(attributes)

    # Separate the proper python variables from other attributes.
    proper = []
    improper = []
    for key in all_attributes:
        if re.match(r"^[a-z_][a-z0-9_]*$", key, re.I):
            proper.append(key)
        else:
            improper.append(key)

    # For proper python variables, format as <key>=<value>.
    fmt_proper = []
    for key in proper:
        x = "%s=%r" % (key, attributes[key])
        fmt_proper.append(x)
    fmt_proper = ", ".join(fmt_proper)

    # For improper python variables, format as a dict.
    x = {}
    for key in improper:
        x[key] = attributes[key]
    fmt_improper = ""
    if x:
        fmt_improper = repr(x)

    if not fmt_improper:
        return fmt_proper
    return "%s, %s" % (fmt_proper, fmt_improper)


def test_bie():
    #print_modules(all_modules); return

    #x = SignalFile(
    #    format="unknown", group_fc=ANYATOM, logged="unknown",
    #    missing_values="unknown", preprocess="unknown")
    #x = SignalFile(preprocess="illumina")
    #in_data = [GEOSeries, ClassLabelFile]
    #in_data = [x, ClassLabelFile]
    
    in_data = [SignalFile(contents='train0',logged="yes", preprocess="rma"),
               SignalFile(contents='train1',logged="yes", preprocess="rma"),
               SignalFile(contents='test',logged="yes", preprocess="rma")]
    #in_data = SignalFile(preprocess="rma", format="jeffs")

    #print _make_goal(SignalFile, x)
    #return

    #goal_datatype = CELFiles
    #goal_attributes = {}
    #goal_attributes = dict(platform="GPL1691")
    #goal_attributes = dict(version=["v3", "v4"])

    #goal_datatype = ILLUFolder
    #goal_attributes = dict(
    #    ill_bg_mode='true',
    #    ill_chip='ilmn_HumanHT_12_V4_0_R1_15002873_B.chip',
    #    ill_clm='',
    #    ill_coll_mode='none',
    #    ill_custom_chip='',
    #    ill_custom_manifest='',
    #    illu_manifest='HumanHT-12_V4_0_R2_15002873_B.txt')
    
    goal_datatype = SignalFile
 #   goal_attributes = dict(format='gct', logged='no',preprocess='rma',combat_norm='yes',
 #                          quantile_norm='yes',gene_center='mean',gene_normalize='variance',
 #                          group_fc='20',num_feature='20',gene_order='t_test_p')
    goal_attributes = dict(
        contents="train0,train1,test",
        format='tdf', logged='yes', preprocess="rma",
        missing_values='zero_fill')
        #gene_center='mean',annotate='yes',
        #gene_normalize='variance',
        #)
    #goal_attributes = dict(
    #    format=['jeffs', 'gct', 'tdf'], preprocess='rma', logged='yes',
    #    missing_values="no")
    #goal_attributes = dict(
    #    format='tdf', preprocess='illumina', logged='yes',
    #    missing_values="no", group_fc="5")
    #goal_attributes = dict(
    #    format='tdf', preprocess="rma", logged='yes', 
    #    missing_values="no")
    #goal_attributes = dict(format='tdf', preprocess='rma', logged='yes')
    #goal_attributes = dict(
    #    format='tdf', preprocess='rma', logged='yes',
    #    quantile_norm="yes", combat_norm="yes", dwd_norm="yes",
    #    missing_values="no",gene_order='gene_list')
    #goal_attributes = dict(
    #    format='tdf', preprocess='illumina', logged='yes')
    #goal_attributes = dict(
    #    format='tdf', preprocess='illumina', logged='yes',
    #    #quantile_norm="yes", combat_norm="yes", dwd_norm="yes",
    #    missing_values="zero_fill", group_fc="5", ill_bg_mode='true',
    #    illu_coll_mode="max")
    #goal_attributes = dict(
    #    format='tdf', preprocess='illumina', logged='yes',
    #    #quantile_norm="yes", combat_norm="yes", dwd_norm="yes",
    #    missing_values="zero_fill", platform='hg19',
    #    duplicate_probe='closest_probe')
    #goal_attributes = dict(
    #    format='tdf', preprocess='illumina', logged='yes',
    #    quantile_norm="no", combat_norm="no", dwd_norm="no",
    #    missing_values="zero_fill", platform='hg19',
    #    duplicate_probe='closest_probe')
    #goal_attributes = dict(
    #    format='tdf', preprocess='illumina', logged='yes',
    #    quantile_norm="yes", combat_norm="yes", dwd_norm="yes",
    #    missing_values="zero_fill", platform='hg19',
    #    duplicate_probe='closest_probe')

    #out_data = make_data(
    #    "signal_file", format='tdf', preprocess='rma', logged='yes',
    #    filter='no', missing='zero', predataset='no', rename_sample='no',
    #    gene_center='no', gene_normalize='no', quantile_norm='yes',
    #    dwd_norm="no", gene_order="class_neighbors", shiftscale_norm="no",
    #    unique_genes="average_genes")
    #out_data = make_data(
    #    "signal_file", format='tdf',preprocess='rma',logged='yes',
    #    filter='no', missing='zero', predataset='no', rename_sample='no',
    #    quantile_norm='yes', dwd_norm='no', gene_order='class_neighbors',
    #    shiftscale_norm='no', combat_norm='no', bfrm_norm='yes',
    #    gene_center='mean', gene_normalize='variance', group_fc='int',
    #    num_features='int', annotate="yes", unique_genes='average_genes',
    #    platform='str', duplicate_probe='high_var_probe')
    
    network = backchain(all_modules, goal_datatype, goal_attributes)
    network = optimize_network(network)
    network = prune_network_by_start(network, in_data)
    print network.nodes
    print len(network.nodes)
    print network.transitions
    #network = prune_network_by_internal(
    #    network, SignalFile(quantile_norm="yes", combat_norm="no"))
    #network = prune_network_by_internal(
    #    network, SignalFile(combat_norm="yes", dwd_norm="no"))
    
    _print_network(network)
    _plot_network_gv("out.png", network)

    # Want function _find_data_node with options:
    # ignore_defaults
    # allow_more_general
    #node = _make_goal(
    #    SignalFile, dict(format="pcl", preprocess="rma"))
    #node_id = _find_data_node(network.nodes, node)
    #print "NODE:", node_id

    #node = _make_goal(
    #    SignalFile, dict(format=["tdf", "pcl", "gct"], preprocess="rma"))
    #node_id = _find_data_node(network.nodes, node)
    #print "NODE:", node_id


ILLU_MANIFEST = [
    'HumanHT-12_V3_0_R2_11283641_A.txt',
    'HumanHT-12_V4_0_R2_15002873_B.txt',
    'HumanHT-12_V3_0_R3_11283641_A.txt',
    'HumanHT-12_V4_0_R1_15002873_B.txt',
    'HumanMI_V1_R2_XS0000122-MAP.txt',
    'HumanMI_V2_R0_XS0000124-MAP.txt',
    'HumanRef-8_V2_0_R4_11223162_A.txt',
    'HumanRef-8_V3_0_R1_11282963_A_WGDASL.txt',
    'HumanRef-8_V3_0_R2_11282963_A.txt',
    'HumanRef-8_V3_0_R3_11282963_A.txt',
    'HumanWG-6_V2_0_R4_11223189_A.txt',
    'HumanWG-6_V3_0_R2_11282955_A.txt',
    'HumanWG-6_V3_0_R3_11282955_A.txt',
    'MouseMI_V1_R2_XS0000127-MAP.txt',
    'MouseMI_V2_R0_XS0000129-MAP.txt',
    'MouseRef-8_V1_1_R4_11234312_A.txt',
    'MouseRef-8_V2_0_R2_11278551_A.txt',
    'MouseRef-8_V2_0_R3_11278551_A.txt',
    'MouseWG-6_V1_1_R4_11234304_A.txt',
    'MouseWG-6_V2_0_R2_11278593_A.txt',
    'MouseWG-6_V2_0_R3_11278593_A.txt',
    'RatRef-12_V1_0_R5_11222119_A.txt'
    ]

ILLU_CHIP = [
    'ilmn_HumanHT_12_V3_0_R3_11283641_A.chip',
    'ilmn_HumanHT_12_V4_0_R1_15002873_B.chip',
    'ilmn_HumanRef_8_V2_0_R4_11223162_A.chip',
    'ilmn_HumanReF_8_V3_0_R1_11282963_A_WGDASL.chip',
    'ilmn_HumanRef_8_V3_0_R3_11282963_A.chip',
    'ilmn_HumanWG_6_V2_0_R4_11223189_A.chip',
    'ilmn_HumanWG_6_V3_0_R3_11282955_A.chip',
    'ilmn_MouseRef_8_V1_1_R4_11234312_A.chip',
    'ilmn_MouseRef_8_V2_0_R3_11278551_A.chip',
    'ilmn_MouseWG_6_V1_1_R4_11234304_A.chip',
    'ilmn_MouseWG_6_V2_0_R3_11278593_A.chip',
    'ilmn_RatRef_12_V1_0_R5_11222119_A.chip'
    ]

RenameFile = DataType('RenameFile')
AgilentFiles = DataType("AgilentFiles")
CELFiles = DataType(
    "CELFiles",
    Attribute(version=["unknown", "cc", "v3", "v4"], DEFAULT="unknown"),
    )
ControlFile = DataType(
    "ControlFile",
    Attribute(
        preprocess=["unknown", "illumina", "agilent", "mas5", "rma", "loess"],
        DEFAULT="unknown"),
    Attribute(
        missing_values=["unknown", "no", "yes", "median_fill", "zero_fill"],
        DEFAULT="unknown"),
    Attribute(
        logged=["unknown", "no", "yes"],
        DEFAULT="unknown"),
    Attribute(
        format=["unknown", "tdf", "gct", "jeffs", "pcl", "res", "xls"],
        DEFAULT="unknown"),
    )
ExpressionFiles = DataType("ExpressionFiles")
GPRFiles = DataType("GPRFiles")
GEOSeries = DataType(
    "GEOSeries",
    Attribute(GSEID=ANYATOM, DEFAULT="", REQUIRED=True),
    Attribute(GPLID=ANYATOM, DEFAULT=""),
    )
IDATFiles = DataType("IDATFiles")
ClassLabelFile = DataType("ClassLabelFile")
ILLUFolder = DataType(
    "ILLUFolder", 
    Attribute(illu_manifest=ILLU_MANIFEST,
              DEFAULT='HumanHT-12_V4_0_R2_15002873_B.txt'),
    Attribute(illu_chip=ILLU_CHIP,
              DEFAULT='ilmn_HumanHT_12_V4_0_R1_15002873_B.chip'),
    Attribute(illu_bg_mode=['false', 'true'], DEFAULT="false"),
    Attribute(illu_coll_mode=['none', 'max', 'median'], DEFAULT="none"),
    Attribute(illu_clm=ANYATOM, DEFAULT=""),
    Attribute(illu_custom_chip=ANYATOM, DEFAULT=""),
    Attribute(illu_custom_manifest=ANYATOM, DEFAULT=""))
GeneListFile=DataType(
    "GeneListFile",
    Attribute(cn_num_neighbors=ANYATOM, DEFAULT=""),
    Attribute(cn_num_perm=ANYATOM, DEFAULT=""),
    Attribute(cn_user_pval=ANYATOM, DEFAULT=""),  
    Attribute(cn_mean_or_median=['mean', 'median'], DEFAULT='mean'),
    Attribute(cn_ttest_or_snr=['t_test','snr'], DEFAULT='t_test'),
    Attribute(cn_filter_data=['yes','no'], DEFAULT='no'),
    Attribute(cn_min_threshold=ANYATOM, DEFAULT=""),
    Attribute(cn_max_threshold=ANYATOM, DEFAULT=""),
    Attribute(cn_min_folddiff=ANYATOM, DEFAULT=""),
    Attribute(cn_abs_diff=ANYATOM, DEFAULT=""),
    Attribute(gene_order=['no', "gene_list", "class_neighbors",
                          "t_test_p", "t_test_fdr"], DEFAULT='gene_list'))
SignalFile = DataType(
    "SignalFile",

    # Properties of the format.
    Attribute(
        format=["unknown", "tdf", "gct", "jeffs", "pcl", "res", "xls"],
        DEFAULT="unknown"),
    
    # Properties of the data.
    Attribute(
        preprocess=["unknown", "illumina", "agilent", "mas5", "rma", "loess"],
        DEFAULT="unknown"),
    Attribute(
        missing_values=["unknown", "no", "yes", "median_fill", "zero_fill"],
        DEFAULT="unknown"),
    Attribute(
        logged=["unknown", "no", "yes"],
        DEFAULT="unknown"),

    # Normalizing the data.  Very difficult to check normalization.
    # If you're not sure if the data is normalized, then the answer is
    # "no".
    Attribute(dwd_norm=["no", "yes"], DEFAULT="no"),
    Attribute(bfrm_norm=["no", "yes"], DEFAULT="no"),
    Attribute(quantile_norm=["no", "yes"], DEFAULT="no"),
    Attribute(shiftscale_norm=["no", "yes"], DEFAULT="no"),
    Attribute(combat_norm=["no", "yes"], DEFAULT="no"),
    Attribute(predataset=["no", "yes"], DEFAULT="no"),
    Attribute(filter=ANYATOM, DEFAULT="no"),
    Attribute(rename_sample=["no", "yes"], DEFAULT="no"),
    Attribute(contents=["train0", "train1", "test", "train0,train1,test",
                        "class0", "class1", "class0,class1", "no"], DEFAULT="no"))
SignalFile1 = DataType(
    "SignalFile1",
    # Properties of the format.
    Attribute(
        format=[ "tdf", "pcl"],
        DEFAULT="tdf"),
    # Properties of the data.
    Attribute(
        preprocess=["unknown", "illumina", "agilent", "mas5", "rma", "loess"],
        DEFAULT="unknown"),
    Attribute(
        missing_values=[ "no", "median_fill", "zero_fill"],
        DEFAULT="no"),
    Attribute(
        logged=["yes"],
        DEFAULT="yes"),
    Attribute(predataset=["no", "yes"], DEFAULT="no"),
    Attribute(filter=ANYATOM, DEFAULT="no"),
    Attribute(rename_sample=["no", "yes"], DEFAULT="no"),
    Attribute(dwd_norm=["no", "yes"], DEFAULT="no"),
    Attribute(bfrm_norm=["no", "yes"], DEFAULT="no"),
    Attribute(quantile_norm=["no", "yes"], DEFAULT="no"),
    Attribute(shiftscale_norm=["no", "yes"], DEFAULT="no"),
    Attribute(combat_norm=["no", "yes"], DEFAULT="no"),
    Attribute(
        gene_center=["unknown", "no", "mean", "median"],
        DEFAULT="unknown"),
    Attribute(
        gene_normalize=["unknown", "no", "variance", "sum_of_squares"],
        DEFAULT="unknown"),
    Attribute(contents=["train0", "train1", "test", "train0,train1,test",
                        "class0", "class1", "class0,class1", "no"], DEFAULT="no")
    )
SignalFile2 = DataType(
    "SignalFile2",
    # Properties of the format.
    Attribute(
        format=[ "tdf", "gct"],
        DEFAULT="tdf"),
    # Properties of the data.
    Attribute(
        preprocess=["unknown", "illumina", "agilent", "mas5", "rma", "loess"],
        DEFAULT="unknown"),
    Attribute(
        missing_values=[ "no", "median_fill", "zero_fill"],
        DEFAULT="no"),
    Attribute(
        logged=[ "no", "yes"],
        DEFAULT="yes"),
    # Normalizing the genes.
    Attribute(
        gene_center=["unknown", "no", "mean", "median"],
        DEFAULT="unknown"),
    Attribute(
        gene_normalize=["unknown", "no", "variance", "sum_of_squares"],
        DEFAULT="unknown"),

    # Normalizing the data.  Very difficult to check normalization.
    # If you're not sure if the data is normalized, then the answer is
    # "no".
    Attribute(
        dwd_norm=["no", "yes"], DEFAULT="no"),
    Attribute(
        bfrm_norm=["no", "yes"], DEFAULT="no"),
    Attribute(
        quantile_norm=["no", "yes"], DEFAULT="no"),
    Attribute(
        shiftscale_norm=["no", "yes"], DEFAULT="no"),
    Attribute(
        combat_norm=["no", "yes"], DEFAULT="no"),

    # Annotations.
    Attribute(annotate=["no", "yes"], DEFAULT="no"),
    Attribute(
        unique_genes=["no", "average_genes", "high_var", "first_gene"],
        DEFAULT="no"),
    Attribute(
        duplicate_probe=["no", "yes", "closest_probe", "high_var_probe"],
        DEFAULT="no"),
    Attribute(rename_sample=["no", "yes"], DEFAULT="no"),


    # Unclassified.
    Attribute(num_features=ANYATOM, DEFAULT="all"),
    Attribute(
        gene_order=[
            "no", "class_neighbors", "gene_list", "t_test_p", "t_test_fdr"],
        DEFAULT="no"),
    Attribute(predataset=["no", "yes"], DEFAULT="no"),
    Attribute(platform=ANYATOM, DEFAULT="no"),
    Attribute(filter=ANYATOM, DEFAULT="no"),
    Attribute(group_fc=ANYATOM, DEFAULT="no"),
    Attribute(contents=["train0", "train1", "test", "train0,train1,test",
                        "class0", "class1", "class0,class1", "no"], DEFAULT="no")
    )
    
all_modules = [
    # GSEID
    Module("download_geo", GEOSeries, ExpressionFiles),
    Module("extract_CEL_files", ExpressionFiles, CELFiles(version="unknown")),

    # CELFiles
    QueryModule(
        "detect_CEL_version",
        CELFiles(version="unknown"),
        CELFiles(version=["cc", "v3", "v4"])),
    Module(
        "convert_CEL_cc_to_CEL_v3",
        CELFiles(version="cc"),
        CELFiles(version="v3")),
    Module(
        "preprocess_rma",
        CELFiles(version=["v3", "v4"]),
        SignalFile(
            logged="yes", preprocess="rma", format="jeffs",
            missing_values="no")
        ),
    Module(
        "preprocess_mas5",
        CELFiles(version=["v3", "v4"]),
        SignalFile(
            logged="no", preprocess="mas5", format="jeffs",
            missing_values="no")),
    # IDATFiles
    Module("extract_illumina_idat_files", ExpressionFiles, IDATFiles),
    Module(
        "preprocess_illumina",
        IDATFiles,
        ILLUFolder(
            illu_manifest=ILLU_MANIFEST, illu_chip=ILLU_CHIP,
            illu_bg_mode=["false", "true"],
            illu_coll_mode=["none", "max", "median"],
            illu_clm=ANYATOM, illu_custom_chip=ANYATOM,
            illu_custom_manifest=ANYATOM)),
    Module(
        "get_illumina_signal",
        ILLUFolder,
        SignalFile(logged="no", preprocess="illumina", format="gct")
        ),
    Module(
        "get_illumina_control",
        ILLUFolder,
        ControlFile(preprocess="illumina", format="gct", logged="no")
        ),
    
    # AgilentFiles
    Module(
        "extract_agilent_files", ExpressionFiles, AgilentFiles),
    Module(
        "preprocess_agilent",
        AgilentFiles,
        SignalFile(logged="no", preprocess="agilent", format="tdf")),

    # GPRFiles
    Module(
        "extract_gpr_files", ExpressionFiles, GPRFiles),
    Module(
        "normalize_with_loess",
        GPRFiles,
        SignalFile(format="tdf", logged="no", preprocess="loess")
        ),
    
    # SignalFile
    Module(
        "convert_signal_to_tdf",
        SignalFile(format=['pcl', 'res', 'gct', 'jeffs', 'unknown', 'xls']),
        SignalFile(format='tdf')),
    
    Module(
        "check_for_log",
        SignalFile(format="tdf", logged='unknown'),
        SignalFile(format="tdf", logged=['yes', "no"])),
    Module(
        "log_signal",
        SignalFile(logged='no', format=["tdf"]),
        SignalFile(logged='yes', format='tdf')),
    
    Module(
        "fill_missing_with_median",
        SignalFile(format="tdf", logged="yes", missing_values="yes"),
        SignalFile(format="tdf", logged="yes", missing_values="median_fill")),
    Module(
        "fill_missing_with_zeros",
        SignalFile(format="tdf", logged="yes", missing_values="yes"),
        SignalFile(format="tdf", logged="yes", missing_values="zero_fill")),
    Module(
        "check_for_missing_values",
        SignalFile(format="tdf", missing_values="unknown",logged='yes'),
        SignalFile(format="tdf", missing_values=["no", "yes"],logged='yes')),
    Module(
        "filter_genes_by_missing_values",
        SignalFile(
            format='tdf', logged="yes", missing_values="yes", filter="no"),
        SignalFile(
            format='tdf', logged="yes", missing_values="yes", filter=ANYATOM)),
    Module(
        "filter_and_threshold_genes",
        SignalFile(format="tdf",logged=["unknown","no"], predataset="no"),
        SignalFile(format="tdf",logged=["unknown","no"], predataset="yes")),
    Module(
        "relabel_samples",
        [RenameFile,
         SignalFile(format='tdf', rename_sample="no",logged="yes",
                    missing_values=['no', 'median_fill', 'zero_fill'],
                   combat_norm='no',quantile_norm="no",
                   dwd_norm="no",bfrm_norm="no",shiftscale_norm="no")],
        SignalFile(format='tdf', rename_sample="yes",logged="yes",
                   missing_values=['no', 'median_fill', 'zero_fill'],
                   combat_norm='no',quantile_norm="no",
                   dwd_norm="no",bfrm_norm="no",shiftscale_norm="no")),
    Module(
           "merge_signal_for_classification",
           [SignalFile(contents="train0",format='tdf',logged="yes",
                       missing_values=['no', 'median_fill', 'zero_fill'],
                       combat_norm='no',quantile_norm="no",
                       dwd_norm="no",bfrm_norm="no",shiftscale_norm="no"),
            SignalFile(contents="train1",format='tdf',logged="yes",
                       missing_values=['no', 'median_fill', 'zero_fill'],
                       combat_norm='no',quantile_norm="no",
                       dwd_norm="no",bfrm_norm="no",shiftscale_norm="no"),
            SignalFile(contents="test",format='tdf',logged="yes",
                       missing_values=['no', 'median_fill', 'zero_fill'],
                       combat_norm='no',quantile_norm="no",
                       dwd_norm="no",bfrm_norm="no",shiftscale_norm="no")],
            SignalFile(contents="train0,train1,test",format='tdf',logged="yes",
                       missing_values=['no', 'median_fill', 'zero_fill'],
                       combat_norm='no',quantile_norm="no",
                       dwd_norm="no",bfrm_norm="no",shiftscale_norm="no")),
    Module(
           "merge_two_classes",
           [SignalFile(contents="class0",format='tdf',logged="yes",
                       missing_values=['no', 'median_fill', 'zero_fill'],
                       combat_norm='no',quantile_norm="no",
                       dwd_norm="no",bfrm_norm="no",shiftscale_norm="no"),
            SignalFile(contents="class1",format='tdf',logged="yes",
                       missing_values=['no', 'median_fill', 'zero_fill'],
                       combat_norm='no',quantile_norm="no",
                       dwd_norm="no",bfrm_norm="no",shiftscale_norm="no")],
            SignalFile(contents="class0,class1",format='tdf',logged="yes",
                       missing_values=['no', 'median_fill', 'zero_fill'],
                       combat_norm='no',quantile_norm="no",
                       dwd_norm="no",bfrm_norm="no",shiftscale_norm="no")),        
    # Sample normalization.
    Module(
        "normalize_samples_with_quantile",
        SignalFile(
            format="tdf", logged="yes",
            missing_values=["no", "zero_fill", "median_fill"],
            quantile_norm="no"),
        SignalFile(
            format="tdf", logged="yes",
            missing_values=["no", "zero_fill", "median_fill"],
            quantile_norm="yes")),
    Module(
        "normalize_samples_with_combat",
        [ClassLabelFile,SignalFile(
            format="tdf", logged="yes",
            missing_values=["no", "zero_fill", "median_fill"],
            combat_norm="no")],
        SignalFile(
            format="tdf", logged="yes",
            missing_values=["no", "zero_fill", "median_fill"],
            combat_norm="yes")),
    Module(
        "normalize_samples_with_dwd",
        [ClassLabelFile,SignalFile(
            format="tdf", logged="yes",
            missing_values=["no", "zero_fill", "median_fill"],
            dwd_norm="no")],
        SignalFile(
            format="tdf", logged="yes",
            missing_values=["no", "zero_fill", "median_fill"],
            dwd_norm="yes")),
    Module(
        "normalize_samples_with_bfrm",
        SignalFile(
            format="tdf", logged="yes",
            missing_values=["no", "zero_fill", "median_fill"],
            bfrm_norm="no"),
        SignalFile(
            format="tdf", logged="yes",
            missing_values=["no", "zero_fill", "median_fill"],
            bfrm_norm="yes")),
    Module(
        "normalize_samples_with_shiftscale",
        [ClassLabelFile,SignalFile(
            format="tdf", logged="yes",
            missing_values=["no", "zero_fill", "median_fill"],
            shiftscale_norm="no")],
        SignalFile(
            format="tdf", logged="yes",
            missing_values=["no", "zero_fill", "median_fill"],
            shiftscale_norm="yes")),
    QueryModule(
        "transfer1",
        SignalFile(
            format="tdf", logged="yes",
            missing_values=["no", "zero_fill", "median_fill"]),
        SignalFile1(
            format="tdf", logged="yes",
            missing_values=["no", "median_fill", "zero_fill"],            
                    preprocess=["unknown", "illumina", "agilent",
                                "mas5", "rma", "loess"],
                    predataset=["no", "yes"], rename_sample=["no", "yes"],
                    filter=ANYATOM,
                    dwd_norm=["no", "yes"], bfrm_norm=["no", "yes"],
                    quantile_norm=["no", "yes"],
                    shiftscale_norm=["no", "yes"], combat_norm=["no", "yes"],
            gene_center='unknown',gene_normalize='unknown',
            contents=["train0", "train1", "test", "train0,train1,test",
                        "class0", "class1", "class0,class1", "no"]
            )),
    QueryModule(
        "check_gene_center",
        SignalFile1(
            format="tdf", logged="yes",
            missing_values=["no", "zero_fill", "median_fill"],
            gene_center="unknown",gene_normalize='unknown'),
        SignalFile1(
            format="tdf", logged="yes",
            missing_values=["no", "median_fill", "zero_fill"],
            gene_center=["no", "mean", "median"],gene_normalize='unknown')),
    QueryModule(
        "check_gene_normalize",
        SignalFile1(
            format="tdf", logged="yes",
            missing_values=["no", "zero_fill", "median_fill"],
            gene_normalize="unknown"),
        SignalFile1(
            format="tdf", logged="yes",
            missing_values=["no", "median_fill", "zero_fill"],
            gene_normalize=["no", "variance", "sum_of_squares"])),
    Module(   
        "convert_signal_to_pcl",
        SignalFile1(format=['tdf']),
        SignalFile1(format='pcl')),
    Module(
        "gene_center",
        SignalFile1(
            format="pcl", logged="yes", gene_center="no",
            missing_values=["no", "zero_fill", "median_fill"],
            gene_normalize='unknown'),
        SignalFile1(
            format="tdf", logged="yes", gene_center=["mean", "median"],
            missing_values=["no", "zero_fill", "median_fill"],
            gene_normalize='unknown')),
    Module(
        "gene_normalize",
        SignalFile1(
            format="pcl", logged="yes", gene_normalize="no",
            missing_values=["no", "zero_fill", "median_fill"]),
        SignalFile1(
            format="tdf", logged="yes",
            gene_normalize=["variance", "sum_of_squares"],
            missing_values=["no", "zero_fill", "median_fill"])),
    QueryModule(
        "transfer2",
        SignalFile1(
            format="tdf", logged="yes",
            missing_values=["no", "zero_fill", "median_fill"]),
        SignalFile2(
            format="tdf", logged="yes",
            missing_values=["no", "median_fill", "zero_fill"],            
                    preprocess=["unknown", "illumina", "agilent",
                                "mas5", "rma", "loess"],
                    predataset=["no", "yes"], rename_sample=["no", "yes"],
                    filter=ANYATOM,
                    dwd_norm=["no", "yes"], bfrm_norm=["no", "yes"],
                    quantile_norm=["no", "yes"],
                    shiftscale_norm=["no", "yes"], combat_norm=["no", "yes"],
                   group_fc='no', gene_order='no', annotate="no",
                    num_features="all", platform="no",
                    duplicate_probe='no', unique_genes='no',
            gene_center=["unknown", "no", "mean", "median"],
            gene_normalize=["unknown", "no", "variance", "sum_of_squares"],
            contents=["train0", "train1", "test", "train0,train1,test",
                        "class0", "class1", "class0,class1", "no"]
            )),
    Module( 
        "filter_genes_by_fold_change_across_classes",
        [ClassLabelFile,
         SignalFile2(
             format="tdf", logged="yes",
             missing_values=["no", "zero_fill", "median_fill"],
             group_fc="no",gene_order='no', annotate="no",
             num_features="all", platform="no",
            duplicate_probe='no', unique_genes='no')],
        SignalFile2(
            format="tdf", logged="yes",
            missing_values=["no", "zero_fill", "median_fill"],
            group_fc=ANYATOM,gene_order='no', annotate="no",
            num_features="all", platform="no",
            duplicate_probe='no', unique_genes='no')),
    Module(  
        "rank_genes_by_class_neighbors",
        [SignalFile2(
            format="tdf", logged="yes",
            gene_order="no",annotate="no",
            num_features="all", platform="no",
            duplicate_probe='no', unique_genes='no'),ClassLabelFile],
        GeneListFile(gene_order="class_neighbors",
                    cn_num_neighbors=ANYATOM,
                    cn_num_perm=ANYATOM,
                    cn_user_pval=ANYATOM,  
                    cn_mean_or_median=['mean', 'median'],
                    cn_ttest_or_snr=['t_test','snr'],
                    cn_filter_data=['yes','no'],
                    cn_min_threshold=ANYATOM, 
                    cn_max_threshold=ANYATOM, 
                    cn_min_folddiff=ANYATOM, 
                    cn_abs_diff=ANYATOM)),
    Module(
         "rank_genes_by_sample_ttest",   
         [SignalFile2(format="tdf", logged="yes",
                   gene_order="no", annotate="no",
                    num_features="all", platform="no",
                    duplicate_probe='no', unique_genes='no'), ClassLabelFile],
         GeneListFile(gene_order=["t_test_p", "t_test_fdr"],
                      cn_num_neighbors=ANYATOM,
                    cn_num_perm=ANYATOM,
                    cn_user_pval=ANYATOM,  
                    cn_mean_or_median=['mean', 'median'],
                    cn_ttest_or_snr=['t_test','snr'],
                    cn_filter_data=['yes','no'],
                    cn_min_threshold=ANYATOM, 
                    cn_max_threshold=ANYATOM, 
                    cn_min_folddiff=ANYATOM, 
                    cn_abs_diff=ANYATOM)),
    Module(
         "reorder_genes",  
         [SignalFile2(format="tdf", logged="yes",
                     gene_order="no", annotate="no",
                     num_features="all", platform="no",
                     duplicate_probe='no', unique_genes='no'),
          GeneListFile(gene_order=['t_test_p', "t_test_fdr",
                                   'class_neighbors', "gene_list"])],
         SignalFile2(
             format="tdf", logged="yes", annotate="no",
             num_features="all", platform="no",
            duplicate_probe='no', unique_genes='no',
             gene_order=['t_test_p', "t_test_fdr",
                         'class_neighbors', "gene_list"])),
    Module(
         'annotate_probes',
         SignalFile2(format="tdf", logged="yes", annotate="no",
                    num_features="all", platform="no",
                    duplicate_probe='no', unique_genes='no'),
         SignalFile2(format="tdf", logged="yes", annotate="yes",
                    num_features="all", platform="no",
                    duplicate_probe='no', unique_genes='no')),
    Module(
        'remove_duplicate_genes',
        SignalFile2(format="tdf",  logged="yes", annotate="yes", unique_genes="no",
                   platform="no", duplicate_probe='no', num_features="all"),
        SignalFile2(format="tdf",  logged="yes", annotate="yes",
                   unique_genes=['average_genes', 'high_var', 'first_gene'],
                   platform="no", duplicate_probe='no', num_features="all")),
    Module(
         'select_first_n_genes',
         SignalFile2(format="tdf", logged="yes", num_features="all", platform="no",
                    duplicate_probe='no'),
         SignalFile2(format="tdf", logged="yes", num_features=ANYATOM, platform="no",
                    duplicate_probe='no')), 
     Module(
         'add_crossplatform_probeid',
         SignalFile2(format="tdf", logged="yes", platform="no",
                    duplicate_probe='no'),
         SignalFile2(format="tdf", logged="yes", platform=ANYATOM,
                    duplicate_probe='no')),
     Module(
        'remove_duplicate_probes',
        SignalFile2(format="tdf", logged="yes", duplicate_probe='no'),
        SignalFile2(format="tdf", logged="yes", duplicate_probe='high_var_probe')),
    Module(
         'select_probe_by_best_match',
         SignalFile2(format="tdf", logged="yes", duplicate_probe='no'),
         SignalFile2(format="tdf", logged="yes", duplicate_probe='closest_probe')),
    Module( 
        'convert_signal_to_gct',
        SignalFile2(format="tdf", 
                   missing_values=["no", "zero_fill", "median_fill"]),
        SignalFile2(format="gct", 
                   missing_values=["no", "zero_fill", "median_fill"])),
    Module( 
        'unlog_signal',
        SignalFile2(format="tdf", logged="yes",
                   missing_values=["no", "zero_fill", "median_fill"]),
        SignalFile2(format="tdf", logged="no",
                   missing_values=["no", "zero_fill", "median_fill"]))
    ]



if __name__ == '__main__':
    test_bie()
##    #import cProfile; cProfile.run("test_bie()")
