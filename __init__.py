from create_tree_helper import make_tree
from compare import find_distance_raw

def distance(a, b):
    return find_distance_raw(make_tree(a), make_tree(b))

if __name__ == '__main__':
    assert distance('a-b;a-c', 'a-b;a-d') == 1
    assert distance('a-b;a-c;b-e', 'a-b;a-c') == 2
    print 'Success'
