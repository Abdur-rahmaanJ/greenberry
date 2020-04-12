# -*- coding: utf-8 -*-
from collections import OrderedDict
import inspect
from symbols import *
from debug_cp import *
from gb_utils.greenberry_search import GreenBerrySearch

L_USER = "dear berry"

# another lex would be to identify blobks first this is a side effect
MATH_OPS = ["+", "-", "*", "/"]
BOOLS = [S.TRUE, S.FALSE]
BOOL_OPS = [S.GREATER, S.LESS]
EOS = [S.NL, S.EOF]


class GreenBerryVarType:
    def __init__(self):
        print(self, "does not have an initialiser")

    def var_data(equal_i, words, delimeters):  # var x = 1
        """recognises data type"""
        value = 0
        type = None
        if words[equal_i + 1] == S.STRING:
            value = GreenBerrySearch.search(equal_i + 1, 0, words, delimeters)
            type = "string"
        elif words[equal_i + 1] == S.VAR_REF:
            value = M.g_vars[words[equal_i + 2]][0]
            type = "var_ref"
        elif words[equal_i + 1].isdigit():
            value = words[equal_i + 1]
            type = "number"
        elif words[equal_i + 1] == S.SQL:
            value = GreenBerrySearch.search(equal_i, 1, words, [S.SQR])
            type = "array"
        elif words[equal_i + 1] == S.BOOL:
            if words[equal_i + 2] == S.TRUE or words[equal_i + 2] == "1":
                value = words[equal_i + 2]
                type = "bool_1"
            if words[equal_i + 2] == S.FALSE or words[equal_i + 2] == "0":
                value = words[equal_i + 2]
                type = "bool_0"

        else:
            value = words[equal_i + 1]
            type = "word"
        return [value, type]

    def var_type(string):  # var x = 1
        type = None
        words = lex(string, KWDs)
        if words[0] == S.STRING:
            type = "string"
        elif words[0] == S.VAR_REF:
            type = "var_ref"
        elif words[0].isdigit():
            type = "number"
        elif words[0] == S.SQL:
            type = "array"
        elif words[0] == S.BOOL:
            if words[1] == S.TRUE or words[1] == "1":
                type = "bool_1"
            if words[1] == S.FALSE or words[1] == "0":
                type = "bool_0"
        else:
            type = "word"
        return type

    def var_ref_handling(at_i, words, g_vars):  # @y[1]
        """recognises references to variables"""
        name = words[at_i + 1]  # class debug
        type = g_vars[name][1]
        value = g_vars[name][0]
        returned_val = 0
        if type == "array" and len(words) > 3:
            value = value.split(S.COMMA)
            returned_val = value[int(words[at_i + 3])].strip()
        else:
            returned_val = value

        return returned_val
