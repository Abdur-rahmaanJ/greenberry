# -*- coding: utf-8 -*-

"""
Class for breaking strings into symbols
and return a list of each symbol.
"""
import inspect
from symbols import *

L_USER = 'dear berry'

# another lex would be to identify blobks first this is a side effect
MATH_OPS = ['+', '-', '*', '/']
BOOLS = [S.TRUE, S.FALSE]
BOOL_OPS = [S.GREATER, S.LESS]
EOS = [S.NL, S.EOF]

class GreenBerryLex():
    def __init__(self):
        print(self, 'does not have an initialiser')

    def lex(x, KWDs, add_eof=''):
        '''
        breaks string into symbols and ids
        returns list

        x - source string
        KWDs - keywords/symbols
        '''
        words = []
        cup = ''
        for i, elem in enumerate(x):
            if elem != ' ':
                cup += elem
            if i+1 >= len(x) or x[i+1] == ' ' or x[i+1] in KWDs or elem in KWDs:
                if cup != '':
                    words.append(cup)
                    cup = ''

        if add_eof == 1:
            words.append(S.EOF)

        return words
