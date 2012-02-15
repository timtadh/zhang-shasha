#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Authors: Tim Henderson and Steve Johnson
#Email: tim.tadh@hackthology.com, steve.johnson.public@gmail.com
#For licensing see the LICENSE file in the top level directory.

import sys, collections, itertools
from test_tree import Node

import numpy as np

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

class AnnotatedTree(object):

    def __init__(self, root):
        def setid(n, _id):
            setattr(n, "_id", _id)
            return n

        self.root = root
        self.nodes = list() # a pre-order enumeration of the nodes in the tree
        self.lmds = list()  # left most descendents
        self.keyroots = None
            # k and k' are nodes specified in the pre-order enumeration.
            # keyroots = {k | there exists no k'>k such that lmd(k) == lmd(k')}
            # see paper for more on keyroots

        stack = list()
        pstack = list()
        stack.append((root, collections.deque()))
        j = 0
        while len(stack) > 0:
            n, anc = stack.pop()
            setid(n, j)
            for c in n.children:
                a = collections.deque(anc)
                a.appendleft(n._id)
                stack.append((c, a))
            pstack.append((n, anc))
            j += 1
        lmds = dict()
        keyroots = dict()
        i = 0
        while len(pstack) > 0:
            n, anc = pstack.pop()
            #print list(anc)
            self.nodes.append(n)
            #print n.label, [a.label for a in anc]
            if not n.children:
                lmd = i
                for a in anc:
                    if a not in lmds: lmds[a] = i
                    else: break
            else:
                try: lmd = lmds[n._id]
                except:
                    import pdb
                    pdb.set_trace()
            self.lmds.append(lmd)
            keyroots[lmd] = i
            i += 1
        self.keyroots = sorted(keyroots.values())

def distance(A, B):
    A, B = AnnotatedTree(A), AnnotatedTree(B)
    treedists = np.zeros((len(A.nodes), len(B.nodes)), int)

    def treedist(i, j):
        Al = A.lmds
        Bl = B.lmds
        An = A.nodes
        Bn = B.nodes

        m = i - Al[i] + 2
        n = j - Bl[j] + 2
        fd = forestdist = np.zeros((m,n), int)
        
        ioff = Al[i] - 1
        joff = Bl[j] - 1

        for x in xrange(1, m): # δ(l(i1)..i, θ) = δ(l(1i)..1-1, θ) + γ(v → λ)
            fd[x][0] = fd[x-1][0] + strdist(An[x-1].label, '')
        for y in xrange(1, n): # δ(θ, l(j1)..j) = δ(θ, l(j1)..j-1) + γ(λ → w)
            fd[0][y] = fd[0][y-1] + strdist('', Bn[y-1].label)

        for x in xrange(1, m): ## the plus one is for the xrange impl
            for y in xrange(1, n):
                # only need to check if x is an ancestor of i
                # and y is an ancestor of j
                if Al[i] == Al[x+ioff] and Bl[j] == Bl[y+joff]:
                    #                   +-
                    #                   | δ(l(i1)..i-1, l(j1)..j) + γ(v → λ)
                    # δ(F1 , F2 ) = min-+ δ(l(i1)..i , l(j1)..j-1) + γ(λ → w)
                    #                   | δ(l(i1)..i-1, l(j1)..j-1) + γ(v → w)
                    #                   +-
                    fd[x][y] = min(
                        fd[x-1][y] + strdist(An[x+ioff].label, ''),
                        fd[x][y-1] + strdist('', Bn[y+joff].label), 
                        fd[x-1][y-1] + strdist(An[x+ioff].label, Bn[y+joff].label)
                    )                        
                    treedists[x+ioff][y+joff] = fd[x][y]
                else:
                    #                   +-
                    #                   | δ(l(i1)..i-1, l(j1)..j) + γ(v → λ)
                    # δ(F1 , F2 ) = min-+ δ(l(i1)..i , l(j1)..j-1) + γ(λ → w)
                    #                   | δ(l(i1)..l(i)-1, l(j1)..l(j)-1)
                    #                   |                     + treedist(i1,j1)
                    #                   +-
                    p = Al[x+ioff]-1-ioff
                    q = Bl[y+joff]-1-joff
                    #print (p, q), (len(fd), len(fd[0]))
                    fd[x][y] = min(
                        fd[x-1][y] + strdist(An[x+ioff].label, ''),
                        fd[x][y-1] + strdist('', Bn[y+joff].label), 
                        fd[p][q] + treedists[x+ioff][y+joff]
                    )                        

    for i in A.keyroots:
        for j in B.keyroots:
            treedist(i,j)

    return treedists[-1][-1]


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
    d = distance(A, B)
    print
    print
    print 'distance', d
