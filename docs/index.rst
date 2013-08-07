Zhang-Shasha: Tree edit distance in Python
==========================================

The :py:mod:`zss` module provides a function (:py:func:`zss.distance`) that
computes the edit distance between the two given trees, as well as a small set
of utilities to make its use convenient.

If you'd like to learn more about how it works, see :doc:`references`.

Installation
------------

::

    pip install zss

Usage
-----

:doc:`Complete yet short API <usage>`

To compare the distance between two trees, you need:

1. A tree.
2. Another tree.
3. A node-node distance function. By default, :py:mod:`zss` compares the edit
   distance between the nodes' labels. :py:mod:`zss` currently only knows how
   to handle nodes with string labels.
4. Functions to let :py:func:`zss.distance` traverse your tree.

Here is an example using the library's built-in default node structure and edit
distance function::

    from zss import distance, Node

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
    assert distance(A, B) == 2

:doc:`See more examples <examples>`

Table of Contents
-----------------

.. toctree::
   :maxdepth: 2

   usage
   examples
   references
