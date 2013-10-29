Zhang-Shasha: Tree edit distance in Python
------------------------------------------

The ``zss`` module provides a function (``zss.distance``) that
computes the edit distance between the two given trees, as well as a small set
of utilities to make its use convenient.

If you'd like to learn more about how it works, see References below.

Brought to you by Tim Henderson (tim.tadh@gmail.com)
and Steve Johnson (steve@steveasleep.com).

`Read the full documentation for more information.
<http://zhang-shasha.readthedocs.org/en/latest/>`_

Installation
------------

You can get ``zss`` and its soft requirements (
``editdist`` and ``numpy`` >= 1.7) from PyPI::

    pip install zss

Both modules are optional. ``editdist`` uses string edit distance to
compare node labels rather than a simple equal/not-equal check, and
``numpy`` significantly speeds up the library. The only reason version
1.7 of ``numpy`` is required is that earlier versions have trouble
installing on current versions of Mac OS X.

You can install ``zss`` from the source code without dependencies in the
usual way::

    python setup.py install

If you want to build the docs, you'll need to install Sphinx >= 1.0.

Usage
-----

To compare the distance between two trees, you need:

1. A tree.
2. Another tree.
3. A node-node distance function. By default, ``zss`` compares the edit
   distance between the nodes' labels. ``zss`` currently only knows how
   to handle nodes with string labels.
4. Functions to let ``zss.distance`` traverse your tree.

Here is an example using the library's built-in default node structure and edit
distance function

.. code-block:: python

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


Specifying Custom Tree Formats
------------------------------

Specifying custom tree formats and distance metrics is easy. The
``zss.simple_distance`` function takes 3 extra parameters besides the two tree
to compare:

1. ``get_children`` - a function to retrieve a list of children from a node.
2. ``get_label`` - a function to retrieve the label object from a node.
3. ``label_dist`` - a function to compute the non-negative integer distance
   between two node labels.

Example
^^^^^^^

.. code-block:: python

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


References
----------

The algorithm used by ``zss`` is taken directly from the original paper by
Zhang and Shasha. If you would like to discuss the paper, or the the tree edit
distance problem (we have implemented a few other algorithms as well) please
email the authors.

`approxlib <http://www.inf.unibz.it/~augsten/src/>`_ by Dr. Nikolaus Augstent
contains a good Java implementation of Zhang-Shasha as well as a number of
other useful tree distance algorithms.

`Kaizhong Zhang and Dennis Shasha. Simple fast algorithms for the editing distance between trees and related problems. SIAM Journal of Computing, 18:1245–1262, 1989.`__ (the original paper)

__ http://www.grantjenks.com/wiki/_media/ideas:simple_fast_algorithms_for_the_editing_distance_between_tree_and_related_problems.pdf

`Slide deck overview of Zhang-Shasha <http://www.inf.unibz.it/dis/teaching/ATA/ata7-handout-1x1.pdf>`_

`Another paper describing Zhang-Shasha <http://research.cs.queensu.ca/TechReports/Reports/1995-372.pdf>`_
