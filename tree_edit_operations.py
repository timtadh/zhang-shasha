class TreeEditOperation(object) :
    """
    This is an abstract definition of what is needed to define a Tree
    Edit Operation.  You can create subclasses of this to meet your
    application needs if more complicated inferences on edit costs are
    required.
    """
    def __init__(self):
        super(TreeEditOperation, self).__init__()
        self.op_name = ""
    
    def get_name(self):
        return self.op_name
    
    def get_cost(self, a_node_id, b_node_id, a_tree, b_tree):
        raise NotImplementedError
    

class BasicDelete(TreeEditOperation):
    """Implements a basic delete operation with cost 1."""
    def __init__(self):
        super(BasicDelete, self).__init__()
        self.op_name = "DELETE"
    
    def get_cost(self, a_node_id, b_node_id, a_tree, b_tree):
        return 1
    

class BasicInsert(TreeEditOperation):
    """Implements a basic insert operation with cost 1."""
    def __init__(self):
        super(BasicInsert, self).__init__()
        self.op_name = "INSERT"
    
    def get_cost(self, a_node_id, b_node_id, a_tree, b_tree):
        return 1
    

class BasicRename(TreeEditOperation):
    """Implements a basic delete operation with cost 1."""
    def __init__(self):
        super(BasicRename, self).__init__()
        self.op_name = "RELABEL"
    
    def get_cost(self, a_node_id, b_node_id, a_tree, b_tree):
        a_string = a_tree.get_label_for_matching(a_node_id);
        b_string = b_tree.get_label_for_matching(b_node_id);
        a_div = a_string.rfind(":")
        b_div = b_string.rfind(":")
        
        if a_div != -1:
            a_string = a_string[0:a_div]
        if b_div != -1:
            b_string = b_string[0:b_div]
        
        if a_string == b_string:
            return 0
        else:
            return 1
    

class BasicIdentity(TreeEditOperation):
    """Implements a basic insert operation with cost 1."""
    def __init__(self):
        super(BasicIdentity, self).__init__()
        self.op_name = "IDENTITY"
    
    def get_cost(self, a_node_id, b_node_id, a_tree, b_tree):
        return 0
    
