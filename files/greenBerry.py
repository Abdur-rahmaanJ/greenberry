# -*- coding: utf-8 -*-
"""
Created on Tue Dec 26 21:53:56 2017

@author: ARJ 
Notes : All Rights Reserved

_______________________________________________________________________________
COMMON COMPILER THEORY SYNTAX P1

- eof -> end of file character : tells the lexer that it has encountered the 
    end of the file. Current methods just return a value telling it has reached
    the end
- grammar -> set of rules that describe a language
- context-free grammar -> rules that define a language independent of syntax
- Context-Free Grammar (CFG) in our case -> a set of rules that 
    describe all possible strings in a given formal language
*** 
it is to be noted that source code are of type strings and as such the word 
'string' is used
***

- production -> production rules specify replacement or substitutions. e.g.
    A → a means that A can be replaced by a. A → a is a production
- start symbol -> In the example below, S is the start symbol
    S → Av
    A → x
    
- terminal   -> does not appear on the left side of a production
- non-terminal -> that which can be broken down further
***
terminal symbol is one thing in grammar and another in syntax analysis. 
see tokens below
***
- term       -> what you add or substract e.g. 1+2+3 i.e. 1 2 3
- factor     -> what you multiply or divide e.g. 3*4*5 i.e 3 4 5
- expression -> combination of term and expression etc
______________________________________________________________________
FORMAL GRAMMAR REPRESENTATIONS

-- Chomsky Normal Form (CNF)
basically has → and | where it means or
normally starts with S to denote Start symbol
Capital letters means replaceable characters

S -> a 
#meaning only possible sentence is the token a

S -> aBa
B -> bb
#B can be replaced with bb 

USE OF |

S -> aBa
B -> bb
B -> aa

can be represented by

S -> aBa
B -> bb | aa

(| means or thus meaning two choices)

the above define strings of fixed length. not useful for programming languages
to solve this we use recursion. see

S -> aBa
B -> bb | aaB

more or less complete description of a computer lang :
    
S -> EXPRESSION
EXPRESSION -> TERM | TERM + EXPRESSION | TERM - EXPRESSION
TERM -> FACTOR | FACTOR * EXPRESSION | FACTOR / EXPRESSION
FACTOR -> NUMBER | ( EXPRESSION )
NUMBER -> 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 | 
          1 NUMBER | 2 NUMBER | 3 NUMBER | 4 NUMBER |
          5 NUMBER | 6 NUMBER | 7 NUMBER | 8 NUMBER |
          9 NUMBER | 0 NUMBER 
          
-- Extended Backus Naur Form (EBNF)
Backus and Naur worked on a representation scheme and others extended on it

uses :== as separator
terminals in ''
[] 0 or 1 occurance of expansion
{} 1 or >1 occurance of expansion

S :== 'a' B 'a'
B :== 'bb'

grammar example
S :== EXPRESSION
EXPRESSION :== TERM | TERM { [+,-] TERM] }
TERM :== FACTOR | FACTOR { [*,/] FACTOR] }
FACTOR :== NUMBER | '(' EXPRESSION ')'
NUMBER :== '1' | '2' | '3' | '4' | '5' | 
           '6' | '7' | '8' | '9' | '0' | 
           '1' NUMBER | '2' NUMBER | '3' NUMBER | 
           '4' NUMBER | '5' NUMBER | '6' NUMBER |
           '7' NUMBER | '8' NUMBER | '9' NUMBER | '0' NUMBER 


______________________________________________________________________
GRAMMAR.TXT

in many languages you have a file defining the grammar in a file called 
grammar.txt (which greenBerry's author has not yet included upto now). 

1) C lang : see end of file
    
2)
Here is a more common example :

program = stmts eof "program1" ;
 
stmts = stmt "stmts1" (';' stmt "stmts2")* ;
 
stmt = "stmt1" 
     | selection "stmt2"
     | iteration "stmt3"
     | assignment "stmt4" ;
      
selection = 'if' alts 'fi' "selection1" ;
 
iteration = 'do' alts 'od' "iteration1" ;
 
alts = alt "alts1" ('::' alt "alts2")* ;
 
alt = guard '?' stmts "alt1" ;
 
guard = expr "guard1" ;
 
assignment = vars ':=' exprs                  "assignment1"
           | vars ':=' subprogram ':=' exprs  "assignment2"
           |      ':=' subprogram ':=' exprs  "assignment3"
           | vars ':=' subprogram ':='        "assignment4"
           |      ':=' subprogram ':='        "assignment5" ;
           
vars = id "vars1" (',' id "vars2")* ;
 
exprs = expr "exprs1" (',' expr "exprs2")* ;
 
subprogram = id "subprogram1" ;
 
expr = disjunction "expr1" ;
 
disjunction = conjunction "disjunction1" ('|' conjunction "disjunction2")* ;
 
conjunction = negation "conjunction1" ('&' negation "conjunction2")* ;
 
negation = relation "negation1" 
         | '~' relation "negation2" ;
         
relation = sum          "relation1"
         | sum '<'  sum "relation2"
         | sum '<=' sum "relation3"
         | sum '='  sum "relation4"
         | sum '~=' sum "relation5"
         | sum '>=' sum "relation6"
         | sum '>'  sum "relation7" ;
         
sum = (term "sum1" | '-' term "sum2") ('+' term "sum3" | '-' term "sum4")* ;
 
term = factor "term1" 
      ('*' factor "term2" | '/' factor "term3" | '//' factor "term4")* ;
      
factor = 'true'       "factor1"
       | 'false'      "factor2"
       | integer      "factor3"
       | real         "factor4"
       | id           "factor5"
       | '(' expr ')' "factor6"
       | 'b2i' factor "factor7"
       | 'i2r' factor "factor8"
       | 'r2i' factor "factor9"
       | 'rand'       "factor10" ;

3)
another variety

program ::= func | e
func	::= DEFINE type id ( decls ) block program
block	::= BEGIN decls stmts END program
decls	::= decls decl | e
decl	::= type id;
type	::= type [ num ] | basic
stmts	::= stmts stmt | e
stmt	::= id = bool;
	 |  decls
	 |  IF ( bool ) stmt |  IF ( bool ) stmt ELSE stmt
	 |  WHILE ( bool ) stmt	 |  DO stmt WHILE ( bool );
	 |  BREAK;
	 |  PRINT lit;
	 |  READ id;
	 |  block
	 |  RETURN bool;
bool	::= bool OR join | join
join	::= join AND equality | equality
equality ::= equality == rel | equality != rel | rel
rel	::= expr < expr | expr <= expr | expr >= expr |
		expr > expr | expr
expr	::= expr + term | expr - term | term
term	::= term * unary | term / unary | unary
unary	::= NOT unary | - unary | factor
factor	::= ( bool ) | id | num | real | true | false


____________________________________________________________________________
COMMON COMPILER THEORY SYNTAX P2
- identifiers(id) -> must be declared before they are used
- litteral        -> fixed values : 11, 'w'
- constants       -> change-once values : once declared / set cannot be altered
- variables       -> multiple changes allowed

- CBC lexer -> CBC means Char/character by Char/character, a program that goes 
    over the source text character by character
    
- keyword   -> word having a special meaning to the compiler

- lexeme    -> set of characters identified by the lexer
    e.g x = 5 + pencils
    lexemes : x,=,5,+,pencils
    
- pattern   -> set of rules that specifies when the sequence of characters from 
    an input makes a token
    
- token     -> typically a mapping of value and type. common cases :
    1) identifiers
    2) keywords
    3) operators
    4) special symbols
    5) constant e.g. PI 
    
    for more info see STEP 1 in analysis
    token and terminal symbol are in essence the same

- front-end : from high-level language to some intermediate language
- back-end : from some intermediary language to binary code
    in each steps below, front-end and back-end has been labelled in ()
__________ __ __ 
CASE :
x = 1 + y * 5

symbol table : contains symbol, type and scope (psst + - * don't have scope, 
    referring to id)

_______________________________________________________________________________
ANALYSIS
_________
(front-end)
STEP 1 : Lexical Analysis -> output tokens
info : tool known as Lexer or Scanner

x     -> identifier (id)
=     -> assignment operator
1 + y -> expression
        1     -> litteral, type : number
        +     -> add operator
        y     -> identifier (id)
*     -> mult operator
5     -> litteral, type : number

transformed into tokens where 
<id, 1> means first id
<=> for eqal sign as it is a litteral :
tokens :
<id, 1> <=> <num, 1> <+> <id, 2> <*> <num, 5>

starting here and in subsequent steps, symbol table :
    1. x
    2. y

Normally : Skips whitespace (new line, space, tabs ...), 
ignore comments (single line, multiline)
_________
(front-end)
STEP 2 : Syntax analysis -> checks order of tokens
info : tool known as Parser

<id, 1> <=> <num, 1> (verified)
<id, 1> <=> <*> (unverified)

also generates parse trees
                        ASSIGN
                          |
               id         =          expression
                |                        |
                x         expression     +     expression
                              |                   |
                            number   expression   *   expression
                              1          |                |
                                     identifier         number        
                                         y                5
 syntax tree as 
 
                                  =
                    <id, 1>                +
                                <num, 1>           *
                                           <id, 2>    <num, 5>
                                           
trees are often generated in JSON format or XML format

JSON
{
        'some_id':
        {
                'type':....,
                'another_property':....,
                'etc':....,
        }
}
        
XML
<function>
    <keyword> func </keyword>
</function>

etc ... just a good enough to represent and handle format
_________
(front-end)
STEP 3 : Semantical Analysis (semantics means meaning)
generates extended syntax tree
handles type corecion for the parse tree above (given y was float)
                                  =
                    <id, 1>                +
                                <num, 1>           *
                                           <id, 2>    int_to_float
                                                      <num, 5>
_______________________________________________________________________________
SYNTHESIS

_________
(front-end)
STEP 1: intermediate code generation
the farthest nodes are reduced like
t1 = tofloat(5)
t2 = t1 * id_2
t3 = 1  + t2
id_1 = t3

_________
(front-end)
STEP 2: optimisation
t1 = 5.0 * id_2
id_1 = 1 + t1

high-level to high-level stops here

_________
(back-end)
STEP 3: code generation
the above in assembly or VM (Virtual Machine) code (psst worth a try)

_________
(back-end)
STEP 4: target specific optimisation








Bibliography :
    - wikipaedia.com
    - dragon book
    - tiger book
    - mdh.se lectures 07/04, compiler-intro
    - Compiler Basics, James Alan Farrell (1995)
    - Vipul97 on github
    - OrangeAaron on github
    - Elements of Computing Systems, MIT Press, Nisan & Schocken
    - Basics of Compiler Design, Torben Ægidius Mogensen
    - stackoverflow.com
    - tutorialspoint.com
    - dartmouth.edu, Bill McKeeman (2007)

useful demos :
    http://effbot.org/zone/simple-top-down-parsing.htm
"""

