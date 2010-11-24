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
    
    def set_root(self, _root):
        self.root = _root
    
    def get_root(self):
        return self.root
    
    def get_root_id(self):
        return self.label_to_ids[self.root]
    
    def set_order(self, order):
        self.chosen_order = order
    
    def get_order(self):
        return self.chosen_order
    
    def order_nodes(self, ordering):
        if ordering == self.POSTORDER:
            self.set_post_ordering(0, self.root)
            self.set_order(self.POSTORDER)
        else:
            self.set_pre_ordering(0, self.root)
            self.set_order(self.PREORDER)
        
        # Create an int-indexed version of the tree
        for parent in self.get_nodes():
            # print 'indexing', parent, self.get_node_id(parent)
            indexed_children = []   #int
            for child in self.get_children(parent):
                # print '   ', child, self.get_node_id(child)
                indexed_children.append(self.get_node_id(child))
            self.tree_structure_ids[self.get_node_id(parent)] = indexed_children
            # print self.tree_structure_ids
    
    def set_post_ordering(self, counter, a_node_label):
        internal_counter = counter
        for child in self.get_children(a_node_label):
            internal_counter = self.set_post_ordering(internal_counter, child)
        
        # set new nodeID for this node (set to counter+1)
        self.put_label(internal_counter+1, a_node_label)
        self.put_node_id(a_node_label, internal_counter+1)

        return internal_counter+1

    def get_label_for_matching(self, node_id):
        """
        This is provides the string label for the node we're matching.
        In some cases, the value of the string may depend on properties
        of the node in addition to the actual node label.
        """
        return self.get_label(node_id)
    
    def get_label(self, node_id):
        return self.ids_to_label[node_id]
    
    def get_node_id(self, node_label):
        return self.label_to_ids[node_label]
        
    def put_label(self, node_id, node_label):
        self.ids_to_label[node_id] = node_label
    
    def put_node_id(self, node_label, node_id):
        self.label_to_ids[node_label] = node_id

    def get_nodes(self):
        """returns a collection of nodes referred to by their original
        (unique) node label."""
        raise NotImplementedError
    
    def get_children(self, a_node_label):
        raise NotImplementedError
    
    def get_children_ids(self, node_id):
        return self.tree_structure_ids[node_id]
    
    def is_leaf(self, node_id):
        return len(self.get_children_ids(node_id)) == 0
    
    def get_node_count(self):
        return len(self.tree_structure_ids)
    
    def __str__(self):
        raise NotImplementedError
    
