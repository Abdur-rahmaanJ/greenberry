from greenberry.symbols import *


class GreenBerryReferences:
    def __init__(self):
        print(self, "does not have an initialiser")
        
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
 
