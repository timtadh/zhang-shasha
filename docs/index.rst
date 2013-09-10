Zhang-Shasha: Tree edit distance in Python
==========================================

The :py:mod:`zss` module provides a function (:py:func:`zss.distance`) that
computes the edit distance between the two given trees, as well as a small set
of utilities to make its use convenient.

If you'd like to learn more about how it works, see :ref:`references`.

Brought to you by Tim Henderson (tim.tadh@gmail.com) and Steve Johnson
(steve@steveasleep.com).

Get the source or report issues `on Github
<https://github.com/timtadh/zhang-shasha/>`_.

Installation
------------

You can get :py:mod:`zss` and its soft requirements (
:py:mod:`editdist` and :py:mod:`numpy` >= 1.7) from PyPI::

    pip install zss

Both modules are optional. :py:mod:`editdist` uses string edit distance to
compare node labels rather than a simple equal/not-equal check, and
:py:mod:`numpy` significantly speeds up the library. The only reason version
1.7 of :py:mod:`numpy` is required is that earlier versions have trouble
installing on current versions of Mac OS X.

You can install :py:mod:`zss` from the source code without dependencies in the
usual way::

    python setup.py install

If you want to build the docs, you'll need to install Sphinx >= 1.0.

Usage
-----

To compare the distance between two trees, you need:

1. A tree.
2. Another tree.
3. A node-node distance function. By default, :py:mod:`zss` compares the edit
   distance between the nodes' labels. :py:mod:`zss` currently only knows how
   to handle nodes with string labels.
4. Functions to let :py:func:`zss.simple_distance` traverse your tree.

Here is an example using the library's built-in default node structure and edit
distance function::

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

:ref:`See more examples <examples>`

.. _api:
.. include:: subsections/api.rst

.. _examples:
.. include:: subsections/examples.rst

.. _references:
.. include:: subsections/references.rst
