from io import StringIO
from greenBerry import greenBerry_eval
import contextlib

def eval(str):         #Function to evaluate postfix expression
    exp=list(str)
    S=[]
    i=0
    while(i<len(exp)):
        if(exp[i].isnumeric()):
            S.append(exp[i])
        else:
            y=int(S[-1])
            S.pop()
            x=int(S[-1])
            S.pop()
            if(exp[i]=='+'):
                S.append(x+y)
            elif(exp[i]=='-'):
                S.append(x-y)
            elif(exp[i]=='*'):
                S.append(x*y)
            elif(exp[i]=='/'):
                S.append(x//y)
            elif(exp[i]=='^'):
                S.append(x**y)
            else:
                pass
        i=i+1
    print(S[0])

def maths_eval(string): # previous InfixCon
    res=''                                                              #Converting Infix expression to postfix
    exp=string                                                          #Enter the expression to evaluate but mind the brackets in case
    exp=list(exp)                                                       #Multiply and divide
    S=[]
    L=[]
    i=0
    while(i<len(exp)):
        if(exp[i]>='0' and exp[i]<='9'):
            res=res+exp[i]

        else:
            if(len(S)==0 or exp[i]=='(' or exp[i]=='^'):
                S.append(exp[i])
            elif(exp[i]==')'):
                while(S[-1]!='('):
                    res=res+S[-1]
                    S.pop()
                S.pop()
            elif(exp[i]=='*' or exp[i]=='/'):
                if(S[-1]=='^'):
                    while(len(S)>0 and S[-1]!='('):
                        res=res+S[-1]
                        S.pop()
                    S.append(exp[i])
                elif(S[-1]=='*' or S[-1]=='/'):
                    while(len(S)>0 and S[-1]!='('  and S[-1]!='^'):
                        res=res+S[-1]
                        S.pop()
                    S.append(exp[i])
                else:
                    S.append(exp[i])
            elif(exp[i]=='+' or exp[i]=='-'):
                if(S[-1]=='^' or S[-1]=='*' or S[-1]=='/'):
                    while(len(S)>0 and S[-1]!='('):
                        res=res+S[-1]
                        S.pop()
                    S.append(exp[i])
                elif(S[-1]=='+' or S[-1]=='-'):
                    while(len(S)>0 and S[-1]!='('  and S[-1]!='^' and S[-1]!='*' and S[-1]!='/'):
                        res=res+S[-1]
                        S.pop()
                    S.append(exp[i])
                else:
                    S.append(exp[i])
        i=i+1
    while(len(S)>0):
        res=res+S[-1]
        S.pop()
    eval(res)


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
