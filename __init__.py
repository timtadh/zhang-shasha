from create_tree_helper import make_tree

from comparison_zhang_shasha import *
from ops_zhang_shasha import *

def distance(a, b):
    tree_corrector = ComparisonZhangShasha()
    return tree_corrector.find_distance(make_tree(a), make_tree(b))

if __name__ == '__main__':
    assert distance('a-b;a-c', 'a-b;a-d') == 1
    assert distance('a-b;a-c;b-e', 'a-b;a-c') == 2
    print 'Success'
