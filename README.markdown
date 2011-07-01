## pyBKTree ##

By [Stephen Holiday](http://stephenholiday.com)

This a python implementation of a BKTree (Burkhard-Keller).
Essentially it allows searching for an object in a metric space.

One common use is for fuzzy string matching, like in a spell checker.
The search is performed by looking at the distance of the test with the current
node and moving according to the distance of the test to the children.

This technique is faster than brute force as it does not need to look at every
possible node in the space.

Implemented according to [this post](http://blog.notdot.net/2007/4/Damn-Cool-Algorithms-Part-1-BK-Trees)

This is meant as a way for me to ensure I understand the algorithm.
I could have written it more 'pythonic' but this is meant to be a
prototype to a C++ version.

This is *NOT* optimized. It's designed to be simple. 
But I would be happy to accept suggestions/pull requests.

The code is under the [Apache 2.0](http://www.apache.org/licenses/LICENSE-2.0) license.

## Requirements ##
 - [python-Levenshtein](http://pypi.python.org/pypi/python-Levenshtein/)

## Example usage ##

    >>> from BKTree import BKTree, StringObject
    >>> tree=BKTree()
    >>> tree.insert(StringObject('hat'))
    >>> print tree
    BKTree<root:BKNode<obj:IMetricDistance<value:hat>, children:[]>>
    >>> tree.insert(StringObject('hats'))
    >>> print tree
    BKTree<root:BKNode<obj:IMetricDistance<value:hat>, children:[1,BKNode<obj:IMetricDistance<value:hats>, children:[]>]>>
    >>> tree.insert(StringObject('hates'))
    >>> tree.insert(StringObject('hater'))
    >>> print tree
    BKTree<root:BKNode<obj:IMetricDistance<value:hat>, children:[1,BKNode<obj:IMetricDistance<value:hats>, children:[]>][2,BKNode<obj:IMetricDistance<value:hates>, children:[1,BKNode<obj:IMetricDistance<value:hater>, children:[]>]>]>>
    >>> tree.insert(StringObject('mat'))
    >>> tree.insert(StringObject('matte'))
    >>> tree.find(StringObject('mats'),1)
    <generator object find at 0x100603550>
    >>> for obj in tree.find(StringObject('mats'),1):
    ...     print obj
    ... 
    IMetricDistance<value:hats>
    IMetricDistance<value:mat>
    >>> for obj in tree.find(StringObject('hate'),1):
    ...     print obj
    ... 
    IMetricDistance<value:hat>
    IMetricDistance<value:hats>
    IMetricDistance<value:hates>
    IMetricDistance<value:hater>
    >>> for obj in tree.find(StringObject('haters'),1):
    ...     print obj
    ... 
    IMetricDistance<value:hates>
    IMetricDistance<value:hater>
    >>> for obj in tree.find(StringObject('haters'),0):
    ...     print obj
    ... 
    >>>