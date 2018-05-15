# -*- coding: utf-8 -*-
"""
Created on Tue Dec 26 21:53:56 2017

@author: ARJ 
Notes : All Rights Reserved
see theory_notes_simple.py
"""

# import pdb
# from gbtools.lexer import Lexer
# from gbsymbols import S

from collections import OrderedDict

"""
HACK VERSION
- unstructured _ unethical _ coded to run
- structuration in process
- you don't need the above knowledge to build something but knowing it helps
"""


L_user = 'dear berry'
# bot test


class S:  # Symbols keywords
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


class T:  # type
    ES = 'ending statement'
    BO = 'bool operator'
    EO = 'equal operator'
    VI = 'var type identifier'
    VD = 'values delimiter'
    AS = 'array symbol'

    
class E:  # error
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
    VARREF = beg + L_user + ' you wrongly referenced a variable on line'
    EVAL = beg + L_user + ' you wrongly used eval on line'
    STRING = beg + L_user + ' you used string wrongly  on line'
    PLOT = beg + L_user + ' you plotted wrongly on line'
    DEBUG = beg + L_user + ' wrong set command on line'
    TO = beg + L_user + ' missed word to on line'
    EQUAL = beg + L_user + ' expecting = on line'
    COLON = beg + L_user + ' expected : on line'
    ADD = beg + L_user + ' wrong add statement'
    
    
class M:  # memory
    g_vars = {}
    g_fs = {}
    g_cls = {}


class F:  # flags
    bStart = 100  # block start
    bEnd = 0
    isDebugOn = 0


class Debug_cp(object):
    def __init__(self, name):
        self.name = name
        self.var = 1
    
    def run(self):
        print(self.name,'*** entered cp',self.var)
        self.var += 1


# another lex would be to identify blobks first this is a side effect
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
        cup = ''
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
    # if words[i-1] != S.COLON:
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
            if words[i+2] == S.EQUAL:
                var_val = var_data(i+2, words, [S.NL, S.EOF])
                g_vars[words[i+1]] = var_val
            else:
                print(E.EQUAL, line)
                
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
    
    def var_type(string):  # var x = 1
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

    def var_ref_handling(at_i, words, g_vars):  # @y[1]
        name = words[at_i+1]  # class debug
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
            S.SQL, S.SQR]  # future direct conversion to list
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
        # printd(elem)
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
                # colon_i = search_symbol(i, 1, words, [S.COLON])[1]
                end_i = search_symbol(i, 1, words, [S.NL, S.EOF])[1]
                F.bEnd = end_i
            except:
                print(E.FOR, line)
                
        elif elem == S.IF: # to be rededefined
            try:
                F.bStart = i
                L, R = 0, 0
                raw = search_symbol(i, 1, words, [S.EQUAL, S.LESS, S.GREATER])
                symbol = raw[0]
                symbol_i = raw[1]
                to_do = search(i, 4, words, [S.NL, S.EOF])
                wds = lex(to_do, KWDs)
                if words[i+1] == S.VAR_REF:
                    # print('L @ detected')
                    L = g_vars[words[i+2]][0]
                elif words[i+1].isdigit():
                    # print('L int detected')
                    L = int(words[i+1])
                else:
                    # print('L str detected')
                    L = search(i, 0, words, [symbol, S.COLON])
                    
                if words[symbol_i+1] == S.VAR_REF:
                    # print('R @ detected')
                    R = g_vars[words[symbol_i+2]][0]
                elif words[symbol_i+1].isdigit():
                    # print("R", words[symbol_i+1])
                    R = int(words[symbol_i+1])
                else:
                    # print('R str detected')
                    R = search(symbol_i, 0, words, [S.COLON])
                # print(L, R, symbol)
                if symbol == S.EQUAL:
                    if L == R:
                        simple_parse2(g_vars, wds)
                elif symbol == S.GREATER:
                    if L > R:
                        simple_parse2(g_vars, wds)
                if symbol == S.LESS:
                    if L < R:
                        simple_parse2(g_vars, wds)
                # colon_i = search_symbol(i, 1, words, [S.COLON])[1]
                end_i = search_symbol(i, 1, words, [S.NL, S.EOF])[1]
                F.bEnd = end_i
            except:
                print(E.IF, line)
            
            # resolve flag
        
        elif elem == S.FUNCDEF:  # func vector : print aaa #func vector x : print @x
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
                    
                # colon_i = search_symbol(i, 1, words, [S.COLON])[1]
                end_i = search_symbol(i, 1, words, [S.NL, S.EOF])[1]
                F.bEnd = end_i
            except:
                print(E.FUNCDEF, line)
            
        elif elem == S.FUNCCALL: # call vector
            try:
                func_name = words[i+1]
                if g_fs[func_name]['params'] is None:
                    # print(g_fs)
                    # print(func_name)
                    wds = lex(g_fs[func_name]['body'], KWDs)
                    simple_parse2(g_vars, wds)
                else:
                    param_vals = search_toks(i, 1, words, [S.NL, S.EOF])
                    registry = g_fs[func_name]['params']
                    i  = 0
                    for key in registry:
                        registry[key] = [param_vals[i], var_type(param_vals[i])]  # data
                        i += 1
                    wds = lex(g_fs[func_name]['body'], KWDs)
                    simple_parse2(registry, wds)
            except:
                print(E.FUNCCALL, line)
            
        elif elem == S.CLASS:  # class Man : power = 10 action walk : print a
            # attrs = {} future
            try:
                F.bStart = i
                
                class_name = words[i+1]  # subsequent changed to action for mult attribs
                attr_name = words[i+3]  # search_symbol var_data(i+4, words, [S.NL, S.EOF])
                attr_val = var_data(i+4, words, [S.ACTION]) 
                action_name = words[i+7]
                action_body = search(i+7, 1, words, [S.NL, S.EOF])
                g_cls[class_name] = {
                        'attributes':{attr_name:attr_val},
                        'actions':{action_name:action_body}
                        }
                
                # colon_i = search_symbol(i, 1, words, [S.COLON])[1]
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
            
        elif elem == S.SEE:  # see power of Man
            try:
                attr = words[i+1]
                class_name = words[i+3]
                print(g_cls[class_name]['attributes'][attr][0])
            except:
                print(E.CLASSATT, line)
                
        elif elem == S.ADD:  # add to Man attribute name = string i am me
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
                        elif words[i+3] == S.ACTION:  # add to Man action run : print running...
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
        elif elem == S.SET:  # set debug on - set debug off
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
    














