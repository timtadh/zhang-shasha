#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Authors: Tim Henderson and Steve Johnson
#Email: tim.tadh@hackthology.com, steve.johnson.public@gmail.com
#For licensing see the LICENSE file in the top level directory.

import collections, itertools
import tree
from test_tree import Node

try:
    from editdist import distance as strdist
except ImportError:
    def strdist(a, b):
        if a == b:
            return 0
        else:
            return 1


def post_traverse(root):
    stack = list()
    pstack = list()
    stack.append(root)
    while len(stack) > 0:
        n = stack.pop()
        for c in n.children: stack.append(c)
        pstack.append(n)
    while len(pstack) > 0:
        n = pstack.pop()
        yield n

class AnotatedTree(object):

    def __init__(self, root):
        self.root = root
        self.nodes = self.idnodes(self.root)
        self.lmds = list()
        keyroots = dict()
        for i, n in enumerate(self.nodes):
            lmd = self.left_most_descendent(n)
            self.lmds.append(lmd)
            keyroots[lmd] = i
        self.keyroots = keyroots.values()
        self.keyroots.sort()

    @staticmethod
    def idnodes(root):
        def setid(n, _id):
            setattr(n, "_id", _id)
            return n
        nodes = [setid(n, i) for i, n in enumerate(post_traverse(root))]
        return nodes

    @staticmethod
    def left_most_descendent(n):
        return post_traverse(n).next()._id

def distance(A, B):
    A, B = AnotatedTree(A), AnotatedTree(B)

    for i, j in itertools.product(A.keyroots, B.keyroots):




if __name__ == '__main__':
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
    print distance(A, B)
