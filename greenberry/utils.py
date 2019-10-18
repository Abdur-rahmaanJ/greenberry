from io import StringIO
from greenBerry import greenBerry_eval
import contextlib

def eval(list):
    '''Function to evaluate postfix expression'''

    exp=list
    S=[]
    for e in exp:
        if e.isnumeric():
            S.append(e)
        else:
            y=int(S.pop())
            
            x=int(S.pop())
            
            if(e=='+'):
                S.append(x+y)
            elif(e=='-'):
                S.append(x-y)
            elif(e=='*'):
                S.append(x*y)
            elif(e=='/'):
                S.append(x//y)
            elif(e=='^'):
                S.append(x**y)
            else:
                pass

    print(S[0])

def maths_eval(string): # previous InfixCon

    ''' Takes a string of infix expression and
        returns the solution'''

    operators = '^/*+-'                                     # operator precedence
    infix_exp = string                                      # the infix input expression 
    pfix_exp  = []                                          # the postfix output expression
    term = ''                                               # multidigit numbers which will be added in the postfix expression
    S = []                                                  # stack to hold operators
    
    for e in infix_exp:

        if e.isnumeric():
            term += e

        else:
            pfix_exp.append(term)
            term = ''

            if e == '(':
                S.append(e)

            elif e == ')':
                while S[-1] != '(':
                    pfix_exp.append(S.pop())
                S.pop()

            elif e in operators:
                while S and not operators.index(e) < operators.index(S[-1]):
                    pfix_exp.append(S.pop())
                S.append(e)

    pfix_exp.append(term)
    while S:
        pfix_exp.append(S.pop())
    
    eval(pfix_exp)
    


def capture_gb_eval_print(code):
    temp_stdout = StringIO()
    # redirect stdout to catch print statement from eval function
    with contextlib.redirect_stdout(temp_stdout):
        greenBerry_eval(code)
    output = temp_stdout.getvalue().strip()
    return output

def capture_maths_eval_print(code):
    temp_stdout = StringIO()
    # redirect stdout to catch print statement from eval function
    with contextlib.redirect_stdout(temp_stdout):
        maths_eval(code)
    output = temp_stdout.getvalue().strip()
    return output
