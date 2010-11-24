import basic_tree

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
    test_tree['a'] = ['b', 'c'];
    test_tree['b'] = []

    # c-[d, e, f]
    
    test_tree['c'] = ['d', 'e', 'f']
    test_tree['d'] = []
    test_tree['e'] = []
    test_tree['f'] = []
    
    a_basic_tree = basic_tree.BasicTree(test_tree, 'a', basic_tree.BasicTree.POSTORDER)
    
    print "Static test tree:"
    print "Number of nodes: %d" % a_basic_tree.get_node_count()
    print "Tree:"
    print a_basic_tree

    # //Now test CreateTreeHelper
    # TreeDefinition bBasicTree = null;

    # if (argv.length == 1) {
    #     bBasicTree = CreateTreeHelper.makeTree(argv[0]);
    #     System.out.println("Input Tree: \n");
    #     System.out.println("The number of nodes are: "+
    #              bBasicTree.getNodeCount());
    #     System.out.println("The tree is: \n"+bBasicTree);
