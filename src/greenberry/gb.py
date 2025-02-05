"""
Created on Tue Dec 26 21:53:56 2017

Notes : see
see theory_notes_simple.py
"""

import inspect
from collections import OrderedDict

from greenberry.symbols import S,E
from greenberry.utils.lex import GreenBerryLex
from greenberry.utils.parse import GreenBerryParse
from greenberry.utils.print import GreenBerryPrint
from greenberry.utils.search import GreenBerrySearch
from greenberry.utils.store import Flag
from greenberry.utils.store import Memory
from greenberry.utils.var_type import GreenBerryVarType
from greenberry.utils.class_instance import class_instance 

L_USER = "dear berry"

def get_keywords():
    """ returns a list of keyword symbols(attributes) from S class which are not built in methods or attibutes  """
    a_list = [a for a in inspect.getmembers(S, lambda a: not inspect.isroutine(a)) if not (a[0].startswith("__") and a[0].endswith("__"))]
    b_list = [b[0] for b in a_list]
    keywords = [getattr(S,i) for i in b_list]

    return keywords

# another lex would be to identify blobks first this is a side effect
MATH_OPS = ["+", "-", "*", "/"]
BOOLS = [S.TRUE, S.FALSE]
BOOL_OPS = [S.GREATER, S.LESS]
EOS = [S.NL, S.EOF]
KEYWORDS = get_keywords()
"""
Function with nested functions with different core
greenberry functionalities

"""


