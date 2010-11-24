"""
This is an implementation of the Zhang and Shasha algorithm as
described in [FIXME]

SWAN 2007-11-01: I'm pretty sure this code comes from:
http://www.cs.queensu.ca/TechReports/Reports/1995-372.pdf and
http://www.inf.unibz.it/dis/teaching/ATA/ata7-handout-1x1.pdf
"""

import collections
from editdist import distance as strdist
import tree

INSERT = 0
DELETE = 1
RENAME = 2
IDENTITY = 3

def distance(a, b):
    return find_distance_raw(tree.convert_tree(a), tree.convert_tree(b))

def multidim_arr(*dims):
    return [multidim_arr(*dims[1:]) for i in xrange(dims[0])] if dims else 0

def default_replace_cost_func(a_node_id, b_node_id, a_tree, b_tree):
    a_string = a_tree.get_label_for_matching(a_node_id)
    b_string = b_tree.get_label_for_matching(b_node_id)
    
    return strdist(a_string, b_string)

def find_distance_raw(a_tree, b_tree, ops=None):
    """
    This is initialised to be n+1 * m+1.  It should really be n*m
    but because of java's zero indexing, the for loops would
    look much more readable if the matrix is extended by one
    column and row.  So, distance[0,*] and distance[*,0] should
    be permanently zero.
    """
    ops = ops or {
        INSERT: lambda *args: 1,
        DELETE: lambda *args: 1,
        RENAME: default_replace_cost_func
    }
    
    distance = multidim_arr(len(a_tree)+1, len(b_tree)+1)

    # Preliminaries
    #      1. Find left-most leaf and key roots
    a_left_leaf = {}
    b_left_leaf = {}
    a_tree_key_roots = []
    b_tree_key_roots = []
    
    find_helper_tables(a_tree, a_left_leaf, a_tree_key_roots, a_tree.get_root_id())
    find_helper_tables(b_tree, b_left_leaf, b_tree_key_roots, b_tree.get_root_id())
    
    # Comparison
    for a_key_root in a_tree_key_roots:
        for b_key_root in b_tree_key_roots:
            # Re-initialise forest distance tables
            fD = collections.defaultdict(lambda: collections.defaultdict(lambda: 0.0))
            
            fD[a_left_leaf[a_key_root]][b_left_leaf[b_key_root]] = 0.0
            
            # for all descendents of aKeyroot: i
            for i in xrange(a_left_leaf[a_key_root], a_key_root+1):
                new_val = fD[i-1][b_left_leaf[b_key_root]-1] + \
                          ops[DELETE](i, 0, a_tree, b_tree)
                fD[i][b_left_leaf[b_key_root]-1] = new_val

            # for all descendents of bKeyroot: j
            for j in xrange(b_left_leaf[b_key_root], b_key_root+1):
                new_val = fD[a_left_leaf[a_key_root]-1][j-1] + \
                          ops[INSERT](0, j, a_tree, b_tree)
                fD[a_left_leaf[a_key_root]-1][j] = new_val
            
            # for all descendents of aKeyroot: i
            for i in xrange(a_left_leaf[a_key_root], a_key_root+1):
                for j in xrange(b_left_leaf[b_key_root], b_key_root+1):
                    # This min compares del vs ins
                    minimum = min(
                        # Option 1: Delete node from a_tree
                        fD[i-1][j] + ops[DELETE](i, 0, a_tree, b_tree),
                        # Option 2: Insert node into b_tree
                        fD[i][j-1] + ops[INSERT](0, j, a_tree, b_tree)
                    )
                    
                    if a_left_leaf[i] == a_left_leaf[a_key_root] and \
                    b_left_leaf[j] == b_left_leaf[b_key_root]:
                        distance[i][j] = min(
                            minimum,
                            fD[i-1][j-1] + ops[RENAME](i, j, a_tree,b_tree)
                        )
                        fD[i][j] = distance[i][j]
                    else:
                        fD[i][j] = min(minimum, fD[a_left_leaf[i]-1][b_left_leaf[j]])
    return distance[len(a_tree)][len(b_tree)]

def find_helper_tables(some_tree, leftmost_leaves, keyroots, a_node_id):
    """
    The initiating call should be to the root node of the tree.
    It fills in an nxn (hash) table of the leftmost leaf for a
    given node.  It also compiles an array of key roots. The
    integer values IDs must come from the post-ordering of the
    nodes in the tree.
    """
    find_helper_tables_recurse(some_tree, leftmost_leaves, keyroots, a_node_id)

    # add root to keyroots
    keyroots.append(a_node_id)

    # add boundary nodes
    leftmost_leaves[0] = 0

def find_helper_tables_recurse(some_tree, leftmost_leaves, keyroots, a_node_id):
    # If this is a leaf, then it is the leftmost leaf
    if some_tree.is_leaf(a_node_id):
        leftmost_leaves[a_node_id] = a_node_id
    else:
        seen_leftmost = False
        for child in some_tree.get_children_ids(a_node_id):
            find_helper_tables_recurse(some_tree, leftmost_leaves, keyroots, child)
            if not seen_leftmost:
                leftmost_leaves[a_node_id] = leftmost_leaves[child]
                seen_leftmost = True
            else:
                keyroots.append(child)
