L_user = "dear berry"


class S:
    """
    contains symbols used in lang
    """

    EOF = "{***end-of-file***}"
    NL = "\n"
    WS = " "
    E = ""

    EQUAL = "="
    LESS = "<"
    GREATER = ">"
    EQUAL_GREATER = ">="
    EQUAL_LESS = "<="
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
    SEE = "see"
    SET = "set"
    ATTRIB = "attribute"
    TABLE = "table"
    AWAIT = "await"
    ELSE = "else"
    IMPORT = "import"
    PASS = "pass"
    NONE = "None"
    BREAK = "break"
    EXCEPT = "except"
    RAISE = "raise"
    FINALLY = "finally"
    RETURN = "return"
    AND = "and"
    CONTINUE = "continue"
    LAMBDA = "lambda"
    TRY = "try"
    AS = "as"
    DEF = "def"
    FROM = "from"
    NONLOCAL = "nonlocal"
    WHILE = "while"
    ASSERT = "assert"
    DEL = "del"
    GLOBAL = "global"
    WITH = "with"
    ASYNC = "async"
    YIELD = "yield"

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
