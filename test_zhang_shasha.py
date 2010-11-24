import create_tree_helper

from comparison_zhang_shasha import *
from ops_zhang_shasha import *

if __name__ == '__main__':
    
    a_tree = create_tree_helper.make_tree('a-b;a-c')
    b_tree = create_tree_helper.make_tree('a-b;a-d')

    tree_corrector = ComparisonZhangShasha()
    costs = OpsZhangShasha()
    transform = tree_corrector.find_distance(a_tree, b_tree, costs)
    
    print transform.get_cost()
