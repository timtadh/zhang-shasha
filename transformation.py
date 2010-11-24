import tree_definition

class Transformation(object):
    """
    This class stores the sequence of operations that transform one
    tree into another.  The two trees are stored in this data
    structure.
    """

    private double totalCost;
    private ArrayList<TreeEditOperation> operationsList 
    = new ArrayList<TreeEditOperation>();
    
    def __init__(self):
        super(Transformation, self).__init__()
        self.total_cost = 0
        self.operations_list = []
    
    def get_cost(self):
        return self.total_cost
    
    def set_cost(self, _cost):
        self.total_cost = _cost
    
    def get_operations(self):
        return self.operations_list
    