#import pdb

from gbtools.lexer import Lexer

from collections import OrderedDict

"""
HACK VERSION
- unstructured _ unethical _ coded to run
- structuration in process
- you don't need the above knowledge to build something but knowing it helps
"""



L_user = 'dear berry'
#bot test
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
    
class T: #type
    ES = 'ending statement'
    BO = 'bool operator'
    EO = 'equal operator'
    VI = 'var type identifier'
    VD = 'values delimiter'
    AS = 'array symbol'
    

    
class E:
    global L_user
    beg = ''
    FOR = beg + L_user + ' you made a mistake on a for loop on line'
    IF = beg + L_user + ' you made a mistake on an if statement on line'
    FUNCDEF = beg + L_user + ' you ill defined a function on line'
    FUNCCALL = beg + L_user + ' you wrongly called a function on line'
    CLASSNAME = beg + L_user + ' you pointed to an inexistent class'
    CLASSDEC = beg + L_user + ' you wrongly declared a class on line'
    CLASSACT = beg + L_user + ' you wrongly called an action on line'
    CLASSATT = beg + L_user + ' you wrongly specified an attribute on line'
    PRINT = beg + L_user + ' you wrongly used print on line'
    VARREF =  beg + L_user + ' you wrongly referenced a variable on line'
    EVAL = beg + L_user + ' you wrongly used eval on line'
    STRING = beg + L_user + ' you used string wrongly  on line'
    PLOT = beg + L_user + ' you plotted wrongly on line'
    DEBUG = beg + L_user + ' wrong set command on line'
    TO = beg + L_user + ' missed word to on line'
    EQUAL = beg + L_user + ' expecting = on line on line'
    COLON = beg + L_user + ' expected : on line'
    ADD = beg + L_user + ' wrong add statement'
    
    
