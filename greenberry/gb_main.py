# -*- coding: utf-8 -*-
"""
Created on Sun Dec 31 22:54:37 2017

@author: ARJ
"""

from greenBerry import greenBerry_eval

x = ''

with open('main.gb', 'r') as f:
    x = f.read()

greenBerry_eval(x)
