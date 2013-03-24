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

In addition the current version uses Numpy (although that dependency could
easily be removed)

Installation:

    cd to/the/base/dir/of/repo
    cat reqs.txt | xargs pip install
    python setup.py install

Tree Format and Usage
---------------------

The tree is represented by objects referencing each other. Each node is
represented by an object with at least the attributes `label` and `children`,
where `label` is a string and `children` is a list of other objects.

To find the distance between two object trees, call `compare.distance(root1,
root2)`.

The object format is used by the tests and is probably the easiest to work with.

#### A simple example:

    # Node(label, children)
    # a---> b
    #  \--> c
    c = Node('c', [])
    b = Node('b', [])
    a = Node('a', [b, c])
    assert compare.distance(a, a) == 0

#### Another Example:
    from zss import compare
    from zss.test_tree import Node

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
    assert compare.distance(A, B) == 2


See `test_metricspace.py` for more examples.

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