class M: #memory
    g_vars = {}
    g_fs = {}
    g_cls = {}
    
class F: #flags
    bStart = 100 #block start
    bEnd = 0
    isDebugOn = 0
    
class Debug_cp(object):
    def __init__(self, name):
        self.name = name
        self.var = 1
    
    def run(self):
        print(self.name,'*** entered cp',self.var)
        self.var += 1
        
#another lex woulde be to identify blobks first this is a side effect
MATH_OPS = ['+','-','*','/']
BOOLS = [S.TRUE, S.FALSE]
BOOL_OPS = [S.GREATER, S.LESS]
EOS = [S.NL, S.EOF]

def greenBerry_eval(x):
    global L_user
        
    def printd(this, *args):
        a = F.isDebugOn
        if a == 1:
            print(' '*5,'@debug->', this)
        for arg in args:
            print(' '*5,'@debug->', arg)
            
    def lex(x, KWDs, **keyword_parameters):
        words = []
        cup =''
        for i, elem in enumerate(x):
            if elem != ' ':
                cup += elem
            if i+1 >= len(x) or x[i+1] == ' ' or x[i+1] in KWDs or elem in KWDs:
                if cup != '':
                    words.append(cup)
                    cup = ''
        if('add_eof' in keyword_parameters):
            if keyword_parameters['add_eof'] == 1:
                words.append(S.EOF)
        return words
    
    def search(i, offset, words, delimeters):
        base = i+offset
        j = 1
        string = ''
        while base+j < len(words):
            if words[base+j] in delimeters:
                break
            else:
                string += words[base+j] + ' '
                j += 1
        return string
    
    def search_toks(i, offset, words, delimeters):
        base = i+offset
        j = 1
        string = []
        while base+j < len(words):
            if words[base+j] in delimeters:
                break
            else:
                string.append(words[base+j])
                j += 1
        return string
    
    def search_symbol(i, offset, words, delimeters): #i to be resolved
        base = i+offset
        j = 1
        while base+j < len(words):
            if words[base+j] in delimeters:
                break
            else:
                j += 1
        return [words[base+j], base+j]
        
    def print_handling(g_vars, i, words): #print
    #if words[i-1] != S.COLON:
        try:
            if i+1 < len(words) and words[i+1] not in [S.STRING, S.EVAL, S.VAR_REF]:
                print(words[i+1])
            elif i+1 < len(words) and words[i+1] == S.VAR_REF:
                try:
                    print(var_ref_handling(i+1, words, g_vars))
                except:
                    print(E.VARREF,line)
            elif i+1 < len(words) and words[i+1] == S.EVAL:
                try:
                    print(eval(words[i+2]))
                except:
                    print(E.EVAL,line)
            elif i+1 < len(words) and words[i+1] == S.STRING:
                try:
                    print(search(i, 1, words, [S.NL, S.EOF]))
                except:
                    print(E.STRING,line)
        except:
            print(E.PRINT)    
            
    def linear_plot(dataX, labelX, dataY, labelY):
        try:
            import matplotlib.pyplot as plt
            plt.plot(dataX, dataY)
            plt.xlabel(labelX)
            plt.ylabel(labelY)
            plt.show()
        except ImportError:
            print('matplotlib unimported')
            
    def plot_handling(i, words):
        try:
            dataX = list(map(int, words[i+1].split(",")))
            labelX = words[i+2].split('-')[1]
            dataY = list(map(int, words[i+3].split(",")))
            labelY = words[i+4].split('-')[1]
            printd(labelY)
            linear_plot(dataX, labelX, dataY, labelY) 
        except:
            print(E.PLOT)
    
      
    def simple_parse(g_vars, i, elem, words):
        #print('--',i, elem)
        if elem == S.VAR: #var x = 1
            var_val = var_data(i+2, words, [S.NL, S.EOF])
            g_vars[words[i+1]] = var_val
                
        elif elem == S.PRINT :
            print_handling(g_vars, i, words)
            
        elif elem == S.PLOT:
            plot_handling(i, words)
                
    def simple_parse2(g_vars, words):
        for i, elem in enumerate(words):
            if elem == S.VAR:
                var_val = var_data(i+2, words, [S.NL, S.EOF])
                g_vars[words[i+1]] = var_val
            elif elem == S.PRINT :
                print_handling(g_vars, i, words)
            elif elem == S.PLOT:
                plot_handling(i, words)
                
    def var_data(equal_i, words, delimeters): #var x = 1
        value = 0
        type = None
        if words[equal_i+1] == S.STRING:
            value = search(equal_i+1, 0, words, delimeters)
            type = 'string'
        elif words[equal_i+1] == S.VAR_REF:
            value = M.g_vars[words[equal_i+2]][0]
            type = 'var_ref'
        elif words[equal_i+1].isdigit():
            value = words[equal_i+1]
            type = 'number'
        elif words[equal_i+1] == S.SQL:
            value = search(equal_i, 1, words, [S.SQR])
            type = 'array'
        elif words[equal_i+1] == S.BOOL:
            if words[equal_i+2] == S.TRUE or words[equal_i+2] == '1':       
                value = words[equal_i+2]
                type = 'bool_1'
            if words[equal_i+2] == S.FALSE or words[equal_i+2] == '0':       
                value = words[equal_i+2]
                type = 'bool_0'
            
        else:
            value = words[equal_i+1]
            type = 'word'
        return [value, type]
    
    def var_type(string): #var x = 1
        type = None
        words = lex(x, KWDs)
        if words[0] == S.STRING:
            type = 'string'
        elif words[0] == S.VAR_REF:
            type = 'var_ref'
        elif words[0].isdigit():
            type = 'number'
        elif words[0] == S.SQL:
            type = 'array'
        elif words[0] == S.BOOL:
            if words[1] == S.TRUE or words[1] == '1':  
                type = 'bool_1'
            if words[1] == S.FALSE or words[1] == '0':    
                type = 'bool_0'            
        else:
            type = 'word'
        return type
        
    
    def var_ref_handling(at_i, words, g_vars): #@y[1]
        name = words[at_i+1]#class debug
        type = g_vars[name][1]
        value = g_vars[name][0]
        returned_val = 0
        if type == 'array' and words[at_i+2] != S.SQL:
            returned_val = value
        elif type == 'array' and words[at_i+2] == S.SQL:
            value = value.split(S.COMMA)
            returned_val = value[int(words[at_i+3])].strip()
        else:
            returned_val = value
        
        return returned_val
            
        
    KWDs = [S.VAR, S.EQUAL, S.PRINT, S.NL, S.NUMBER, 
            S.STRING, S.EVAL, S.VAR_REF, S.PLOT, S.FOR,
            S.IF,S.CLASS, S.ACTION, S.COMMA, S.MAKE, S.IS,
            S.MAKE, S.ADD, S.TO, S.SEE, S.COLON, S.ATTRIB,
            S.SQL, S.SQR] #future direct conversion to list
    g_vars = M.g_vars
    g_fs = M.g_fs
    g_cls = M.g_cls
    words = lex(x, KWDs, add_eof=1)
    printd(words) 
    line = 1
    '''
    if elem.value == S.NL
    error : elem.line
    '''
    for i, elem in enumerate(words):
        #printd(elem)
        if elem == S.NL:
            line += 1
        elif elem == S.FOR:
            try:
                F.bStart = i
                
                times_by = int(words[i+1])
                base = i+3
                j = 1
                string = ''
                while base+j < len(words):
                    if words[base+j] == S.NL or words[base+j] == S.EOF:
                        break
                    else:
                        string += words[base+j] + ' '
                        j += 1
                wds = lex(string, KWDs)
                printd(wds)
                for d in range(times_by):
                    simple_parse2(g_vars, wds)
                #colon_i = search_symbol(i, 1, words, [S.COLON])[1]
                end_i = search_symbol(i, 1, words, [S.NL, S.EOF])[1]
                F.bEnd = end_i
            except:
                print(E.FOR, line)
                
        elif elem == S.IF: #to be rededefined
            try:
                F.bStart = i
                L, R = 0, 0
                raw = search_symbol(i, 1, words, [S.EQUAL, S.LESS, S.GREATER])
                symbol = raw[0]
                symbol_i = raw[1]
                to_do = search(i, 4, words, [S.NL, S.EOF])
                wds = lex(to_do, KWDs)
                if words[i+1] == S.VAR_REF:
                    #print('L @ detected')
                    L = g_vars[words[i+2]][0]
                elif words[i+1].isdigit():
                    #print('L int detected')
                    L = int(words[i+1])
                else:
                    #print('L str detected')
                    L = search(i, 0, words, [symbol, S.COLON])
                    
                if words[symbol_i+1] == S.VAR_REF:
                    #print('R @ detected')
                    R = g_vars[words[symbol_i+2]][0]
                elif words[symbol_i+1].isdigit():
                    #print("R", words[symbol_i+1])
                    R = int(words[symbol_i+1])
                else:
                    #print('R str detected')
                    R = search(symbol_i, 0, words, [S.COLON])
                #print(L, R, symbol)
                if symbol == S.EQUAL:
                    if L == R:
                        simple_parse2(g_vars, wds)
                elif symbol == S.GREATER:
                    if L > R:
                        simple_parse2(g_vars, wds)
                if symbol == S.LESS:
                    if L < R:
                        simple_parse2(g_vars, wds)
                #colon_i = search_symbol(i, 1, words, [S.COLON])[1]
                end_i = search_symbol(i, 1, words, [S.NL, S.EOF])[1]
                F.bEnd = end_i
            except:
                print(E.IF, line)
            
            #resolve flag
        
        elif elem == S.FUNCDEF: #func vector : print aaa #func vector x : print @x
            params = []
            try:
                
                F.bStart = i
                func_name = words[i+1]
                if words[i+2] == S.COLON:
                    body = search(i, 2, words, [S.NL, S.EOF])
                    g_fs[func_name] = {'params':None, 'body':body}
                else :
                    params = search_toks(i, 1, words, [S.COLON])
                    col_i = search_symbol(i, 1, words, [S.COLON])[1]
                    body = search(col_i, 0, words, [S.NL, S.EOF])
                    registry = OrderedDict()
                    for param in params:
                        registry[param] = None
                    g_fs[func_name] = {'params':registry, 'body':body}
                    
                #colon_i = search_symbol(i, 1, words, [S.COLON])[1]
                end_i = search_symbol(i, 1, words, [S.NL, S.EOF])[1]
                F.bEnd = end_i
            except:
                print(E.FUNCDEF, line)
            
        elif elem == S.FUNCCALL: #call vector
            try:
                func_name = words[i+1]
                if g_fs[func_name]['params'] == None:
                    #print(g_fs)
                    #print(func_name)
                    wds = lex(g_fs[func_name]['body'], KWDs)
                    simple_parse2(g_vars, wds)
                else:
                    param_vals = search_toks(i, 1, words, [S.NL, S.EOF])
                    registry = g_fs[func_name]['params']
                    i  = 0
                    for key in registry:
                        registry[key] = [param_vals[i], var_type(param_vals[i])] #data
                        i += 1
                    wds = lex(g_fs[func_name]['body'], KWDs)
                    simple_parse2(registry, wds)
            except:
                print(E.FUNCCALL, line)
            
        elif elem == S.CLASS: #class Man : power = 10 action walk : print a
            #attrs = {} future
            try:
                F.bStart = i
                
                class_name = words[i+1] #subsequent changed to action for mult attribs
                attr_name = words[i+3] #search_symbol var_data(i+4, words, [S.NL, S.EOF])
                attr_val = var_data(i+4, words, [S.ACTION]) 
                action_name = words[i+7]
                action_body = search(i+7, 1, words, [S.NL, S.EOF])
                g_cls[class_name] = {
                        'attributes':{attr_name:attr_val},
                        'actions':{action_name:action_body}
                        }
                
                #colon_i = search_symbol(i, 1, words, [S.COLON])[1]
                end_i = search_symbol(i, 1, words, [S.NL, S.EOF])[1]
                F.bEnd = end_i
                """
                class_name = {
                name = name,
                attributes = {
                        x = 1,
                        y = 2
                        }
                methods = {
                        walk = string here,
                        raise hand = string here
                        }
                }
                """
            except:
                print(E.CLASSDEC, line)
                
        elif elem == S.MAKE:
            try:
                class_name = words[i+1]
                if class_name not in g_cls:
                    print('wrong class name berry')
                action_name = words[i+2]
                raw_text = g_cls[class_name]['actions'][action_name]
                wds = lex( raw_text, KWDs)
                simple_parse2(g_vars, wds)
            except:
                print(E.CLASSACT, line)
            
        elif elem == S.SEE: #see power of Man
            try:
                attr = words[i+1]
                class_name = words[i+3]
                print(g_cls[class_name]['attributes'][attr][0])
            except:
                print(E.CLASSATT, line)
                
        elif elem == S.ADD: #add to Man attribute name = string i am me
            try:
                F.bStart = i
                if words[i+1] == S.TO:
                    if words[i+2] in g_cls:
                        if words[i+3] == S.ATTRIB:
                            if words[i+5] == S.EQUAL:
                                value = var_data(i+5, words, [S.NL, S.EOF])
                                g_cls[words[i+2]]['attributes'][words[i+4]] = value 
                            else:
                                print(E.EQUAL, line)
                        elif words[i+3] == S.ACTION: #add to Man action run : print running...
                            if words[i+5] == S.COLON:
                                g_cls[words[i+2]]['actions'][words[i+4]] = search(i, 5, words, [S.NL, S.EOF])
                            else:
                                print(E.COLON, line)
                            
                    else:
                        print(E.CLASSNAME, line)
                else:
                    print(E.TO, line)
                end_i = search_symbol(i, 1, words, [S.NL, S.EOF])[1]
                F.bEnd = end_i
            except:
                print(E.ADD, line)
        elif elem == S.SET :#set debug on - set debug off
            try:
                if words[i+1] == 'debug':
                    if words[i+2] == 'on':
                        F.isDebugOn = 1
                    elif words[i+2] == 'off':
                        F.isDebugOn = 0
            except:
                print(E.DEBUG, line)
        else:
            if i < F.bStart or i > F.bEnd :
                simple_parse(g_vars, i, elem, words)  
                
        
    printd(g_vars)
    printd(g_fs)
    printd(g_cls)

