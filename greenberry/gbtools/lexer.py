class Token:
    def __init__(self, value, type, status, line):
        self.value = value
        self.type = type
        self.status = status
        self.line = line

class Lexeme:
    def __init__(self, value, line):
        self.value = value
        self.line = line

class Lexer:
    global ops
    def __init__(self, source, KWDs):
        #parameters
        self.source = source #text-file or string
        self.KWDs = KWDs

        #data containers
        self.cup = ''
        self.lexemes = []
        self.tokens = []

        #info
        self.line = 1
        self.status = ''


    def get_lexemes(self):
        for i, elem in enumerate(self.source):
            if elem == S.NL:
                self.line += 1
            if elem != S.WS:
                self.cup += elem
            if i+1 >= len(self.source) or self.source[i+1] == S.WS or \
                         self.source[i+1] in self.KWDs or elem in self.KWDs:
                if self.cup != S.E:
                    self.lexemes.append(Lexeme(self.cup, self.line))
                    self.cup = S.E
        return self.lexemes

    def get_tokens(self, lexemes):
        for lexeme in lexemes:
            type = ''
            status = ''
            isStringOn = 0
            isIfOn = 0

            if lexeme.value in MATH_OPS:
                type = 'math operator'
            elif lexeme.value in BOOL_OPS:
                type = 'bool operator'
            elif lexeme.value in BOOLS:
                type = 'bool value'
            elif lexeme.value == S.STRING:
                isStringOn = 1
                type = 'string'
            elif lexeme.value == S.EQUAL:
                if isIfOn == 1:
                    type = 'equalto comparison'
                else:
                    type = 'assignment operator'
            elif lexeme.value in EOS: # newline
                isStringOn = 0
                isIfOn = 0

            if isStringOn == 1:
                type = 'string'
                self.tokens.append(Token(lexeme.value, type, status, lexeme.line))

        return self.tokens
