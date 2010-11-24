import tree_definition

class BasicTree(tree_definition.TreeDefinition):
    """
    This defines are tree.  The tree contains labelled nodes.  Labels
    must be unique.  Sibling order is defined by the order in which
    edges are added to a parent node.

    Populating the tree is done at construction time, which must also
    specify what type of tree node traversal to number all the nodes.
    Default is POSTORDER
    """
    
    def __init__(self, ts=None, _root=None, o=0):
        """This takes a |e| x 2 array of string, where |e| is the number
        of edges."""
        super(BasicTree, self).__init__()
        self.set_root(_root)
        self.tree_structure = ts or {}
        self.order_nodes(o)
    
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
    
