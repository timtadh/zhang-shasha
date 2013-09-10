Examples
========

Tree Format and Usage
---------------------

By default, the tree is represented by objects referencing each other. Each
node is represented by an object with the attributes ``label`` and
``children``, where ``label`` is a string and ``children`` is a list of other
objects. However, all of this is configurable by passing in functions. Here is
how to use the default API:

To find the distance between two object trees, call
``zss.simple_distance(root1, root2)``.

The object format is used by the tests and is probably the easiest to work
with.

A simple example
^^^^^^^^^^^^^^^^

::

    from zss import simple_distance, Node

    # Node(label, children)
    # a---> b
    #  \--> c
    c = Node('c', [])
    b = Node('b', [])
    a = Node('a', [b, c])
    assert simple_distance(a, a) == 0

    # a---> c
    a2 = Node('a', [Node('c', [])])
    assert simple_distance(a, a2) == 1

Another Example:
^^^^^^^^^^^^^^^^

::

    from zss import simple_distance, Node

    A = (
        Node("f")
            .addkid(Node("a")
                .addkid(Node("h"))
                .addkid(Node("c")
                    .addkid(Node("l"))))
            .addkid(Node("e"))
        )
    B = (
        Node("f")
            .addkid(Node("a")
                .addkid(Node("d"))
                .addkid(Node("c")
                    .addkid(Node("b"))))
            .addkid(Node("e"))
        )
    assert simple_distance(A, B) == 2


See ``test_metricspace.py`` for more examples.


Specifying Custom Tree Formats
------------------------------

Specifying custom tree formats and distance metrics is easy. The
:py:func:`zss.simple_distance` function takes 3 extra parameters besides the
two tree to compare:

1. ``get_children`` - a function to retrieve a list of children from a node.
2. ``get_label`` - a function to retrieve the label object from a node.
3. ``label_dist`` - a function to compute the non-negative integer distance
   between two node labels.

Example
^^^^^^^

::

    #!/usr/bin/env python

    import zss

    try:
        from editdist import distance as strdist
    except ImportError:
        def strdist(a, b):
            if a == b:
                return 0
            else:
                return 1

    def weird_dist(A, B):
        return 10*strdist(A, B)

    class WeirdNode(object):

        def __init__(self, label):
            self.my_label = label
            self.my_children = list()

        @staticmethod
        def get_children(node):
            return node.my_children

        @staticmethod
        def get_label(node):
            return node.my_label

        def addkid(self, node, before=False):
            if before:  self.my_children.insert(0, node)
            else:   self.my_children.append(node)
            return self

    A = (
    WeirdNode("f")
        .addkid(WeirdNode("d")
        .addkid(WeirdNode("a"))
        .addkid(WeirdNode("c")
            .addkid(WeirdNode("b"))
        )
        )
        .addkid(WeirdNode("e"))
    )
    B = (
    WeirdNode("f")
        .addkid(WeirdNode("c")
        .addkid(WeirdNode("d")
            .addkid(WeirdNode("a"))
            .addkid(WeirdNode("b"))
        )
        )
        .addkid(WeirdNode("e"))
    )

    dist = zss.simple_distance(
        A, B, WeirdNode.get_children, WeirdNode.get_label, weird_dist)

    print dist
    assert dist == 20
