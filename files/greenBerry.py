# -*- coding: utf-8 -*-
"""
Created on Tue Dec 26 21:53:56 2017

@author: ARJ
import matplotlib.pyplot as plt
plt.plot([1,2,3,4])
plt.ylabel('some numbers')
plt.show()
"""
import pdb

L_user = 'dear berry' + ' '

class S: #Symbols
    EOF = '{***end-of-file***}'
    NL = '\n'
    EQUAL = '='
    LESS = '<'
    GREATER = '>'
    PRINT = 'print'
    NUMBER = 'number'
    STRING = 'string'
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
    
class E:
    global L_user
    beg = ''
    FOR = beg + L_user + ' you made a mistake on a for loop on line'
    IF = beg + L_user + ' you made a mistake on an if statement on line'
    FUNCDEF = beg + L_user + ' you ill defined a function on line'
    FUNCCALL = beg + L_user + ' you wrongly called a function on line'
    CLASSDEC = beg + L_user + ' you wrongly declared a class on line'
    CLASSACT = beg + L_user + ' you wrongly called an action on line'
    CLASSATT = beg + L_user + ' you wrongly specified an attribute on line'
    PRINT = beg + L_user + ' you wrongly used print on line'
    VARREF =  beg + L_user + ' you wrongly referenced a variable on line'
    EVAL = beg + L_user + ' you wrongly used eval on line'
    STRING = beg + L_user + ' you used string wrongly  on line'
    PLOT = beg + L_user + ' you plotted wrongly on line'
    
    
class M:
    g_vars = {}
    g_fs = {}
    g_cls = {}
    

#another lex woulde be to identify blobks first this is a side effect

def greenBerry_eval(x):
    global L_user
    class F:
        isPrintOn = 1
        isSimpleParseOn = 1
        isSimpleParse2On = 1
        isBlockOn = 0
        bStart = 100
        bEnd = 0
        
    def printd(this):
        a = 0
        if a == 1:
            print(' '*5,'@debug->', this)
            
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
                    print(g_vars[words[i+2]][1])
                except:
                    print(E.VARREF)
            elif i+1 < len(words) and words[i+1] == S.EVAL:
                try:
                    print(eval(words[i+2]))
                except:
                    print(E.EVAL)
            elif i+1 < len(words) and words[i+1] == S.STRING:
                try:
                    print(search(i, 1, words, [S.NL, S.EOF]))
                except:
                    print(E.STRING)
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
        if F.isBlockOn == 0: #not necessary
            if elem == S.VAR:
                #print('--   * var ass exec *')
                string = search(i, 2, words, [S.NL, S.EOF])
                g_vars[words[i+1]] = ['---', string]
            elif elem == S.PRINT :
                print_handling(g_vars, i, words)
            elif elem == S.PLOT:
                plot_handling(i, words)
                #print(words[base+1], words[base+2], words[base+3])
    def simple_parse2(g_vars, words):
        for i, elem in enumerate(words):
            if elem == S.VAR:
                g_vars[words[i+1]] = [words[i+4], words[i+3]]
            elif elem == S.PRINT :
                print_handling(g_vars, i, words)
            elif elem == S.PLOT:
                plot_handling(i, words)
                
    #x = 'var x = number 1_print x_print @x_print eval (2+3+10-4)_print string ab cd ef' #print var x print flag
    #x = '''
    #print ok
    #if 2 > 3 : var a = number 2
    #if mango = mango : print w
    #if 1 < 2 : var d = number 4
    #func vector : print aaa
    #call vector
    #python greenBerry_REPL.py
    #'''

    KWDs = [S.VAR, S.EQUAL, S.PRINT, S.NL, S.NUMBER, 
            S.STRING, S.EVAL, S.VAR_REF, S.PLOT, S.FOR,
            S.IF,S.CLASS, S.ACTION, S.COMMA, S.MAKE, S.IS,
            S.MAKE, S.ADD, S.TO, S.SEE, S.COLON] #future direct conversion to list
    g_vars = M.g_vars
    g_fs = M.g_fs
    g_cls = M.g_cls
    words = lex(x, KWDs, add_eof=1)
    printd(words) 
    line = 0
    
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
        
        elif elem == S.FUNCDEF: #func vector : print aaa
            try:
                F.bStart = i
                
                g_fs[words[i+1]] = search(i, 2, words, [S.NL, S.EOF])
                
                #colon_i = search_symbol(i, 1, words, [S.COLON])[1]
                end_i = search_symbol(i, 1, words, [S.NL, S.EOF])[1]
                F.bEnd = end_i
            except:
                print(E.FUNCDEF, line)
            
        elif elem == S.FUNCCALL: #call vector
            try:
                print(g_fs)
                print(words[i+1])
                wds = lex(g_fs[words[i+1]], KWDs)
                simple_parse2(g_vars, wds)
            except:
                print(E.FUNCCALL, line)
            
        elif elem == S.CLASS: 
            #attrs = {} future
            try:
                F.bStart = i
                
                class_name = words[i+1] #subsequent changed to action for mult attribs
                attr_name = words[i+3] #search_symbol 
                attr_val = words[i+5] 
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
                try:
                    x = g_cls[class_name]
                except:
                    print('wrong class name berry')
                action_name = words[i+2]
                raw_text = g_cls[class_name]['actions'][action_name]
                wds = lex( raw_text, KWDs)
                simple_parse2(g_vars, wds)
            except:
                print(E.CLASSACT, line)
            
        elif elem == S.SEE:
            try:
                attr = words[i+1]
                class_name = words[i+3]
                print(g_cls[class_name]['attributes'][attr])
            except:
                print(E.CLASSATT, line)
            
        else:
            if i < F.bStart or i > F.bEnd :
                simple_parse(g_vars, i, elem, words)  
                
        
    printd(g_vars)
    printd(g_fs)
    printd(g_cls)

# python greenBerry_REPL.py













