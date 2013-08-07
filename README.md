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
