#!/usr/bin/env python
#-*- coding:utf-8 -*-

from sys import _getframe
import os


def frameOutOfContext():
    this_frame = frame = _getframe(1)
    while folder() in frame.f_code.co_filename:
        frame = frame.f_back
    return frame

def folder():
    return os.path.dirname(__file__)
    


