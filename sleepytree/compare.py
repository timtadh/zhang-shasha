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
    treedists = dict()
    forestdists = dict()
    def forestdist(a, b):
        key = (a, b)
        if key in forestdists:
            #print 'memoized', key
            return forestdists[key]
        #print forestdists

        Al = A.lmds
        Bl = B.lmds
        An = A.nodes
        Bn = B.nodes


        if a[0] >= a[1] and b[0] >= b[1]: # δ(θ, θ) = 0
            #print 'null', a, b
            fd = 0
        elif b[0] >= b[1]: # δ(l(i1)..i, θ) = δ(l(1i)..1-1, θ) + γ(v → λ)
            #print 'insert', a, b
            return (
                forestdist((Al[a[0]],a[1]-1), b) + strdist(An[a[0]].label, '')
            )
        elif a[0] >= a[1]: # δ(θ, l(j1)..j) = δ(θ, l(j1)..j-1) + γ(λ → w)
            #print 'delete', a, b
            fd = (
                forestdist(a, (Bl[b[0]],b[1]-1)) + strdist('', Bn[b[0]].label)
            )
        else:
            #print 'complex', a,b
            #import pdb
            #pdb.set_trace()
            if A.lmds[a[0]] == A.lmds[a[1]] and B.lmds[b[0]] == B.lmds[b[1]]:
                #                   +-
                #                   | δ(l(i1)..i-1, l(j1)..j) + γ(v → λ)
                # δ(F1 , F2 ) = min-+ δ(l(i1)..i , l(j1)..j-1) + γ(λ → w)
                #                   | δ(l(i1)..i-1, l(j1)..j-1) + γ(v → w)
                #                   +-
                fd = min(
                    (
                        forestdist((Al[a[0]],a[1]-1), b)
                        + strdist(An[a[0]].label, '')
                    ),
                    (
                        forestdist(a, (Bl[b[0]],b[1]-1))
                        + strdist('', Bn[b[0]].label)
                    ),
                    (
                        forestdist((Al[a[0]],a[1]-1), (Bl[b[0]],b[1]-1))
                        +strdist(An[a[0]].label, Bn[b[0]].label)
                    )
                )
            else:
                #                   +-
                #                   | δ(l(i1)..i-1, l(j1)..j) + γ(v → λ)
                # δ(F1 , F2 ) = min-+ δ(l(i1)..i , l(j1)..j-1) + γ(λ → w)
                #                   | δ(l(i1)..l(i)-1, l(j1)..l(j)-1) + treedist(i,j)
                #                   +-
                fd = min(
                    (
                        forestdist((Al[a[0]],a[1]-1), b)
                        + strdist(An[a[0]].label, '')
                    ),
                    (
                        forestdist(a, (Bl[b[0]],b[1]-1))
                        + strdist('', Bn[b[0]].label)
                    ),
                    (
                        forestdist((Al[a[0]],Al[a[1]]-1), (Bl[b[0]],Bl[b[1]]-1))
                        + treedist(a[1], b[1])
                    )
                )
        forestdists[key] = fd
        return fd
    def treedist(i, j):
        if i in treedists and j in treedists[i]: return treedists[i][j]
        def s(i, j, v):
            if i not in treedists: treedists[i] = dict()
            treedists[i][j] = v

        ## Note because my algorithm is memoized rather than dynamic in structure
        ## i do not have to explicitly store my results or precompute them
        ## as they will be computed as necessary

        #forestdist((0,0),(0,0))
        #for x in xrange(A.lmds[i], i+1): ## the plus one is for the xrange impl
            #forestdist((A.lmds[i], x), (0,0))

        #for y in xrange(B.lmds[j], j+1):
            #forestdist((0,0),(B.lmds[j], y))

        for x in xrange(A.lmds[i], i+1): ## the plus one is for the xrange impl
            for y in xrange(B.lmds[j], j+1):
                #if A.lmds[i] == A.lmds[x] and B.lmds[j] == B.lmds[y]:
                v = forestdist((A.lmds[i], x), (B.lmds[j], y))
                s(x, y, v)
                    #print (A.lmds[i], x), (B.lmds[j], y), 'td', v
                #else:
                    #print (A.lmds[i], x), (B.lmds[j], y), 'td'


        return treedists[i][j]

    #for i, j in ((i, j) for i in A.keyroots for j in B.keyroots):
        #print i, j, treedist(i, j)
        #x = treedist(i,j)
        #print '----->', (i,j), x
        #forestdists = dict()
    i = len(A.nodes)-1
    j = len(B.nodes)-1
    x = treedist(i,j)
    #print '----->', (i,j), x
    #for i in sorted(treedists.keys()):
        #for j in sorted(treedists.keys()):
            #print treedists[i][j],
        #print
    return x




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
    #print distance(A, B)
