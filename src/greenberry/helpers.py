import contextlib
from io import StringIO

from greenberry.gb import greenberry_eval


def eval(str):
    """
    Function to evaluate postfix expression
    """

    exp = list(str)
    S = []
    i = 0
    while i < len(exp):
        if exp[i].isnumeric():
            S.append(exp[i])
        else:
            y = int(S[-1])
            S.pop()
            x = int(S[-1])
            S.pop()
            if exp[i] == "+":
                S.append(x + y)
            elif exp[i] == "-":
                S.append(x - y)
            elif exp[i] == "*":
                S.append(x * y)
            elif exp[i] == "/":
                S.append(x // y)
            elif exp[i] == "^":
                S.append(x**y)
            else:
                pass
        i = i + 1
    print(S[0])


def maths_eval(string):  # previous InfixCon
    """
    Converts Infix expression to postfix
    Enter the expression to evaluate but mind the brackets in case of multiply and divide
    """
    res = ""
    exp = string
    exp = list(exp)
    S = []
    L = []
    i = 0
    while i < len(exp):
        if exp[i] >= "0" and exp[i] <= "9":
            res = res + exp[i]

        else:
            if len(S) == 0 or exp[i] == "(" or exp[i] == "^":
                S.append(exp[i])
            elif exp[i] == ")":
                while S[-1] != "(":
                    res = res + S[-1]
                    S.pop()
                S.pop()
            elif exp[i] == "*" or exp[i] == "/":
                if S[-1] == "^":
                    while len(S) > 0 and S[-1] != "(":
                        res = res + S[-1]
                        S.pop()
                    S.append(exp[i])
                elif S[-1] == "*" or S[-1] == "/":
                    while len(S) > 0 and S[-1] != "(" and S[-1] != "^":
                        res = res + S[-1]
                        S.pop()
                    S.append(exp[i])
                else:
                    S.append(exp[i])
            elif exp[i] == "+" or exp[i] == "-":
                if S[-1] == "^" or S[-1] == "*" or S[-1] == "/":
                    while len(S) > 0 and S[-1] != "(":
                        res = res + S[-1]
                        S.pop()
                    S.append(exp[i])
                elif S[-1] == "+" or S[-1] == "-":
                    while (
                        len(S) > 0
                        and S[-1] != "("
                        and S[-1] != "^"
                        and S[-1] != "*"
                        and S[-1] != "/"
                    ):
                        res = res + S[-1]
                        S.pop()
                    S.append(exp[i])
                else:
                    S.append(exp[i])
        i = i + 1
    while len(S) > 0:
        res = res + S[-1]
        S.pop()
    eval(res)


def capture_print(func, *args, **kwargs):
    temp_stdout = StringIO()
    # Redirect stdout to catch the print statements from the provided function
    with contextlib.redirect_stdout(temp_stdout):
        func(*args, **kwargs)
    output = temp_stdout.getvalue().strip()
    return output