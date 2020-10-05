#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Authors: Tim Henderson and Steve Johnson
#Email: tim.tadh@gmail.com, steve@steveasleep.com
#For licensing see the LICENSE file in the top level directory.

from __future__ import absolute_import
from six.moves import range

import collections

try:
    import numpy as np
    zeros = np.zeros
except ImportError:
    def py_zeros(dim, pytype):
        assert len(dim) == 2
        return [[pytype() for y in range(dim[1])]
                for x in range(dim[0])]
    zeros = py_zeros

try:
    from editdist import distance as strdist
except ImportError:
    try:
        from editdistance import eval as strdist
    except ImportError:
        def strdist(a, b):
            if a == b:
                return 0
            else:
                return 1

from zss.simple_tree import Node


class AnnotatedTree(object):

    def __init__(self, root, get_children):
        self.get_children = get_children

        self.root = root
        self.nodes = list()  # a post-order enumeration of the nodes in the tree
        self.ids = list()    # a matching list of ids
        self.lmds = list()   # left most descendents
        self.keyroots = None
            # k and k' are nodes specified in the post-order enumeration.
            # keyroots = {k | there exists no k'>k such that lmd(k) == lmd(k')}
            # see paper for more on keyroots

        stack = list()
        pstack = list()
        stack.append((root, collections.deque()))
        j = 0
        while len(stack) > 0:
            n, anc = stack.pop()
            nid = j
            for c in self.get_children(n):
                a = collections.deque(anc)
                a.appendleft(nid)
                stack.append((c, a))
            pstack.append(((n, nid), anc))
            j += 1
        lmds = dict()
        keyroots = dict()
        i = 0
        while len(pstack) > 0:
            (n, nid), anc = pstack.pop()
            self.nodes.append(n)
            self.ids.append(nid)
            if not self.get_children(n):
                lmd = i
                for a in anc:
                    if a not in lmds: lmds[a] = i
                    else: break
            else:
                try: lmd = lmds[nid]
                except:
                    import pdb
                    pdb.set_trace()
            self.lmds.append(lmd)
            keyroots[lmd] = i
            i += 1
        self.keyroots = sorted(keyroots.values())


class Operation(object):
    """
    Dummy class for storing edit operations
    """
    remove = 0
    insert = 1
    update = 2
    match = 3

    def __init__(self, op, arg1=None, arg2=None):
        self.type = op
        self.arg1 = arg1
        self.arg2 = arg2

    def __repr__(self):
        if hasattr(self.arg1, "label") and hasattr(self.arg2, "label"):
            if self.type == self.remove:
                return '<Operation Remove: ' + self.arg1.label + '>'
            elif self.type == self.insert:
                return '<Operation Insert: ' + self.arg2.label + '>'
            elif self.type == self.update:
                return '<Operation Update: ' + self.arg1.label + ' to ' + self.arg2.label + '>'
            else:
                return '<Operation Match: ' + self.arg1.label + ' to ' + self.arg2.label + '>'
        else:
            if self.type == self.remove:
                return '<Operation Remove>'
            elif self.type == self.insert:
                return '<Operation Insert>'
            elif self.type == self.update:
                return '<Operation Update>'
            else:
                return '<Operation Match>'

    def __eq__(self, other):
        if other is None: return False
        if not isinstance(other, Operation):
            raise TypeError("Must compare against type Operation")
        return self.type == other.type and self.arg1 == other.arg1 and \
            self.arg2 == other.arg2


REMOVE = Operation.remove
INSERT = Operation.insert
UPDATE = Operation.update
MATCH = Operation.match


def simple_distance(A, B, get_children=Node.get_children,
        get_label=Node.get_label, label_dist=strdist, return_operations=False):
    """Computes the exact tree edit distance between trees A and B.

    Use this function if both of these things are true:

    * The cost to insert a node is equivalent to ``label_dist('', new_label)``
    * The cost to remove a node is equivalent to ``label_dist(new_label, '')``

    Otherwise, use :py:func:`zss.distance` instead.

    :param A: The root of a tree.
    :param B: The root of a tree.

    :param get_children:
        A function ``get_children(node) == [node children]``.  Defaults to
        :py:func:`zss.Node.get_children`.

    :param get_label:
        A function ``get_label(node) == 'node label'``.All labels are assumed
        to be strings at this time. Defaults to :py:func:`zss.Node.get_label`.

    :param label_dist:
        A function
        ``label_distance((get_label(node1), get_label(node2)) >= 0``.
        This function should take the output of ``get_label(node)`` and return
        an integer greater or equal to 0 representing how many edits to
        transform the label of ``node1`` into the label of ``node2``. By
        default, this is string edit distance (if available). 0 indicates that
        the labels are the same. A number N represent it takes N changes to
        transform one label into the other.

    :param return_operations: if True, return a tuple (cost, operations)
        where operations is a list of the operations to transform A into B.

    :return: An integer distance [0, inf+)
    """
    return distance(
        A, B, get_children,
        insert_cost=lambda node: label_dist('', get_label(node)),
        remove_cost=lambda node: label_dist(get_label(node), ''),
        update_cost=lambda a, b: label_dist(get_label(a), get_label(b)),
        return_operations=return_operations
    )


