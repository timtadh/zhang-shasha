#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Authors: Tim Henderson and Steve Johnson
#Email: tim.tadh@hackthology.com, steve.johnson.public@gmail.com
#For licensing see the LICENSE file in the top level directory.

from test_tree import Node
import compare

def simple_trees():
    A = (
        Node("f")
            .addkid(Node("d")
                .addkid(Node("a"))
                .addkid(Node("c")
                    .addkid(Node("b"))))
            .addkid(Node("e"))
        )
    B = (
        Node("f")
            .addkid(Node("c")
                .addkid(Node("d")
                    .addkid(Node("a"))
                    .addkid(Node("b"))))
            .addkid(Node("e"))
        )
    return A, B

def test_post_traverse():
    A, B = simple_trees()
    assert (
        [n.label for n in compare.post_traverse(A)] == ['a','b','c','d','e','f']
    )
    assert (
        [n.label for n in compare.post_traverse(B)] == ['a','b','d','c','e','f']
    )


def test_nodes():
    A, B = [compare.AnnotatedTree(t) for t in simple_trees()]
    for i, n in enumerate(reversed(A.nodes)):
        assert hasattr(n, '_id')
        assert n._id == i
    for i, n in enumerate(reversed(B.nodes)):
        assert hasattr(n, '_id')
        assert n._id == i

def test_left_most_descendent():
    A, B = [compare.AnnotatedTree(t) for t in simple_trees()]
    assert A.lmds[0] == 0
    assert A.lmds[1] == 1
    assert A.lmds[2] == 1
    assert A.lmds[3] == 0
    assert A.lmds[4] == 4
    assert A.lmds[5] == 0

    assert B.lmds[0] == 0
    assert B.lmds[1] == 1
    assert B.lmds[2] == 0
    assert B.lmds[3] == 0
    assert B.lmds[4] == 4
    assert B.lmds[5] == 0

def test_keyroots():
    A, B = [compare.AnnotatedTree(t) for t in simple_trees()]
    assert A.keyroots == [2, 4, 5]
    assert B.keyroots == [1, 4, 5]
