Zhang Shasha
============

### Compute Tree Edit Distance Using the Zhang-Shasha Algorithm

Tim Henderson ([tim.tadh@gmail.com](tim.tadh@gmail.com))
and Steve Johnson ([steve@steveasleep.com](steve@steveasleep.com))

If you like this module you may also like
[pygram](https://github.com/timtadh/PyGram) which computes an approximation to
tree edit distance. The difference? PyGram (which uses the PQ-Gram algorithm) is
in general much faster than the Zhang-Shasha algorithm but it doesn't given an
exact edit score like Zhang-Shasha does.

Installation
------------

Zhang Shasha requires at least Python 2.5. If the
[`editdist`](http://pypi.python.org/pypi/editdist/0.1) module is installed, it
will be used to determine replacement cost instead of a simple 1/0 equality
comparison.

The current version optionally uses Numpy.

Installation:

    python setup.py install

If you would like to try install `numpy`, `editdist`, and `nose` (for running
tests) then also run:

    pip install -r requirements.txt

If you want to build the docs, you'll need to `pip install sphinx`.


Tree Format and Usage
---------------------

By default the tree is represented by objects referencing each other. Each node
is represented by an object with at least the attributes `label` and `children`,
where `label` is a string and `children` is a list of other objects. However,
all of this is configurable by passing in functions. Here is how to use the
default api:

To find the distance between two object trees, call
`zss.distance(root1, root2)`.

The object format is used by the tests and is probably the easiest to work with.

#### A simple example:

```python
# Node(label, children)
# a---> b
#  \--> c
c = zss.Node('c', [])
b = zss.Node('b', [])
a = zss.Node('a', [b, c])
assert zss.distance(a, a) == 0
```

#### Another Example:

```python
from zss import distance, Node

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
            .addkid(Node("c")
                .addkid(Node("b"))))
        .addkid(Node("e"))
    )
assert distance(A, B) == 2
```


See `test_metricspace.py` for more examples.


Specifying Custom Tree Formats
------------------------------

Specifying custom tree formats and distance metrics is easy. The `zss.distance`
function takes 3 extra parameters besides the two tree to compare:

1. `get_children` - a function to retrieve a list of children from a node.
2. `get_label` - a function to retrieve the label object from a node.
3. `label_dist` - a function to compute the non-negative integer distance
   between two node labels.

### Example

```python
#!/usr/bin/env python

import zss

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

A = (
  WeirdNode("f")
    .addkid(WeirdNode("d")
      .addkid(WeirdNode("a"))
      .addkid(WeirdNode("c")
        .addkid(WeirdNode("b"))
      )
    )
    .addkid(WeirdNode("e"))
)
B = (
  WeirdNode("f")
    .addkid(WeirdNode("c")
      .addkid(WeirdNode("d")
        .addkid(WeirdNode("a"))
        .addkid(WeirdNode("b"))
      )
    )
    .addkid(WeirdNode("e"))
)

dist = zss.distance(
    A, B, WeirdNode.get_children, WeirdNode.get_label, weird_dist)

print dist
assert dist == 20
```

References
----------

This module began as a direct port of [this Java project from a dark alley of
the internet](http://web.science.mq.edu.au/~swan/howtos/treedistance/), which is
actually an **incorrect implementation.** Unfortunately, the author of the Java
project got it so wrong even our port was incorrect. Thus, the entire algorithm
was re-implemented from scratch based on the original paper by Zhang and Shasha.
If you would like to discuss the paper, or the the tree edit distance problem
(we have implemented a few other algorithms as well) please email the authors.

### Another Good Implementation

Another good implementation can be found on Dr. Nikolaus Augsten's site. It is
called [approxlib](http://www.inf.unibz.it/~augsten/src/) and it contains a
number of useful tree distance algorithms. Highly recommended.

### Papers

The original paper describing the algorithm:

[Kaizhong Zhang and Dennis Shasha. Simple fast algorithms for the editing distance between trees and related problems. SIAM Journal of Computing, 18:1245–1262, 1989.](http://www.grantjenks.com/wiki/_media/ideas:simple_fast_algorithms_for_the_editing_distance_between_tree_and_related_problems.pdf)

[Slide deck overview of Zhang-Shasha](http://www.inf.unibz.it/dis/teaching/ATA/ata7-handout-1x1.pdf)

[Another paper describing Zhang-Shasha](http://research.cs.queensu.ca/TechReports/Reports/1995-372.pdf)

