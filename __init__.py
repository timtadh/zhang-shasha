from create_tree_helper import make_tree
from compare import find_distance_raw

def distance(a, b):
    return find_distance_raw(make_tree(a), make_tree(b))

if __name__ == '__main__':
    trees = [
        'a-b',
        'a-b;a-c',
        'a-b;a-d',
        'a-b;a-c;b-e'
    ]
    for t in trees:
        print t
        print distance(t, t)
        assert distance(t, t) == 0
    assert distance(trees[1], trees[2]) == 1
    assert distance(trees[1], trees[3]) == 2
    print 'Success'
