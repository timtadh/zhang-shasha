#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

import unittest, os, sys, base64, itertools, random, time, copy
import copy, collections
from random import randint, seed, shuffle

from zss import compare
from zss.test_tree import Node

seed(os.urandom(15))

def test_empty_tree_distance():
    assert compare.distance(Node(''), Node('')) == 0
    assert compare.distance(Node('a'), Node('')) == 1
    assert compare.distance(Node(''), Node('b')) == 1

def test_paper_tree():
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
    dist = compare.distance(A,B)
    assert dist == 2

def test_simplelabelchange():
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
                .addkid(Node("r")
                    .addkid(Node("b"))))
            .addkid(Node("e"))
        )
    dist = compare.distance(A,B)
    print dist
    assert dist == 3
    #print 'distance', d

def test_incorrect_behavior_regression():
    A = (
     Node("a")
       .addkid(Node("b")
         .addkid(Node("x"))
         .addkid(Node("y"))
       )
     )
    B = (
     Node("a")
       .addkid(Node("x"))
       .addkid(Node("b")
         .addkid(Node("y"))
       )
     )
    dist = compare.distance(A, B)
    print dist
    assert dist == 2

