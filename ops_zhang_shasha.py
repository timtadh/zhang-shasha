from tree_edit_operations import *

class OpsZhangShasha(object):
    """
    This is a basic operations cost set for the Zhang and Shasha
    algorithm. All operations are 1.  If node labels match, the cost is
    0.
    """

    INSERT = 0
    DELETE = 1
    RENAME = 2
    IDENTITY = 3
    
    def __init__(self):
        super(OpsZhangShasha, self).__init__()
        self.operations = [BasicInsert(), BasicDelete(), BasicRename()]

    def get_op(self, op_id):
        """Returns the nth operation.  For convenience, the operation IDs are
        provided as named int constants."""
        return self.operations[op_id]
    
    def get_operations(self):
        return self.operations
    
