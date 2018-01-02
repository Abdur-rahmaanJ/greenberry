# -*- coding: utf-8 -*-
"""
Created on Sun Dec 31 22:21:00 2017

@author: ARJ
"""
from greenBerry import greenBerry_eval

print('''
      ---greenBerry(c)---
      welcome to the .gb REPL
      ---greenBerry(c)---
      ''')
while 1:
    x = input('---> ')
    greenBerry_eval(x)
    print()
