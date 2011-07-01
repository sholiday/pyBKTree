#!/usr/bin/env python
# encoding: utf-8
"""
BKTree.py

By Stephen Holiday 2011
http://stephenholiday.com

The code is under the [Apache 2.0](http://www.apache.org/licenses/LICENSE-2.0) license.

This a python implementation of a BKTree (Burkhard-Keller).
Essentially it allows searching for an object in a metric space.

One common use is for fuzzy string matching, like in a spell checker.
The search is performed by looking at the distance of the test with the current
node and moving according to the distance of the test to the children.

This technique is faster than brute force as it does not need to look at every
possible node in the space.

Implemented according to this post:
http://blog.notdot.net/2007/4/Damn-Cool-Algorithms-Part-1-BK-Trees

This is meant as a way for me to ensure I understand the algorithm.
I could have written it more 'pythonic' but this is meant to be a
prototype to a C++ version.

This is NOT an optimized version of the algorithm.
But I would be happy to accept suggestions/pull requests.

REQUIREMENTS:
 - python-Levenshtein http://pypi.python.org/pypi/python-Levenshtein/

Example usage:

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
"""

from Levenshtein import distance
class BKTree(object):
    def __init__(self):
        self.root=None
        pass
        
    def insert(self,obj):
        '''Takes an IMetricDistance object'''
        if self.root==None:
            self.root=BKNode(obj)
        else:
            self.root.insert(obj)

    def find(self,obj,threshold):
        if self.root is not None:
            for res in self.root.find(obj,threshold):
                yield res
        
    
    def __str__(self):
        return 'BKTree<root:%s>'%(self.root)
    
class BKNode(object):
    obj=None
    children=dict()
    
    def __init__(self,obj):
        self.obj=obj
        self.children=dict()
        
    def insert(self,obj):
        if obj==self.obj:
            return False
        else:
            d=obj.distance(self.obj)
            #print 's:%s is %d away from o:%s'%(self.obj,d,obj)
            #print self.children
            if self.children.has_key(d):
                #print 'going to %s'%self.children[d]
                self.children[d].insert(obj)
            else:
                self.children[d]=BKNode(obj)
            return True
            
    def find(self,obj,threshold):
        d=obj.distance(self.obj)
        #print 's:%s is %d from %s'%(self.obj,d,obj)
        if d <= threshold:
            yield self.obj
        dmin=d-threshold
        dmax=d+threshold
        for i in range(dmin,dmax+1):
            if self.children.has_key(i):
                for child in self.children[i].find(obj,threshold):
                    yield child
    def __str__(self):
        children_str=''
        for k in self.children:
            children_str='%s[%s,%s]'%(children_str,k,self.children[k].__str__())
        if children_str=='':
            children_str='[]'
        return 'BKNode<obj:%s, children:%s>'%(self.obj,children_str)
        
class StringObject(object):
    def __init__(self,value):
        self.value=value
    def distance(self,obj):
        return distance(self.value,obj.value)
    def get(self):
        return this.value
    def __str__(self):
        return 'IMetricDistance<value:%s>'%(self.value)
        
if __name__ == "__main__":
    bktree=BKTree()
    bktree.insert(StringObject('hey'))
    print bktree