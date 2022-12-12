"""
Class for breaking strings into symbols
and return a list of each symbol.
"""
import inspect

from greenberry.symbols import *
from greenberry.utils.print import GreenBerryPrint

L_USER = "dear berry"

# another lex would be to identify blobks first this is a side effect
MATH_OPS = ["+", "-", "*", "/"]
BOOLS = [S.TRUE, S.FALSE]
BOOL_OPS = [S.GREATER, S.LESS]
EOS = [S.NL, S.EOF]


class GreenBerryLex:
    def __init__(self):
        print(self, "does not have an initialiser")

    def lex(x, KWDs, add_eof=""):
        """
        breaks string into symbols and ids
        returns list

        x - source string
        KWDs - keywords/symbols
        """
        words = []
        cup = ""
        LEX_FLAG = 0  # if lexer occur an error

        for i, elem in enumerate(x):
            if elem != " ":
                cup += elem
            if i + 1 >= len(x) or x[i + 1] == " " or x[i + 1] in KWDs or elem in KWDs:
                if cup != "":
                    words.append(cup)
                    cup = ""

        if add_eof == 1:
            words.append(S.EOF)

        # idea is to scan over the list of words to make sure that the EOF symbol is not in the middle
        pos = -1
        for i in range(0, len(words)):
            if words[i] is S.EOF:
                pos = i
                break
        if pos != -1 and pos is not len(words) - 1:
            LEX_FLAG = 1
            GreenBerryPrint.printLE()

        if LEX_FLAG == 1:
            return ["Lex-Error"]

        return words
