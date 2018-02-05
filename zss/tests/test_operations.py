#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Erick Fonseca
#Email: erickrfonseca@gmail.com
#For licensing see the LICENSE file in the top level directory.

from __future__ import absolute_import

from zss import simple_distance, Node, Operation

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
C = (
    Node("a")
        .addkid(Node("c")
                .addkid(Node("d")
                        .addkid(Node("b"))
                        .addkid(Node("e"))))
        .addkid(Node("f"))
)


def all_equal(list1, list2):
    if len(list1) != len(list2):
        return False

    for item1, item2 in zip(list1, list2):
        if item1 != item2:
            return False

    return True


def test_ab():
    expected_ops = [Operation(Operation.match, Node("a"), Node("a")),
                    Operation(Operation.match, Node("b"), Node("b")),
                    Operation(Operation.remove, Node("c"), None),
                    Operation(Operation.match, Node("d"), Node("d")),
                    Operation(Operation.insert, None, Node("c")),
                    Operation(Operation.match, Node("e"), Node("e")),
                    Operation(Operation.match, Node("f"), Node("f"))]
    cost, ops = simple_distance(A, B, return_operations=True)
    assert ops == expected_ops


def test_ac():
    expected_ops = [Operation(Operation.remove, Node("a"), None),
                    Operation(Operation.match, Node("b"), Node("b")),
                    Operation(Operation.insert, None, Node("e")),
                    Operation(Operation.insert, None, Node("d")),
                    Operation(Operation.match, Node("c"), Node("c")),
                    Operation(Operation.remove, Node("d"), None),
                    Operation(Operation.update, Node("e"), Node("f")),
                    Operation(Operation.update, Node("f"), Node("a"))]
    cost, ops = simple_distance(A, C, return_operations=True)
    assert ops == expected_ops


def test_bc():
    expected_ops = [Operation(Operation.remove, Node("a"), None),
                    Operation(Operation.match, Node("b"), Node("b")),
                    Operation(Operation.insert, None, Node("e")),
                    Operation(Operation.match, Node("d"), Node("d")),
                    Operation(Operation.match, Node("c"), Node("c")),
                    Operation(Operation.update, Node("e"), Node("f")),
                    Operation(Operation.update, Node("f"), Node("a"))]
    cost, ops = simple_distance(B, C, return_operations=True)
    assert ops == expected_ops