def distance(A, B, get_children, insert_cost, remove_cost, update_cost,
             return_operations=False):
    '''Computes the exact tree edit distance between trees A and B with a
    richer API than :py:func:`zss.simple_distance`.

    Use this function if either of these things are true:

    * The cost to insert a node is **not** equivalent to the cost of changing
      an empty node to have the new node's label
    * The cost to remove a node is **not** equivalent to the cost of changing
      it to a node with an empty label

    Otherwise, use :py:func:`zss.simple_distance`.

    :param A: The root of a tree.
    :param B: The root of a tree.

    :param get_children:
        A function ``get_children(node) == [node children]``.  Defaults to
        :py:func:`zss.Node.get_children`.

    :param insert_cost:
        A function ``insert_cost(node) == cost to insert node >= 0``.

    :param remove_cost:
        A function ``remove_cost(node) == cost to remove node >= 0``.

    :param update_cost:
        A function ``update_cost(a, b) == cost to change a into b >= 0``.

    :param return_operations: if True, return a tuple (cost, operations)
        where operations is a list of the operations to transform A into B.

    :return: An integer distance [0, inf+)
    '''
    A, B = AnnotatedTree(A, get_children), AnnotatedTree(B, get_children)
    size_a = len(A.nodes)
    size_b = len(B.nodes)
    treedists = zeros((size_a, size_b), float)
    operations = [[[] for _ in range(size_b)] for _ in range(size_a)]

    def treedist(i, j):
        Al = A.lmds
        Bl = B.lmds
        An = A.nodes
        Bn = B.nodes

        m = i - Al[i] + 2
        n = j - Bl[j] + 2
        fd = zeros((m,n), float)
        partial_ops = [[[] for _ in range(n)] for _ in range(m)]

        ioff = Al[i] - 1
        joff = Bl[j] - 1

        for x in range(1, m): # δ(l(i1)..i, θ) = δ(l(1i)..1-1, θ) + γ(v → λ)
            node = An[x+ioff]
            fd[x][0] = fd[x-1][0] + remove_cost(node)
            op = Operation(REMOVE, node)
            partial_ops[x][0] = partial_ops[x-1][0] + [op]
        for y in range(1, n): # δ(θ, l(j1)..j) = δ(θ, l(j1)..j-1) + γ(λ → w)
            node = Bn[y+joff]
            fd[0][y] = fd[0][y-1] + insert_cost(node)
            op = Operation(INSERT, arg2=node)
            partial_ops[0][y] = partial_ops[0][y-1] + [op]

        for x in range(1, m):  # the plus one is for the xrange impl
            for y in range(1, n):
                # x+ioff in the fd table corresponds to the same node as x in
                # the treedists table (same for y and y+joff)
                node1 = An[x+ioff]
                node2 = Bn[y+joff]
                # only need to check if x is an ancestor of i
                # and y is an ancestor of j
                if Al[i] == Al[x+ioff] and Bl[j] == Bl[y+joff]:
                    #                   +-
                    #                   | δ(l(i1)..i-1, l(j1)..j) + γ(v → λ)
                    # δ(F1 , F2 ) = min-+ δ(l(i1)..i , l(j1)..j-1) + γ(λ → w)
                    #                   | δ(l(i1)..i-1, l(j1)..j-1) + γ(v → w)
                    #                   +-
                    costs = [fd[x-1][y] + remove_cost(node1),
                             fd[x][y-1] + insert_cost(node2),
                             fd[x-1][y-1] + update_cost(node1, node2)]
                    fd[x][y] = min(costs)
                    min_index = costs.index(fd[x][y])

                    if min_index == 0:
                        op = Operation(REMOVE, node1)
                        partial_ops[x][y] = partial_ops[x-1][y] + [op]
                    elif min_index == 1:
                        op = Operation(INSERT, arg2=node2)
                        partial_ops[x][y] = partial_ops[x][y - 1] + [op]
                    else:
                        op_type = MATCH if fd[x][y] == fd[x-1][y-1] else UPDATE
                        op = Operation(op_type, node1, node2)
                        partial_ops[x][y] = partial_ops[x - 1][y - 1] + [op]

                    operations[x + ioff][y + joff] = partial_ops[x][y]
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
                    costs = [fd[x-1][y] + remove_cost(node1),
                             fd[x][y-1] + insert_cost(node2),
                             fd[p][q] + treedists[x+ioff][y+joff]]
                    fd[x][y] = min(costs)
                    min_index = costs.index(fd[x][y])
                    if min_index == 0:
                        op = Operation(REMOVE, node1)
                        partial_ops[x][y] = partial_ops[x-1][y] + [op]
                    elif min_index == 1:
                        op = Operation(INSERT, arg2=node2)
                        partial_ops[x][y] = partial_ops[x][y-1] + [op]
                    else:
                        partial_ops[x][y] = partial_ops[p][q] + \
                            operations[x+ioff][y+joff]

    for i in A.keyroots:
        for j in B.keyroots:
            treedist(i, j)

    if return_operations:
        return treedists[-1][-1], operations[-1][-1]
    else:
        return treedists[-1][-1]