# python greenBerry_REPL.py
    #psst coding only <600 lines
    
"""
Here is a grammar.txt for the C lanaguage, which reveals quite a few 
tricks you might not know about 

primary-expression
    identifier
    constant
    string-literal
    ( expression )

postfix-expression
    primary-expression
    postfix-expression [ expression ]
    postfix-expression ( )
    postfix-expression ( argument-expression-list )
    postfix-expression . identifier
    postfix-expression -> identifier
    postfix-expression ++
    postfix-expression --

argument-expression-list
    assignment-expression
    argument-expression-list , assignment-expression

unary-expression
    postfix-expression
    ++ unary-expression
    -- unary-expression
    unary-operator cast-expression
    sizeof unary-expression
    sizeof ( type-name )

unary-operator
    &
    *
    +
    -
    ~
    !

cast-expression
    unary-expression
    ( type-name ) cast-expression

multiplicative-expression
    cast-expression
    multiplicative-expression * cast-expression
    multiplicative-expression / cast-expression
    multiplicative-expression % cast-expression

additive-expression
    multiplicative-expression
    additive-expression + multiplicative-expression
    additive-expression - multiplicative-expression

shift-expression
    additive-expression
    shift-expression << additive-expression
    shift-expression >> additive-expression

relational-expression
    shift-expression
    relational-expression < shift-expression
    relational-expression > shift-expression
    relational-expression <= shift-expression
    relational-expression >= shift-expression

equality-expression
    relational-expression
    equality-expression == relational-expression
    equality-expression != relational-expression

AND-expression
    equality-expression
    AND-expression & equality-expression

exclusive-OR-expression
    AND-expression
    exclusive-OR-expression ^ AND-expression

inclusive-OR-expression
    exclusive-OR-expression
    inclusive-OR-expression | exclusive-OR-expression

logical-AND-expression
    inclusive-OR-expression
    logical-AND-expression && inclusive-OR-expression

logical-OR-expression
    logical-AND-expression
    logical-OR-expression || logical-AND-expression

conditional-expression
    logical-OR-expression
    logical-OR-expression ? expression : conditional-expression

assignment-expression
    conditional-expression
    unary-expression assignment-operator assignment-expression

assignment-operator
    =
    *=
    /=
    %=
    +=
    -=
    <<=
    >>=
    &=
    ^=
    |=

expression
    assignment-expression
    expression , assignment-expression

constant-expression
    conditional-expression

#
# C declaration rules
#

declaration
    declaration-specifiers ;
    declaration-specifiers init-declarator-list ;

declaration-specifiers
    storage-class-specifier
    type-specifier
    type-qualifier
    storage-class-specifier declaration-specifiers
    type-specifier          declaration-specifiers
    type-qualifier          declaration-specifiers

init-declarator-list
    init-declarator
    init-declarator-list , init-declarator

init-declarator
    declarator
    declarator = initializer

storage-class-specifier
    typedef
    extern
    static
    auto
    register

type-specifier
    void
    char
    short
    int
    long
    float
    double
    signed
    unsigned
    struct-or-union-specifier
    enum-specifier
    typedef-name

struct-or-union-specifier
    struct-or-union { struct-declaration-list }
    struct-or-union identifier { struct-declaration-list }
    struct-or-union identifier

struct-or-union
    struct
    union

struct-declaration-list
    struct-declaration
    struct-declaration-list struct-declaration

struct-declaration
    specifier-qualifier-list struct-declarator-list ;

specifier-qualifier-list
    type-specifier
    type-qualifier
    type-specifier specifier-qualifier-list 
    type-qualifier specifier-qualifier-list 

struct-declarator-list
    struct-declarator
    struct-declarator-list , struct-declarator

struct-declarator
    declarator
     constant-expression
    declarator  constant-expression

enum-specifier
    enum { enumerator-list }
    enum identifier { enumerator-list }
    enum identifier

enumerator-list
    enumerator
    enumerator-list , enumerator

enumerator
    enumeration-constant
    enumeration-constant = constant-expression

enumeration-constant
    identifier

type-qualifier
    const
    volatile

declarator
    direct-declarator
    pointer direct-declarator

direct-declarator
    identifier
    ( declarator )
    direct-declarator [ ]
    direct-declarator [ constant-expression ]
    direct-declarator ( )
    direct-declarator ( parameter-type-list )
    direct-declarator ( identifier-list )

pointer
     *
     * pointer
     * type-qualifier-list
     * type-qualifier-list pointer

type-qualifier-list
    type-qualifier
    type-qualifier-list type-qualifier

parameter-type-list
    parameter-list
    parameter-list , ...

parameter-list
    parameter-declaration
    parameter-list , parameter-declaration

parameter-declaration
    declaration-specifiers declarator
    declaration-specifiers
    declaration-specifiers abstract-declarator

identifier-list
    identifier
    identifier-list , identifier

type-name
    specifier-qualifier-list
    specifier-qualifier-list abstract-declarator

abstract-declarator
    pointer
    direct-abstract-declarator
    pointer direct-abstract-declarator

direct-abstract-declarator
    ( abstract-declarator )
    [ ]
    [ constant-expression ]
    ( )
    ( parameter-type-list )
    direct-abstract-declarator [ ]
    direct-abstract-declarator [ constant-expression ]
    direct-abstract-declarator ( )
    direct-abstract-declarator ( parameter-type-list )

typedef-name
    identifier

initializer
    assignment-expression
    { initializer-list }
    { initializer-list , }

initializer-list
    initializer
    initializer-list , initializer

#
# C statement rules
#

statement
    labeled-statement
    compound-statement
    expression-statement
    selection-statement
    iteration-statement
    jump-statement

labeled-statement
    identifier : statement
    case constant-expression : statement
    default : statement

compound-statement
    { }
    { declaration-list }
    { statement-list }
    { declaration-list statement-list }

declaration-list
    declaration
    declaration-list declaration

statement-list
    statement
    statement-list statement

expression-statement
    ;
    expression ;

selection-statement
    if ( expression ) statement
    if ( expression ) statement else statement
    switch ( expression ) statement

iteration-statement
    while ( expression ) statement
    do statement while ( expression ) ;
    for (            ;            ;            ) statement
    for (            ;            ; expression ) statement
    for (            ; expression ;            ) statement
    for (            ; expression ; expression ) statement
    for ( expression ;            ;            ) statement
    for ( expression ;            ; expression ) statement
    for ( expression ; expression ;            ) statement
    for ( expression ; expression ; expression ) statement

jump-statement
    goto identifier ;
    continue ;
    break ;
    return ;
    return expression ;

translation-unit
    external-declaration
    translation-unit external-declaration

external-declaration
    function-definition
    declaration

function-definition
                           declarator                  compound-statement
    declaration-specifiers declarator                  compound-statement
                           declarator declaration-list compound-statement
    declaration-specifiers declarator declaration-list compound-statement
"""













