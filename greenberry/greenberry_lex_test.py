from gb_utils.greenberry_lex import GreenBerryLex
from gb_utils.greenberry_print import GreenBerryPrint
from symbols import *
from debug_cp import *
import inspect
from collections import OrderedDict
MATH_OPS = ["+", "-", "*", "/"]
BOOLS = [S.TRUE, S.FALSE]
BOOL_OPS = [S.GREATER, S.LESS]
EOS = [S.NL, S.EOF]
def greenberry_lex_test(x, expected):
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
    words = GreenBerryLex.lex(x, KWDs, add_eof=1)
    print("\033[1mWords:\033[0m")
    is_correct = True
    j = 0
    for i in words:
        print(i)
        if not i == expected[j]:
            print("\x1b[31m This token is unexpected.\x1b[39m")
            is_correct = False
        j += 1
    return is_correct
def greenberry_lex_tester(to_lex, *args):
    l_args = list(args)
    l_args.append("{***end-of-file***}")
    result = greenberry_lex_test(to_lex, l_args)
    if result:
        print("\x1b[32m Test passed \x1b[39m")
    else:
        print("\x1b[31m Test failed \x1b[39m")
    return result
def greenberry_multi_tests(*args):
    result = True
    for i in args:
        cur = greenberry_lex_tester(i["test"], *i["expected"])
        if not cur:
            result = False
    if result:
        print("\x1b[32m All tests passed. \x1b[39m")
    else:
        print("\x1b[31m A test failed. \x1b[39m")
greenberry_multi_tests({
    "test": "print \"hi\"",
    "expected": ["print", "\"hi\""]
},
{
    "test": "print string hi",
    "expected": ["print", "string", "hi"]
},
{
    "test": "5 * 3 + (3 / 1)",
    "expected": ["5", "*", "3", "+", "(", "3", "/", "1", ")"]
},
{
    "test": "for 3 times: print greenBerry",
    "expected": ["for", "3", "times", ":", "print", "greenBerry"]
})