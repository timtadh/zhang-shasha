#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.


import unittest, os, sys, base64, itertools, random, time
import copy, collections
from random import randint, seed, shuffle

import compare

seed(os.urandom(15))

class Node(object):

    def __init__(self, label):
        self.label = label
        self.children = list()

    def addkid(self, node, before=False):
        if before:  self.children.insert(0, node)
        else:   self.children.append(node)
        return self

    def get(self, label):
        if self.label == label: return self
        for c in self.children:
            if label in c: return c.get(label)

    def iter(self):
        queue = collections.deque()
        queue.append(self)
        while len(queue) > 0:
            n = queue.popleft()
            for c in n.children: queue.append(c)
            yield n

    def __contains__(self, b):
        if isinstance(b, str) and self.label == b: return 1
        elif not isinstance(b, str) and self.label == b.label: return 1
        elif (isinstance(b, str) and self.label != b) or self.label != b.label:
            return sum(b in c for c in self.children)
        raise TypeError, "Object %s is not of type str or Node" % repr(b)

    def __eq__(self, b):
        if b is None: return False
        if not isinstance(b, Node):
            raise TypeError, "Must compare against type Node"
        return self.label == b.label

    def __ne__(self, b):
        return not self.__eq__(b)

    def __repr__(self):
        return super(Node, self).__repr__()[:-1] + " %s>" % self.label

    def __str__(self):
        s = "%d:%s" % (len(self.children), self.label)
        s = '\n'.join([s]+[str(c) for c in self.children])
        return s

tree1_nodes = ['a','b','c','d','e','f']
def tree1():
    return (
        Node("f")
            .addkid(Node("d")
                .addkid(Node("a"))
                .addkid(Node("c")
                    .addkid(Node("b"))))
            .addkid(Node("e"))
        )

tree2_nodes = ['a','b','c','d','e','f']
def tree2():
    return (
        Node("a")
            .addkid(Node("c")
                .addkid(Node("d")
                    .addkid(Node("b"))
                    .addkid(Node("e"))))
            .addkid(Node("f"))
        )

tree3_nodes = ['a','b','c','d','e','f']
def tree3():
    return (
        Node("a")
            .addkid(Node("d")
                .addkid(Node("f"))
                .addkid(Node("c")
                    .addkid(Node("b"))))
            .addkid(Node("e"))
        )

tree4_nodes = ['q','b','c','d','e','f']
def tree4():
    return (
        Node("f")
            .addkid(Node("d")
                .addkid(Node("q"))
                .addkid(Node("c")
                    .addkid(Node("b"))))
            .addkid(Node("e"))
        )

def randtree(depth=2, alpha='abcdefghijklmnopqrstuvwxyz', repeat=2, width=2):
    labels = [''.join(x) for x in itertools.product(alpha, repeat=repeat)]
    shuffle(labels)
    labels = (x for x in labels)
    root = Node("root")
    p = [root]
    c = list()
    for x in xrange(depth-1):
        for y in p:
            for z in xrange(randint(1,1+width)):
                n = Node(labels.next())
                y.addkid(n)
                c.append(n)
        p = c
        c = list()
    return root

class TestTestNode(unittest.TestCase):

    def test_contains(self):
        root = tree1()
        self.assertTrue("a" in root)
        self.assertTrue("b" in root)
        self.assertTrue("c" in root)
        self.assertTrue("d" in root)
        self.assertTrue("e" in root)
        self.assertTrue("f" in root)
        self.assertFalse("q" in root)

    def test_get(self):
        root = tree1()
        self.assertEquals(root.get("a").label, "a")
        self.assertEquals(root.get("b").label, "b")
        self.assertEquals(root.get("c").label, "c")
        self.assertEquals(root.get("d").label, "d")
        self.assertEquals(root.get("e").label, "e")
        self.assertEquals(root.get("f").label, "f")

        self.assertNotEquals(root.get("a").label, "x")
        self.assertNotEquals(root.get("b").label, "x")
        self.assertNotEquals(root.get("c").label, "x")
        self.assertNotEquals(root.get("d").label, "x")
        self.assertNotEquals(root.get("e").label, "x")
        self.assertNotEquals(root.get("f").label, "x")

        self.assertEquals(root.get("x"), None)

    def test_iter(self):
        root = tree1()
        self.assertEqual(list(x.label for x in root.iter()), ['f','d','e','a','c','b'])

class TestCompare(unittest.TestCase):
    def test_distance(self):
        trees = itertools.product([tree1(), tree2(), tree3(), tree4()], repeat=2)
        for a,b in trees:
            ab = compare.distance(a,b)
            ba = compare.distance(b,a)
            self.assertEquals(ab,ba)
            self.assertTrue((ab == 0 and a is b) or a is not b)
        trees = itertools.product([tree1(), tree2(), tree3(), tree4()], repeat=3)
        for a,b,c in trees:
            ab = compare.distance(a,b)
            bc = compare.distance(b,c)
            ac = compare.distance(a,c)
            self.assertTrue(ac <= ab + bc)

    #def test_randtree(self):
        #print randtree(5, repeat=3, width=2)

    def test_symmetry(self):
        trees = itertools.product((randtree(5, repeat=3, width=2) for x in xrange(10)), repeat=2)
        for a,b in trees:
            self.assertEquals(compare.distance(a,b), compare.distance(b,a))

    def test_nondegenercy(self):
        trees = itertools.product((randtree(5, repeat=3, width=2) for x in xrange(10)), repeat=2)
        for a,b in trees:
            d = compare.distance(a,b)
            self.assertTrue((d == 0 and a is b) or a is not b)

    def test_triangle_inequality(self):
        trees = itertools.product((randtree(5, repeat=3, width=2) for x in xrange(10)), (randtree(5, repeat=3, width=2) for x in xrange(10)), (randtree(5, repeat=3, width=2) for x in xrange(10)))
        for a,b,c in trees:

            ab = compare.distance(a,b)
            bc = compare.distance(b,c)
            ac = compare.distance(a,c)
            self.assertTrue(ac <= ab + bc)

if __name__ == '__main__':
    unittest.main()

