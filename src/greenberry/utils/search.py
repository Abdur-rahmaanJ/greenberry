import inspect
from collections import OrderedDict

from greenberry.debug_cp import *
from greenberry.symbols import *

L_USER = "dear berry"

# another lex would be to identify blobks first this is a side effect
MATH_OPS = ["+", "-", "*", "/"]
BOOLS = [S.TRUE, S.FALSE]
BOOL_OPS = [S.GREATER, S.LESS]
EOS = [S.NL, S.EOF]


class GreenBerrySearch:
    def __init(self):
        print(self, "does not have an initialiser")

    def search(i, offset, words, delimeters):
        """
        searches for symbols and returns string in between specified index
        and symbol

        i - current index
        offset - offset from index
        words - current list of symbol/keyword being searched in
        delimiters - list of delimiting symbols

        return string
        """
        base = i + offset
        j = 1
        string = ""
        while base + j < len(words):
            if words[base + j] in delimeters:
                break
            string += words[base + j] + " "
            j += 1
        return string

    def search_toks(i, offset, words, delimeters):
        """
        searches for symbols and returns all found sybols in between
        specified index and symbol as list

        i - current index
        offset - offset from index
        words - current list of symbol/keyword being searched in
        delimiters - list of delimiting symbols

        return list
        """
        base = i + offset
        j = 1
        list = []
        while base + j < len(words):
            if words[base + j] in delimeters:
                break
            list.append(words[base + j])
            j += 1
        return list

    def search_symbol(i, offset, words, delimeters):  # i to be resolved
        """
        finds the index as well as the delimiting symbol (in case there are
        many) we are searching for

        i - current index
        offset - offset from index
        words - current list of symbol/keyword being searched in
        delimiters - list of delimiting symbols
        word - symbol or set of symbols currently being checked
        new_base - index to be returned after the search

        return list

        list[0] - symbol
        list[1] - index
        """
        base = i + offset
        j = 1
        word = ""
        new_base = 0
        while base + j < len(words):
            word = "".join(words[base + j : base + j + 2])
            new_base = base + j + 1
            if word in delimeters:
                break
            word = words[base + j]
            new_base = base + j
            if word in delimeters:
                break
            j += 1
        return [word, new_base]
