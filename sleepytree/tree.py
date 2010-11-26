import collections

class Tree(object):
    """
    This defines necessary operations on tree required for the tree
    algorithms in this package.  Subclasses handle the particular
    representation of the contents of the tree. This parent superclass
    looks after generic tree functionality like ordering nodes.
    """
    
    def __init__(self, root):
        self.root = root
        self.ids_to_label = {}
        self.id_tree = {}
        self.node_for_id = {}
        self.id_for_node = {}
        
        self.root_id = self.generate_ids(root, 0)
    
    def generate_ids(self, n, counter):
        child_ids = []
        for child in n.children:
            counter = self.generate_ids(child, counter)
            child_ids.append(counter)
        
        self.id_tree[counter + 1] = child_ids
        self.node_for_id[counter + 1] = n
        self.id_for_node[n] = counter + 1
        
        return counter + 1

    def get_label_for_matching(self, node_id):
        """
        This is provides the string label for the node we're matching.
        In some cases, the value of the string may depend on properties
        of the node in addition to the actual node label.
        """
        return self.node_for_id[node_id].label
    
    def is_leaf(self, node_id):
        return len(self.id_tree[node_id]) == 0
    
    def __len__(self):
        return len(self.id_tree)
    
    def __str__(self):
        self._str_recurse(self.root)
    
    def _str_recurse(self, n, indent=0):
        if n.children:
            return "  "*indent + n.label + "\n" + "\n".join([self._str_recurse(c, indent+1) for c in n.children])
        else:
            return "  "*indent + n.label + "\n".join([self._str_recurse(c, indent+1) for c in n.children])
            
    
