# -*- coding: utf-8 -*-
from collections import OrderedDict
import inspect
from symbols import *
from debug_cp import *
from greenberry_var_type import GreenBerryVarType
from greenberry_var_type import GreenBerrySearch

L_USER = 'dear berry'

MATH_OPS = ['+', '-', '*', '/']
BOOLS = [S.TRUE, S.FALSE]
BOOL_OPS = [S.GREATER, S.LESS]
EOS = [S.NL, S.EOF]

class GreenBerryPrint:
    def __init(self):
        print(self, 'does not have an initialiser')


    def printd(*args):
        '''
        custom debugger print
        no return
        '''
        if F.isDebugOn:
            for arg in args:
                print(' '*5, '@debug->', arg)

    def print_handling(g_vars, i, words):
            '''parses print command'''
            try:
                if i+1 < len(words) and words[i+1] not in [S.STRING, S.EVAL, S.VAR_REF]:
                    print(words[i+1])
                elif i+1 < len(words) and words[i+1] == S.VAR_REF:
                    try:
                        print(GreenBerryVarType.var_ref_handling(i+1, words, g_vars))
                    except:
                        print(E.VARREF, line)
                elif i+1 < len(words) and words[i+1] == S.EVAL:
                    try:
                        print(eval(words[i+2]))
                    except:
                        print(E.EVAL, line)
                elif i+1 < len(words) and words[i+1] == S.STRING:
                    try:
                        print(GreenBerrySearch.search(i, 1, words, [S.NL, S.EOF]))
                    except:
                        print(E.STRING, line)
            except:
                print(E.PRINT)

