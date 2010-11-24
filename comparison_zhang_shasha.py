"""
This is an implementation of the Zhang and Shasha algorithm as
described in [FIXME]

SWAN 2007-11-01: I'm pretty sure this code comes from:
http://www.cs.queensu.ca/TechReports/Reports/1995-372.pdf and
http://www.inf.unibz.it/dis/teaching/ATA/ata7-handout-1x1.pdf
"""

import transformation
from ops_zhang_shasha import *

def multidim_arr(*dims):
    return [multidim_arr(*dims[1:]) for i in xrange(dims[0])] if dims else 0

class ComparisonZhangShasha(object):
    """
    "Dynamic Programming" Table.
    use function setFD to access it.
    Each call to findDistance will change these tables.  But each
    call is independent (and reinitialises this) so the side effect
    has no real consequence.  ie.  There are NO public side effects.
    """
    
    def __init__(self):
        super(ComparisonZhangShasha, self).__init__()
        self.forest_distance = None
        self.distance = None
    
    def find_distance(self, a_tree, b_tree, ops):
        """
        This is initialised to be n+1 * m+1.  It should really be n*m
        but because of java's zero indexing, the for loops would
        look much more readable if the matrix is extended by one
        column and row.  So, distance[0,*] and distance[*,0] should
        be permanently zero.
        """
        self.distance = multidim_arr(a_tree.get_node_count()+1, b_tree.get_node_count()+1)

        # Preliminaries
        #      1. Find left-most leaf and key roots
        a_left_leaf = {}
        b_left_leaf = {}
        a_tree_key_roots = []
        b_tree_key_roots = []
        
        self.find_helper_tables(a_tree, a_left_leaf, a_tree_key_roots, a_tree.get_root_id())
        self.find_helper_tables(b_tree, b_left_leaf, b_tree_key_roots, b_tree.get_root_id())

        # Comparison
        for a_key_root in a_tree_key_roots:
            for b_key_root in b_tree_key_roots:
                # Re-initialise forest distance tables
                fD = {}
            
                self.set_fd(a_left_leaf[a_key_root], b_left_leaf[b_key_root], 0.0, fD)
                
                # for all descendents of aKeyroot: i
                for i in xrange(a_left_leaf[a_key_root], a_key_root+1):
                    self.set_fd(i,
                                b_left_leaf[b_key_root]-1,
                                self.get_fd(i-1, b_left_leaf[b_key_root]-1, fD)+
                                    ops.get_op(OpsZhangShasha.DELETE).get_cost(
                                        i, 0, a_tree, b_tree),
                                fD)

                # for all descendents of bKeyroot: j
                for j in xrange(b_left_leaf[b_key_root], b_key_root+1):
                    self.set_fd(a_left_leaf[a_key_root]-1,
                                j, 
                                self.get_fd(a_left_leaf[a_key_root]-1, j-1, fD)+
                                    ops.get_op(OpsZhangShasha.INSERT).get_cost(
                                        0, j, a_tree, b_tree), 
                                fD)
                
                # for all descendents of aKeyroot: i
                for i in xrange(a_left_leaf[a_key_root], a_key_root+1):
                    for j in xrange(b_left_leaf[b_key_root], b_key_root+1):
                        # This min compares del vs ins
                        minimum = min(
                            # Option 1: Delete node from a_tree
                            self.get_fd(i-1, j, fD) + 
                                ops.get_op(OpsZhangShasha.DELETE).get_cost(i, 0, a_tree, b_tree),
                             
                            # Option 2: Insert node into b_tree
                            self.get_fd(i, j-1, fD) +
                                ops.get_op(OpsZhangShasha.INSERT).get_cost(0, j, a_tree, b_tree)
                        )
                        
                        if a_left_leaf[i] == a_left_leaf[a_key_root] and \
                        b_left_leaf[j] == b_left_leaf[b_key_root]:
                            self.distance[i][j] = min(
                                minimum,
                                self.get_fd(i-1, j-1, fD) +
                                    ops.get_op(OpsZhangShasha.RENAME).get_cost(i, j, a_tree,b_tree)
                            )
                            self.set_fd(i, j, self.distance[i][j], fD)
                        else:
                            self.set_fd(i, j, 
                                        min(minimum, 
                                            self.get_fd(a_left_leaf[i]-1, 
                                                        b_left_leaf[j], fD)
                                        ),
                                        fD
                            )
        transform = transformation.Transformation()
        transform.set_cost(self.distance[a_tree.get_node_count()][b_tree.get_node_count()])
        return transform;

    def find_helper_tables(self, some_tree, leftmost_leaves, keyroots, a_node_id):
        """
        The initiating call should be to the root node of the tree.
        It fills in an nxn (hash) table of the leftmost leaf for a
        given node.  It also compiles an array of key roots. The
        integer values IDs must come from the post-ordering of the
        nodes in the tree.
        """
        self.find_helper_tables_recurse(some_tree, leftmost_leaves, keyroots, a_node_id);

        # add root to keyroots
        keyroots.append(a_node_id);

        # add boundary nodes
        leftmost_leaves[0] = 0
    
    def find_helper_tables_recurse(self, some_tree, leftmost_leaves, keyroots, a_node_id):
        # If this is a leaf, then it is the leftmost leaf
        if some_tree.is_leaf(a_node_id):
            leftmost_leaves[a_node_id] = a_node_id
        else:
            seen_leftmost = False
            for child in some_tree.get_children_ids(a_node_id):
                self.find_helper_tables_recurse(some_tree, leftmost_leaves, keyroots, child)
                if not seen_leftmost:
                    leftmost_leaves[a_node_id] = leftmost_leaves[child]
                    seen_leftmost = True
                else:
                    keyroots.append(child)

    def get_fd(self, a, b, forest_distance):
        """This returns the value in the cell of the ForestDistance table"""
        
        if not forest_distance.has_key(a):
            forest_distance[a] = {}
        
        rows = forest_distance[a]
        
        if not rows.has_key(b):
            rows[b] = 0.0
        
        return rows[b]
    
    def set_fd(self, a, b, a_value, forest_distance):
        if not forest_distance.has_key(a):
            forest_distance[a] = {}
        rows = forest_distance[a]
        rows[b] = a_value
    
