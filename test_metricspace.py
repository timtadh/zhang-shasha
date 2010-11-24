#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.


import unittest, os, sys, base64, itertools, random, time
import copy, collections
from random import randint, seed, shuffle

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

class TestKlein(unittest.TestCase):

    def test_flatten(self):
        self.assertEquals(klein.flatten([1,2,[3,[4,5],6,[7,[8,9,[0,[1,[2,[3]]]]]]]]), [1,2,3,4,5,6,7,8,9,0,1,2,3])

    def test_opinjection(self):
        Node.__sub__ = lambda self, b: Node("xyz")
        n1 = Node("1")
        n2 = Node("2")
        self.assertTrue(n1 - n2)

    def test_removenode1(self):
        def __sub__(self, b):
            a = copy.deepcopy(self)
            return klein.remove_node(a, b)
        for c in tree1_nodes:
            root = tree1()
            root.__class__.remove_node = klein.remove_node
            root.__class__.__sub__ = __sub__
            toremove = root.get(c)
            roots = root.remove_node(toremove)
            for n in tree1_nodes:
                if n == c: self.assertFalse(sum(n in r for r in roots))
                else: self.assertTrue(sum(n in r for r in roots))

        for c in tree1_nodes:
            root = tree1()
            toremove = root.get(c)
            new_roots = root - toremove
            for n in tree1_nodes:
                if n == c: self.assertFalse(sum(n in r for r in new_roots))
                else: self.assertTrue(sum(n in r for r in new_roots))
                self.assertTrue(n in root)

    def test_removetree1(self):
        tree1_nodes.sort()
        for c in tree1_nodes:
            root = tree1()
            root.__class__.remove_tree = klein.remove_tree
            toremove = root.get(c)
            non_existant = [c.label for c in toremove.iter()]
            non_existant.sort()
            roots = root.remove_tree(toremove)
            for n in tree1_nodes:
                if roots == None: self.assertEquals(tree1_nodes, non_existant)
                elif n in non_existant: self.assertFalse(sum(n in r for r in roots))
                else: self.assertTrue(sum(n in r for r in roots))


    def test_distance(self):
        trees = itertools.product([tree1(), tree2(), tree3(), tree4()], repeat=2)
        for a,b in trees:
            ab = klein.distance(a,b)
            ba = klein.distance(b,a)
            self.assertEquals(ab,ba)
            self.assertTrue((ab == 0 and a is b) or a is not b)
        trees = itertools.product([tree1(), tree2(), tree3(), tree4()], repeat=3)
        for a,b,c in trees:
            ab = klein.distance(a,b)
            bc = klein.distance(b,c)
            ac = klein.distance(a,c)
            self.assertTrue(ac <= ab + bc)

    def test_symmetry(self):
        trees = itertools.product((randtree(2, repeat=2, width=2) for x in xrange(2)), repeat=2)
        for a,b in trees:
            self.assertEquals(klein.distance(a,b), klein.distance(b,a))

    def test_nondegenercy(self):
        trees = itertools.product((randtree(2, repeat=2, width=2) for x in xrange(2)), repeat=2)
        for a,b in trees:
            d = klein.distance(a,b)
            self.assertTrue((d == 0 and a is b) or a is not b)

    def test_triangle_inequality(self):
        trees = itertools.product((randtree(3, repeat=2, width=2) for x in xrange(1)), (randtree(3, repeat=2, width=2) for x in xrange(1)), (randtree(3, repeat=2, width=2) for x in xrange(1)))
        for a,b,c in trees:

            ab = klein.distance(a,b)
            bc = klein.distance(b,c)
            ac = klein.distance(a,c)
            self.assertTrue(ac <= ab + bc)

if __name__ == '__main__':
    unittest.main()

