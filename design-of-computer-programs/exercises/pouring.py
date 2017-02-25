# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals


def pouring(xx, yy, goal, start=(0, 0)):
    if goal in start:
        return [start]


def test():
    assert pouring(xx=1, yy=1, goal=0)


test()
print 'pass'
