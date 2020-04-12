# -*- coding: utf-8 -*-
"""
Created on Tue Dec 26 21:53:56 2017

Notes : see
see theory_notes_simple.py
"""

from collections import OrderedDict
import inspect
from symbols import *
from debug_cp import *
from gb_utils.greenberry_print import GreenBerryPrint
from gb_utils.greenberry_lex import GreenBerryLex
from gb_utils.greenberry_parse import GreenBerryParse
from gb_utils.greenberry_plot import GreenBerryPlot
from gb_utils.greenberry_search import GreenBerrySearch
from gb_utils.greenberry_var_type import GreenBerryVarType

L_USER = "dear berry"


# another lex would be to identify blobks first this is a side effect
MATH_OPS = ["+", "-", "*", "/"]
BOOLS = [S.TRUE, S.FALSE]
BOOL_OPS = [S.GREATER, S.LESS]
EOS = [S.NL, S.EOF]

"""
Function with nested functions with different core
greenberry functionalities

"""


def greenBerry_eval(x):
    global L_USER
    ###
    # program starts here
    ###

    M.g_vars = {}
    M.g_fs = {}
    M.g_cls = {}
    F.bStart = 100
    F.bEnd = 0
    F.isDebugOn = 0  # this is a reset needed for gb_ide

    KWDs = [
        getattr(S, i)
        for i in [
            b[0]
            for b in [
                a
                for a in inspect.getmembers(S, lambda a: not inspect.isroutine(a))
                if not (a[0].startswith("__") and a[0].endswith("__"))
            ]
        ]
    ]

    g_vars = M.g_vars
    g_fs = M.g_fs
    g_cls = M.g_cls
    words = GreenBerryLex.lex(x, KWDs, add_eof=1)
    GreenBerryPrint.printd(words)
    line = 1

    """
    if elem.value == S.NL
    error : elem.line
    """
    for i, elem in enumerate(words):  # mainloop for complex parsing
        # printd(elem)

        #
        # newline
        #
        if elem == S.NL:
            line += 1

        #
        # minified for loop
        #
        elif elem == S.FOR:
            try:
                F.bStart = i

                times_by = int(words[i + 1])
                string = GreenBerrySearch.search(i, 3, words, [S.NL, S.EOF])
                wds = GreenBerryLex.lex(string, KWDs)
                GreenBerryPrint.printd(wds)
                for d in range(times_by):
                    GreenBerryParse.simple_parse(g_vars, wds, line)
                # colon_i = search_symbol(i, 1, words, [S.COLON])[1]
                F.bEnd = GreenBerrySearch.search_symbol(i, 1, words, [S.NL, S.EOF])[1]
            except:
                print(E.FOR, line)

        #
        # if statement
        #
        elif elem == S.IF:  # to be rededefined
            try:
                F.bStart = i
                L, R = 0, 0
                raw = GreenBerrySearch.search_symbol(
                    i,
                    1,
                    words,
                    [S.EQUAL, S.LESS, S.GREATER, S.EQUAL_GREATER, S.EQUAL_LESS],
                )
                symbol = raw[0]
                symbol_i = raw[1]
                colon_i = GreenBerrySearch.search_symbol(i, 1, words, S.COLON)[1]
                to_do = GreenBerrySearch.search(colon_i, 0, words, [S.NL, S.EOF])
                wds = GreenBerryLex.lex(to_do, KWDs)
                if words[i + 1] == S.VAR_REF:
                    # print('L @ detected')
                    L = g_vars[words[i + 2]][0]
                elif words[i + 1].isdigit():
                    # print('L int detected')
                    L = int(words[i + 1])
                else:
                    # print('L str detected')
                    L = GreenBerrySearch.search(i, 0, words, [symbol, S.COLON])

                if words[symbol_i + 1] == S.VAR_REF:
                    # print('R @ detected')
                    R = g_vars[words[symbol_i + 2]][0]
                elif words[symbol_i + 1].isdigit():
                    # print("R", words[symbol_i+1])
                    R = int(words[symbol_i + 1])
                else:
                    # print('R str detected')
                    R = GreenBerrySearch.search(symbol_i, 0, words, [S.COLON])
                # print(L, R, symbol)
                if symbol == S.EQUAL:
                    if L == R:
                        GreenBerryParse.simple_parse(g_vars, wds, line)
                elif symbol == S.GREATER:
                    if L > R:
                        GreenBerryParse.simple_parse(g_vars, wds, line)
                elif symbol == S.LESS:
                    if L < R:
                        GreenBerryParse.simple_parse(g_vars, wds, line)
                elif symbol == S.EQUAL_GREATER:
                    if L >= R:
                        GreenBerryParse.simple_parse(g_vars, wds, line)
                elif symbol == S.EQUAL_LESS:
                    if L <= R:
                        GreenBerryParse.simple_parse(g_vars, wds, line)
                # colon_i = search_symbol(i, 1, words, [S.COLON])[1]
                F.bEnd = GreenBerrySearch.search_symbol(i, 1, words, [S.NL, S.EOF])[1]
            except:
                print(E.IF, line)

            # resolve flag
        #
        # function definition
        #
        elif elem == S.FUNCDEF:  # func vector : print aaa #func vector x : print @x
            params = []
            try:

                F.bStart = i
                func_name = words[i + 1]
                if words[i + 2] == S.COLON:
                    body = GreenBerrySearch.search(i, 2, words, [S.NL, S.EOF])
                    g_fs[func_name] = {"params": None, "body": body}
                else:
                    params = GreenBerrySearch.search_toks(i, 1, words, [S.COLON])
                    col_i = GreenBerrySearch.search_symbol(i, 1, words, [S.COLON])[1]
                    body = GreenBerrySearch.search(col_i, 0, words, [S.NL, S.EOF])
                    registry = OrderedDict()
                    for param in params:
                        registry[param] = None
                    g_fs[func_name] = {"params": registry, "body": body}

                # colon_i = search_symbol(i, 1, words, [S.COLON])[1]
                F.bEnd = GreenBerrySearch.search_symbol(i, 1, words, [S.NL, S.EOF])[1]
            except:
                print(E.FUNCDEF, line)
        #
        # function call
        #
        elif elem == S.FUNCCALL:  # call vector
            try:
                func_name = words[i + 1]
                if g_fs[func_name]["params"] is None:
                    # print(g_fs)
                    # print(func_name)
                    wds = GreenBerryLex.lex(g_fs[func_name]["body"], KWDs)
                    GreenBerryParse.simple_parse(g_vars, wds, line)
                else:
                    param_vals = GreenBerrySearch.search_toks(
                        i, 1, words, [S.NL, S.EOF]
                    )
                    registry = g_fs[func_name]["params"]
                    i = 0
                    for key in registry:
                        registry[key] = [
                            param_vals[i],
                            GreenBerryVarType.var_type(param_vals[i]),
                        ]  # data
                        i += 1
                    wds = lex(g_fs[func_name]["body"], KWDs)
                    GreenBerryParse.simple_parse(registry, wds, line)
            except:
                print(E.FUNCCALL, line)

        #
        # class definition
        #
        elif elem == S.CLASS:  # class Man : power = 10 action walk : print a
            # attrs = {} future
            try:
                F.bStart = i

                class_name = words[
                    i + 1
                ]  # subsequent changed to action for mult attribs
                attr_name = words[
                    i + 3
                ]  # search_symbol var_data(i+4, words, [S.NL, S.EOF])
                attr_val = GreenBerryVarType.var_data(i + 4, words, [S.ACTION])
                action_name = words[i + 7]
                action_body = GreenBerrySearch.search(i + 7, 1, words, [S.NL, S.EOF])
                g_cls[class_name] = {
                    "attributes": {attr_name: attr_val},
                    "actions": {action_name: action_body},
                }

                # colon_i = search_symbol(i, 1, words, [S.COLON])[1]
                F.bEnd = GreenBerrySearch.search_symbol(i, 1, words, [S.NL, S.EOF])[1]
                """
                class_name = {
                name = name,
                attributes = {
                        x = 1,
                        y = 2
                        }
                methods = {
                        walk = string here,
                        raise hand = string here
                        }
                }
                """
            except:
                print(E.CLASSDEC, line)

        #
        # call class method.
        #
        elif elem == S.MAKE:  # make Man walk
            try:
                class_name = words[i + 1]
                if class_name not in g_cls:
                    print("wrong class name berry")
                action_name = words[i + 2]
                raw_text = g_cls[class_name]["actions"][action_name]
                wds = GreenBerryLex.lex(raw_text, KWDs)
                GreenBerryParse.simple_parse(g_vars, wds, line)
            except:
                print(E.CLASSACT, line)

        #
        # attribute viewing
        #
        elif elem == S.SEE:  # see power of Man
            try:
                attr = words[i + 1]
                class_name = words[i + 2]
                print(g_cls[class_name]["attributes"][attr][0])
            except:
                print(E.CLASSATT, line)

        #
        # add attribute to class
        #
        elif elem == S.ADD:  # add to Man attribute name = string i am me
            try:
                F.bStart = i
                if words[i + 1] in g_cls:
                    if words[i + 2] == S.ATTRIB:
                        if words[i + 4] == S.EQUAL:
                            value = GreenBerryVarType.var_data(
                                i + 4, words, [S.NL, S.EOF]
                            )
                            g_cls[words[i + 1]]["attributes"][words[i + 3]] = value
                        else:
                            print(E.EQUAL, line)
                    elif (
                        words[i + 2] == S.ACTION
                    ):  # add to Man action run : print running...
                        if words[i + 4] == S.COLON:
                            g_cls[words[i + 1]]["actions"][
                                words[i + 3]
                            ] = GreenBerrySearch.search(i, 4, words, [S.NL, S.EOF])
                        else:
                            print(E.COLON, line)

                else:
                    print(E.CLASSNAME, line)
                F.bEnd = GreenBerrySearch.search_symbol(i, 1, words, [S.NL, S.EOF])[1]
            except:
                print(E.ADD, line)

        #
        # debug on or off
        #
        elif elem == S.SET:  # set debug on - set debug off
            try:
                if words[i + 1] == "debug":
                    if words[i + 2] == "on":
                        F.isDebugOn = 1
                    elif words[i + 2] == "off":
                        F.isDebugOn = 0
            except:
                print(E.DEBUG, line)
        else:
            if i < F.bStart or i > F.bEnd and elem != S.EOF:
                F.bStart = i
                F.bEnd = GreenBerrySearch.search_symbol(i, 1, words, [S.NL, S.EOF])[1]
                to_do = GreenBerrySearch.search(i - 1, 0, words, [S.NL, S.EOF])
                wds = GreenBerryLex.lex(to_do, KWDs)
                GreenBerryParse.simple_parse(g_vars, wds, line)

    GreenBerryPrint.printd(g_vars)
    GreenBerryPrint.printd(g_fs)
    GreenBerryPrint.printd(g_cls)


# python greenBerry_REPL.py
