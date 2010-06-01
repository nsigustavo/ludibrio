#!/usr/bin/env python
#-*- coding:utf-8 -*-


class matcher(object):
    """Base for special arguments for matching parameters."""

    def __init__(self, matcher, expected=None):
        self.expected = expected
        self.matcher = matcher

    def __call__(self, expected=None):
        return type(self)(self.matcher, expected)

    def __eq__(self, other):
        return self.matcher(other, self.expected)

from matcher import *



