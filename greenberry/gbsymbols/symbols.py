class S: #Symbols keywords
    EOF = '{***end-of-file***}'
    NL = '\n'
    WS = ' '
    E = ''

    EQUAL = '='
    LESS = '<'
    GREATER = '>'
    COMMA = ','
    SQL = '['
    SQR = ']'

    PRINT = 'print'

    NUMBER = 'number'
    STRING = 'string'
    BOOL = 'bool'

    TRUE = 'true'
    FALSE = 'false'

    EVAL = 'eval'

    VAR = 'var'
    VAR_REF = '@'
    PLOT = 'plot'
    FOR = 'for'
    IF = 'if'
    COLON = ':'
    FUNCDEF = 'func'
    FUNCCALL = 'call'
    CLASS = 'class'
    ACTION = 'action'
    COMMA = ','
    IS = 'is'
    MAKE = 'make'
    ADD = 'add'
    TO = 'to'
    SEE = 'see'
    OF = 'of'
    SET = 'set'
    ATTRIB = 'attribute'
    TABLE = 'table'

    # math
    ODD = 'odd'
    EVEN = 'even'
    PRIME = 'prime'
    PI = 'pi'
    LOG = 'log'
    LOG10 = 'log10'  # log(x) returns the logarithm value of x
    SQROOT = 'sqroot'  # sqroot(x) should return square root value of x
    SQ = 'square'  # square(x) returns square value of x
    TAN = 'tan'  # tan(x) returns tangent value of x
    COS = 'cos'  # cos(x) returns cosine value of x
    SIN = 'sin'  # sin(x) returns sine value of x
    HYP = 'hyp'  # returns sqroot(x**2 + y**2), takes in two parameters
