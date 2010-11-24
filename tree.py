import collections

class TreeDefinition(object):
    """
    This defines necessary operations on tree required for the tree
    algorithms in this package.  Subclasses handle the particular
    representation of the contents of the tree. This parent superclass
    looks after generic tree functionality like ordering nodes.
    """
    
    POSTORDER = 0
    PREORDER = 1
    
    def __init__(self):
        self.chosen_order = self.POSTORDER
        self.root = ""
        self.ids_to_label = {}  #int -> string
        self.label_to_ids = {}  #string -> int
        self.tree_structure_ids = {}    #int -> [int]
        
        self.get_label = self.ids_to_label.__getitem__
        self.get_node_id = self.label_to_ids.__getitem__
        self.get_children_ids = self.tree_structure_ids.__getitem__
    
    def get_root_id(self):
        return self.label_to_ids[self.root]
    
    def order_nodes(self, ordering):
        if ordering == self.POSTORDER:
            self.set_post_ordering(0, self.root)
            self.order = self.POSTORDER
        else:
            self.set_pre_ordering(0, self.root)
            self.order = self.PREORDER
        
        self.index_children(self.root)
    
    def index_children(self, n):
        indexed_children = []
        for child in self.get_children(n):
            indexed_children.append(self.get_node_id(child))
            self.index_children(n)
        self.tree_structure_ids[self.get_node_id(n)] = indexed_children
    
    def set_post_ordering(self, counter, a_node_label):
        internal_counter = counter
        for child in self.get_children(a_node_label):
            internal_counter = self.set_post_ordering(internal_counter, child)
        
        # set new nodeID for this node (set to counter+1)
        self.ids_to_label[internal_counter+1] = a_node_label
        self.label_to_ids[a_node_label] = internal_counter+1

        return internal_counter+1

    def get_label_for_matching(self, node_id):
        """
        This is provides the string label for the node we're matching.
        In some cases, the value of the string may depend on properties
        of the node in addition to the actual node label.
        """
        return self.get_label(node_id)

    def get_nodes(self):
        """returns a collection of nodes referred to by their original
        (unique) node label."""
        raise NotImplementedError
    
    def get_children(self, a_node_label):
        raise NotImplementedError
    
    def is_leaf(self, node_id):
        return len(self.get_children_ids(node_id)) == 0
    
    def __len__(self):
        return len(self.tree_structure_ids)
    
    def __str__(self):
        raise NotImplementedError
    

class BasicTree(TreeDefinition):
    """
    This defines are tree.  The tree contains labelled nodes.  Labels
    must be unique.  Sibling order is defined by the order in which
    edges are added to a parent node.

    Populating the tree is done at construction time, which must also
    specify what type of tree node traversal to number all the nodes.
    Default is POSTORDER
    """
    
    def __init__(self, ts=None, root=None, o=0):
        """This takes a |e| x 2 array of string, where |e| is the number
        of edges."""
        super(BasicTree, self).__init__()
        self.root = root
        self.tree_structure = ts or {}
        self.order_nodes(o)
        
        self.get_nodes = self.tree_structure.keys
        self.get_children = self.tree_structure.__getitem__
    
    def get_nodes(self):
        return self.tree_structure.keys()
    
    def get_children(self, node_label):
        return self.tree_structure[node_label]
    
    def __str__(self):
        root_id = self.get_root_id()
        def child_string(child):
            return " - %s (%d)\n" % (str(child), self.get_node_id(child))
        
        def children_string_for_i(i):
            return ''.join(child_string(child) for child in self.get_children(self.get_label(i)))
        
        def i_string(i):
            return "%s (%d)\n%s" % (self.get_label(i), i, children_string_for_i(i))
        
        return ''.join(i_string(i) for i in xrange(root_id, 0, -1))
    

def convert_tree(root):
    t = convert_tree_recurse(collections.defaultdict(list), root)
    return BasicTree(t, root, BasicTree.POSTORDER)

def convert_tree_recurse(t, n):
    for c in n.children:
        t[n.label].append(c.label)
        t[c.label]
        t = convert_tree_recurse(t, c)
    return t
