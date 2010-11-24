import collections
import tree
"""
This takes a String describing a tree and converts it into a
TreeDefinition.  The format of the string is a series of edges
represented as pairs of string separated by semi-colons.  Each
pair is comma separated.  The first substring in the pair is
the parent, the second is the child.  The first edge parent
must be the root of the tree.  

For example: "a-b;a-c;c-d;c-e;c-f;"
"""

def make_tree(tree_spec, root_id=None):
    """
    This takes a String describing a tree and converts it into a
    TreeDefinition.  The format of the string is a series of edges
    represented as pairs of string separated by semi-colons.  Each
    pair is comma separated.  The first substring in the pair is
    the parent, the second is the child.  

    For example: "a-b;a-c;c-d;c-e;c-f;"
    """
    a_tree = collections.defaultdict(list)
    root = root_id
    
    for edge in tree_spec.split(';'):
        nodes = edge.split('-')
        a_tree[nodes[0]].append(nodes[1])
        a_tree[nodes[1]]
        root = root or nodes[0]
    
    return tree.BasicTree(a_tree, root, tree.BasicTree.POSTORDER)
