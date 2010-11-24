import tree, create_tree_helper

def dictprint(items):
    print
    print '---'
    for k, v in items.viewitems():
        print ' *', k, ':', v

if __name__ == '__main__':
    print "Testing tree definition"
    
    # A Tree
    test_tree = {}

    # a-[b,c]
    test_tree['a'] = ['b', 'c']
    test_tree['b'] = []

    # c-[d, e, f]
    
    test_tree['c'] = ['d', 'e', 'f']
    test_tree['d'] = []
    test_tree['e'] = []
    test_tree['f'] = []
    
    a_basic_tree = tree.BasicTree(test_tree, 'a', tree.BasicTree.POSTORDER)
    
    print "Static test tree:"
    print "Number of nodes: %d" % a_basic_tree.get_node_count()
    print "Tree:"
    print a_basic_tree
    
    b_basic_tree = create_tree_helper.make_tree('a-b;a-c;c-d;c-e;c-f')
    
    print "Parsed tree:"
    print b_basic_tree
