#!/usr/bin/env python
# coding: utf-8
from __future__ import print_function

__source__ = "FrameStack.py"
__author__ = "Frank J. Greco"
__copyright__ = "Copyright 2015-2018, Frank J, Greco"
__credits__ = []
__license__ = "Apache"
__version__ = "1.0.1"
__email__ = ""
__status__ = "Development"

class FrameStack:
    def __init__(self,stack_size=10):
        self.items = stack_size*['']
        self.stack_size = stack_size
        self.save = ''

    def isEmpty(self):
        return self.items == []

    def size(self):
        return len(self.items)

    def push(self, item):
        self.items.append(item)

    def limit_push(self,item):
        self.items.append(item)
        if len(self.items) > self.stack_size:
            self.save=self.items[0]
            del self.items[0]

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items) - 1]

    def long_peek(self,slen):
        group = ''
        ll = len(self.items)
        for i in range(ll-1,ll-slen-1,-1):
            group= self.items[i]+' '+group
            group = group.replace("'", "")
        return group

    def reset(self):
        self.items=self.stack_size *['']

    def undo_limit_push(self):
        self.items.pop()
        self.items.insert(0,self.save)