def greenberry_eval(x):
    global L_USER
    ###
    # program starts here
    ###

    Memory.g_vars = {}
    Memory.g_fs = {}
    Memory.g_cls = {}
    Flag.bStart = 100
    Flag.bEnd = 0
    Flag.isDebugOn = 0  # this is a reset needed for.ide

    g_vars = Memory.g_vars
    g_fs = Memory.g_fs
    g_cls : dict[str, dict[str, dict]] = Memory.g_cls
    words = GreenBerryLex.lex(x, KEYWORDS, add_eof=1)
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
                if words[i-1]=="print":
                    pass
                else:
                    Flag.bStart = i

                    times_by = int(words[i + 1])
                    string = GreenBerrySearch.search(i, 3, words, [S.NL, S.EOF])
                    wds = GreenBerryLex.lex(string, KEYWORDS)
                    GreenBerryPrint.printd(wds)
                    for d in range(times_by):
                        GreenBerryParse.simple_parse(g_vars, wds, line)
                    # colon_i = search_symbol(i, 1, words, [S.COLON])[1]
                    Flag.bEnd = GreenBerrySearch.search_symbol(i, 1, words, [S.NL, S.EOF])[
                        1
                    ]
            except:
                print(E.FOR, line)
                return
        #
        # new keyword
        #
        elif elem == S.NEW:
            if words[i-1]=="print":
                pass
            var_val = GreenBerryVarType.var_data(i, words, [S.NL, S.EOF])
            class_name = var_val[0]
            if class_name not in g_cls.keys(): # Check if the class exists
                print(E.NEW, line)
                return
            else:
                g_vars[class_name] = class_instance(class_name, g_cls[class_name]["attributes"])
            
            
        #
        # if statement
        #
        elif elem == S.IF:  # to be rededefined
            try:
                if words[i-1]=="print":
                    pass
                else:
                    Flag.bStart = i
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
                    wds = GreenBerryLex.lex(to_do, KEYWORDS)
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
                    Flag.bEnd = GreenBerrySearch.search_symbol(i, 1, words, [S.NL, S.EOF])[
                        1
                    ]
            except:
                print(E.IF, line)
                return

            # resolve flag
        #
        # function definition
        #
        elif elem == S.FUNCDEF:  # func vector : print aaa #func vector x : print @x
            params = []
            try:
                if words[i-1]=="print":
                    pass
                else:
                    Flag.bStart = i
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
                    Flag.bEnd = GreenBerrySearch.search_symbol(i, 1, words, [S.NL, S.EOF])[
                        1
                    ]
            except:
                print(E.FUNCDEF, line)
                return
        #
        # function call
        #
        elif elem == S.FUNCCALL:  # call vector
            try:
                if words[i-1]=="print":
                    pass
                else:
                    func_name = words[i + 1]
                    if g_fs[func_name]["params"] is None:
                        # print(g_fs)
                        # print(func_name)
                        wds = GreenBerryLex.lex(g_fs[func_name]["body"], KEYWORDS)
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
                        wds = GreenBerryLex.lex(g_fs[func_name]["body"], KEYWORDS)
                        GreenBerryParse.simple_parse(registry, wds, line)
            except:
                print(E.FUNCCALL, line)
                return

        #
        # class definition
        #
        elif elem == S.CLASS:  # class Man : power = 10 action walk : print a
            # attrs = {} future
            try:
                if words[i-1]=="print":
                    pass
                else:
                    Flag.bStart = i

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
                    Flag.bEnd = GreenBerrySearch.search_symbol(i, 1, words, [S.NL, S.EOF])[
                        1
                    ]
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
                return

        #
        # call class method.
        #
        elif elem == S.MAKE:  # make Man walk
            try:
                if words[i-1]=="print":
                    pass
                else:
                    class_name = words[i + 1]
                    if class_name not in g_cls:
                        print("wrong class name berry")
                        return
                    action_name = words[i + 2]
                    raw_text = g_cls[class_name]["actions"][action_name]
                    wds = GreenBerryLex.lex(raw_text, KEYWORDS)
                    GreenBerryParse.simple_parse(g_vars, wds, line)
            except:
                print(E.CLASSACT, line)
                return

        #
        # attribute viewing
        #
        elif elem == S.SEE:  # see power of Man
            try:
                if words[i-1]=="print":
                    pass
                else:
                    attr = words[i + 1]
                    class_name = words[i + 2]
                print(g_vars[class_name].instance_vars[attr])
            except:
                print(E.CLASSATT, line)
                return

        #
        # add attribute to class
        #
        elif elem == S.ADD:  # add to Man attribute name = string i am me
            try:
                if words[i-1]=="print":
                    pass
                else:
                    Flag.bStart = i
                    if words[i + 1] in g_cls:
                        if words[i + 2] == S.ATTRIB:
                            if words[i + 4] == S.EQUAL:
                                value = GreenBerryVarType.var_data(
                                    i + 4, words, [S.NL, S.EOF]
                                )
                                g_cls[words[i + 1]]["attributes"][words[i + 3]] = value
                            else:
                                print(S.EQUAL, line)
                        elif (
                            words[i + 2] == S.ACTION
                        ):  # add to Man action run : print running...
                            if words[i + 4] == S.COLON:
                                g_cls[words[i + 1]]["actions"][
                                    words[i + 3]
                                ] = GreenBerrySearch.search(i, 4, words, [S.NL, S.EOF])
                            else:
                                print(S.COLON, line)

                    else:
                        print(S.CLASSNAME, line)
                Flag.bEnd = GreenBerrySearch.search_symbol(i, 1, words, [S.NL, S.EOF])[
                    1
                ]
            except:
                print(E.ADD, line)
                return

        #
        # debug on or off
        #
        elif elem == S.SET:  # set debug on - set debug off
            try:
                if words[i-1]=="print":
                    pass
                else:
                    if words[i + 1] == "debug":
                        if words[i + 2] == "on":
                            Flag.isDebugOn = 1
                        elif words[i + 2] == "off":
                            Flag.isDebugOn = 0
            except:
                print(S.DEBUG, line)
                return
        else:
            if i < Flag.bStart or i > Flag.bEnd and elem != S.EOF:
                Flag.bStart = i
                Flag.bEnd = GreenBerrySearch.search_symbol(i, 1, words, [S.NL, S.EOF])[
                    1
                ]
                to_do = GreenBerrySearch.search(i - 1, 0, words, [S.NL, S.EOF])
                wds = GreenBerryLex.lex(to_do, KEYWORDS)
                GreenBerryParse.simple_parse(g_vars, wds, line)

    GreenBerryPrint.printd(g_vars)
    GreenBerryPrint.printd(g_fs)
    GreenBerryPrint.printd(g_cls)


# python greenberry_REPL.py
