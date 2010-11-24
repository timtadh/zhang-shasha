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
    a_tree = {}
    root = root_id
    
    for edge in tree_spec.split(';'):
        nodes = edge.split('-')
        add_edge(nodes[0], nodes[1], a_tree)
        root = root or nodes[0]
    
    return tree.BasicTree(a_tree, root, tree.BasicTree.POSTORDER)

def add_edge(parent_label, child_label, tree_structure):
    """This adds the edge (and nodes if necessary) to the tree
    definition."""
    
    # Add Parent node, edge and child
    if not tree_structure.has_key(parent_label):
        tree_structure[parent_label] = []
    tree_structure[parent_label].append(child_label)

    # Add child if not already there
    if not tree_structure.has_key(child_label):
        tree_structure[child_label] = []
