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
   # M.g_vars = {}
    #M.g_fs = {}
    #M.g_cls = {}
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
    is_correct = True
    words = GreenBerryLex.lex(x, KWDs, add_eof=1)
    print("\033[1mWords:\033[0m")
    j = 0
    for i in words:
        print(i)
        if not i == expected[j]:
            print("This token is unexpected.")
            is_correct = False
        j += 1
    return is_correct
greenberry_lex_test("print \"Hi\"", ["print", "\"Hi\"", "{***end-of-file***}"])
greenberry_lex_test("print \"Hi\"", ["print", "\"Hi\"", "{***end-of-file***}"])
greenberry_lex_test("print \"Hi\"", ["print", "\"Hi\"", "{***end-of-file***}"])
greenberry_lex_test("print \"Hi\"", ["print", "\"Hi\"", "{***end-of-file***}"])