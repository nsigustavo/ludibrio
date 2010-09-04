#!/usr/bin/env python
#-*- coding:utf-8 -*-

from sys import _getframe
import os


def frame_out_of_context():
    this_frame = frame = _getframe(1)
    while folder() in frame.f_code.co_filename:
        frame = frame.f_back
    return frame

def folder():
    return os.path.dirname(__file__)

def format_called(attr, args, kargs):
    if attr == "__getattribute__": return args[0]
    parameters = ', '.join(
                     [repr(arg) for arg in args]
                    +['%s=%r'%(k, v) for k, v in kargs.items()])
    return "%s(%s)"%( attr, parameters)



def _reindent(text, space_with=4):
	lines = text.split("\n")
	lines_indented = [" "*space_with+line for line in lines]
	return '\n'.join(lines_indented)