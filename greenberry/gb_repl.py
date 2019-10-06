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
isSessionOn = 1
while isSessionOn == 1:
    x = input('---> ')
    greenBerry_eval(x)
    if x == 'berry exit':
        isSessionOn = 0
    print()
print('''
      ---greenBerry(c)---
      .gb REPL exited. see you soon _ _
      ---greenBerry(c)---
      ''')
