import inspect
from collections import OrderedDict

from greenberry.debug_cp import *
from greenberry.symbols import E
from greenberry.symbols import *
from greenberry.utils.store import Flag
from greenberry.utils.store import Memory
from greenberry.utils.var_type import GreenBerrySearch
from greenberry.utils.var_type import GreenBerryVarType

L_USER = "dear berry"

MATH_OPS = ["+", "-", "*", "/"]
BOOLS = [S.TRUE, S.FALSE]
BOOL_OPS = [S.GREATER, S.LESS]
EOS = [S.NL, S.EOF]


class GreenBerryPrint:
    def __init(self):
        print(self, "does not have an initialiser")

    def printd(*args):
        """
        custom debugger print
        no return
        """
        if Flag.isDebugOn:
            for arg in args:
                print(" " * 5, "@debug->", arg)

    def print_handling(g_vars, i, words):
        """parses print command"""
        try:
            if i + 1 < len(words) and words[i + 1] not in [S.STRING, S.EVAL, S.VAR_REF]:
                print(words[i + 1])
            elif i + 1 < len(words) and words[i + 1] == S.VAR_REF:
                try:
                    print(GreenBerryVarType.var_ref_handling(i + 1, words, g_vars))
                except:
                    print(E.VARREF, line)
            elif i + 1 < len(words) and words[i + 1] == S.EVAL:
                expression = "".join([x for x in words[i + 2 :]])
                try:
                    print(eval(expression))
                except:
                    print(E.EVAL, line)
            elif i + 1 < len(words) and words[i + 1] == S.STRING:
                try:
                    print(GreenBerrySearch.search(i, 1, words, [S.NL, S.EOF]))
                except:
                    print(E.STRING, line)
        except:
            print(E.PRINT)

    def printLE():
        """Print lexer error"""
        LEX_ERROR = "lex error: no EOF should used in the middle of file"
        print(LEX_ERROR)
