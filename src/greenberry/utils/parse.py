import inspect
from collections import OrderedDict

from greenberry.debug_cp import *
from greenberry.symbols import *
from greenberry.utils.plot import GreenBerryPlot
from greenberry.utils.print import GreenBerryPrint
from greenberry.utils.var_type import GreenBerryVarType

L_USER = "dear berry"

# another lex would be to identify blobks first this is a side effect
MATH_OPS = ["+", "-", "*", "/"]
BOOLS = [S.TRUE, S.FALSE]
BOOL_OPS = [S.GREATER, S.LESS]
EOS = [S.NL, S.EOF]


class GreenBerryParse:
    def __init__(self):
        print(self, "does not have an initialiser")

    def simple_parse(g_vars, words, line):
        """
        parses simple statements

        variable assignment
        print statement
        ploting

        g_vars is a registry / dictionary storing variables
        """
        for i, elem in enumerate(words):
            if elem == S.VAR:
                var_val = GreenBerryVarType.var_data(i + 2, words, [S.NL, S.EOF])
                g_vars[words[i + 1]] = var_val
            elif elem == S.PRINT:
                GreenBerryPrint.print_handling(g_vars, i, words)
            elif elem == S.PLOT:
                Plot = GreenBerryPlot()
                Plot.plot_handling(i, words, line)
