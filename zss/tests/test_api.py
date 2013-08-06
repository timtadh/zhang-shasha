#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@gmail.com
#For licensing see the LICENSE file in the top level directory.

from zss import compare

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

def test_paper_tree():
    Node = WeirdNode
    A = (
      Node("f")
        .addkid(Node("d")
          .addkid(Node("a"))
          .addkid(Node("c")
            .addkid(Node("b"))
          )
        )
        .addkid(Node("e"))
    )
    B = (
      Node("f")
        .addkid(Node("c")
          .addkid(Node("d")
            .addkid(Node("a"))
            .addkid(Node("b"))
          )
        )
        .addkid(Node("e"))
    )
    #print A
    #print
    #print B
    dist = compare.distance(A,B,WeirdNode.get_children, WeirdNode.get_label,
        weird_dist)
    assert dist == 20


