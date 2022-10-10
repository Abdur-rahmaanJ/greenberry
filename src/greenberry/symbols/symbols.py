L_user = "dear berry"

class S:  # Symbols keywords
    EOF = "{***end-of-file***}"
    NL = "\n"
    WS = " "
    E = ""

    EQUAL = "="
    LESS = "<"
    GREATER = ">"
    COMMA = ","
    SQL = "["
    SQR = "]"

    PRINT = "print"

    NUMBER = "number"
    STRING = "string"
    BOOL = "bool"

    TRUE = "true"
    FALSE = "false"

    EVAL = "eval"

    VAR = "var"
    VAR_REF = "@"
    PLOT = "plot"
    FOR = "for"
    IF = "if"
    COLON = ":"
    FUNCDEF = "func"
    FUNCCALL = "call"
    CLASS = "class"
    ACTION = "action"
    COMMA = ","
    IS = "is"
    MAKE = "make"
    ADD = "add"
    TO = "to"
    SEE = "see"
    OF = "of"
    SET = "set"
    ATTRIB = "attribute"
    TABLE = "table"

    # math
    ODD = "odd"
    EVEN = "even"
    PRIME = "prime"
    PI = "pi"
    LOG = "log"
    LOG10 = "log10"  # log(x) returns the logarithm value of x
    SQROOT = "sqroot"  # sqroot(x) should return square root value of x
    SQ = "square"  # square(x) returns square value of x
    TAN = "tan"  # tan(x) returns tangent value of x
    COS = "cos"  # cos(x) returns cosine value of x
    SIN = "sin"  # sin(x) returns sine value of x
    HYP = "hyp"  # returns sqroot(x**2 + y**2), takes in two parameters


class T:
    """
    type of symbols
    """

    ES = "ending statement"
    BO = "bool operator"
    EO = "equal operator"
    VI = "var type identifier"
    VD = "values delimiter"
    AS = "array symbol"


class E:
    global L_user
    """
    contains error messages
    """
    beg = ""
    FOR = beg + L_user + " you made a mistake on a for loop on line"
    IF = beg + L_user + " you made a mistake on an if statement on line"
    FUNCDEF = beg + L_user + " you ill defined a function on line"
    FUNCCALL = beg + L_user + " you wrongly called a function on line"
    CLASSNAME = beg + L_user + " you pointed to an inexistent class"
    CLASSDEC = beg + L_user + " you wrongly declared a class on line"
    CLASSACT = beg + L_user + " you wrongly called an action on line"
    CLASSATT = beg + L_user + " you wrongly specified an attribute on line"
    PRINT = beg + L_user + " you wrongly used print on line"
    VARREF = beg + L_user + " you wrongly referenced a variable on line"
    EVAL = beg + L_user + " you wrongly used eval on line"
    STRING = beg + L_user + " you used string wrongly  on line"
    PLOT = beg + L_user + " you plotted wrongly on line"
    DEBUG = beg + L_user + " wrong set command on line"
    EQUAL = beg + L_user + " expecting = on line"
    COLON = beg + L_user + " expected : on line"
    ADD = beg + L_user + " wrong add statement"


class M:  # memory
    """
    global memory
    """

    g_vars = {}
    g_fs = {}
    g_cls = {}


class F:
    """
    flags
    """

    bStart = 100  # block start
    bEnd = 0
    isDebugOn = 0