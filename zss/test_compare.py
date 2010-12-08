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

def test_idnodes():
    A, B = simple_trees()
    A_nodes = compare.AnotatedTree.idnodes(A)
    B_nodes = compare.AnotatedTree.idnodes(B)
    for i, n in enumerate(A_nodes):
        assert hasattr(n, '_id')
        assert n._id == i
    for i, n in enumerate(B_nodes):
        assert hasattr(n, '_id')
        assert n._id == i

def test_left_most_descendent():
    A, B = simple_trees()
    A_nodes = compare.AnotatedTree.idnodes(A)
    B_nodes = compare.AnotatedTree.idnodes(B)
    assert compare.AnotatedTree.left_most_descendent(A_nodes[0]) == 0
    assert compare.AnotatedTree.left_most_descendent(A_nodes[1]) == 1
    assert compare.AnotatedTree.left_most_descendent(A_nodes[2]) == 1
    assert compare.AnotatedTree.left_most_descendent(A_nodes[3]) == 0
    assert compare.AnotatedTree.left_most_descendent(A_nodes[4]) == 4
    assert compare.AnotatedTree.left_most_descendent(A_nodes[5]) == 0

    assert compare.AnotatedTree.left_most_descendent(B_nodes[0]) == 0
    assert compare.AnotatedTree.left_most_descendent(B_nodes[1]) == 1
    assert compare.AnotatedTree.left_most_descendent(B_nodes[2]) == 0
    assert compare.AnotatedTree.left_most_descendent(B_nodes[3]) == 0
    assert compare.AnotatedTree.left_most_descendent(B_nodes[4]) == 4
    assert compare.AnotatedTree.left_most_descendent(B_nodes[5]) == 0

def test_keyroots():
    A, B = simple_trees()
    A, B = compare.AnotatedTree(A), compare.AnotatedTree(B)
    assert A.keyroots == [2, 4, 5]
    assert B.keyroots == [1, 4, 5]
