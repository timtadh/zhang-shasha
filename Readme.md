Sleepytree
==========

### Estimate tree distance using the Zhang-Shasha algorithm

"Zhang Shasha" -> "ZSS" -> "Zzz." Get it? Ha!

Based on [Simple fast algorithms for the editing distance between trees and related problems.](http://www.grantjenks.com/wiki/_media/ideas:simple_fast_algorithms_for_the_editing_distance_between_tree_and_related_problems.pdf)*

About
-----

The author needed to calculate tree edit distance. All the good explanations of algorithms were behind paywalls and the only public implementation that could be found was in a zip archive of a Java project with a broken makefile on the server of some university in Australia.

This is a [considerably] cleaned up Python translation of that Java project. [Here is the original.](http://web.science.mq.edu.au/~swan/howtos/treedistance/) Note that _the original is an incorrect implementation_ and the bugs have been fixed in this implementaiton.

Most of the comments are preserved from the original.

<sub>* Kaizhong Zhang and Dennis Shasha. Simple fast algorithms for the editing distance between trees and related problems. SIAM Journal of Computing, 18:1245–1262, 1989.
</sub>