import re

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value
    def __repr__(self):
        return f"Token({self.type}, {self.value})"
class Lexer:
    def __init__(self, source):
        self.source = source
        self.position = 0
    def get_next_token(self):
         
        if self.position >= len(self.source):
            return None
        while self.position < len(self.source) and self.source[self.position].isspace():
            self.position += 1
        if self.position >= len(self.source):
            return None
        if self.source[self.position:self.position + 2] == "//":
            while self.position < len(self.source) and self.source[self.position] != '\n':
                self.position += 1
            return self.get_next_token()
        if self.position >= len(self.source):
            return None
        if self.source[self.position].isdigit():
            number = ""
            while self.position < len(self.source) and self.source[self.position].isdigit():
                number += self.source[self.position]
                self.position += 1
            return Token("NUMBER", int(number))
        if self.source[self.position].isalpha() or self.source[self.position] == '_':
            identifier = ""
            while self.position < len(self.source) and (self.source[self.position].isalnum() or self.source[self.position] == '_'):
                identifier += self.source[self.position]
                self.position += 1

            if identifier == "print":
                return Token("PRINT", identifier)

            elif identifier == "if":
                return Token("IF", identifier)
            elif identifier == "else":
                return Token("ELSE", identifier)
            elif identifier == "def":
                return Token("DEF", identifier)
            elif identifier == "while":
                return Token("WHILE", identifier)
            elif identifier == "return":
                return Token("RETURN", identifier)
            return Token("IDENTIFIER", identifier)
        if self.source[self.position] == '+':
            self.position += 1
            return Token("ADD", "+")
        elif self.source[self.position] == '-':
            self.position += 1
            return Token("SUB", "-")
        elif self.source[self.position] == '*':
            self.position += 1
            return Token("MUL", "*")
        elif self.source[self.position] == '/':
            self.position += 1
            return Token("DIV", "/")
        if self.source[self.position] == '=':
            if self.position + 1 < len(self.source) and self.source[self.position + 1] == '=':
                self.position += 2
                return Token("EQ", "==")
            else:
                self.position += 1
                return Token("ASSIGN", "=")

        elif self.source[self.position] == ';':
            self.position += 1
            return Token("SEMICOLON", ";")
        elif self.source[self.position] == '"':
            self.position += 1
            return Token("DOUBLE QUOTES", "")
        elif self.source[self.position] == ':':
            self.position += 1
            return Token("COLON", ":")
        elif self.source[self.position] == '(':
            self.position += 1
            return Token("LPAREN", "(")
        elif self.source[self.position] == ')':
            self.position += 1
            return Token("RPAREN", ")")
        elif self.source[self.position] == '{':
            self.position += 1
            return Token("LBRACE", "{")
        elif self.source[self.position] == '}':
            self.position += 1
            return Token("RBRACE", "}")
        elif self.source[self.position] == '[':
            self.position += 1
            return Token("LBRACKET", "[")
        elif self.source[self.position] == ']':
            self.position += 1
            return Token("RBRACKET", "]")
        elif self.source[self.position] == ':':
            self.position += 1
            return Token("COLON", ":")
        elif self.source[self.position] == ',':
            self.position += 1
            return Token("COMMA", ",")
        # Add these to your get_next_token method
        elif self.source[self.position] == '@':
            self.position += 1
            return Token("AT", "@")
        elif self.source[self.position] == '#':
            self.position += 1
            return Token("HASH", "#")
        elif self.source[self.position] == '$':
            self.position += 1
            return Token("DOLLAR", "$")
        elif self.source[self.position] == '%':
            self.position += 1
            return Token("MOD", "%")
        elif self.source[self.position] == '^':
            self.position += 1
            return Token("POW", "^")
        elif self.source[self.position] == '&':
            self.position += 1
            return Token("AMPERSAND", "&")
        elif self.source[self.position] == '|':
            self.position += 1
            return Token("OR", "|")
        elif self.source[self.position] == '<':
            self.position += 1
            return Token("LT", "<")
        elif self.source[self.position] == '>':
            self.position += 1
            return Token("GT", ">")
        elif self.source[self.position] == '?':
            self.position += 1
            return Token("QUESTION", "?")
        elif self.source[self.position] == '\\':
            self.position += 1
            return Token("BACKSLASH", "\\")
        elif self.source[self.position] == '!':
            self.position += 1
            return Token("NEQ", "!")

        

       
    
    
def tokenize(source_code):
    lexer = Lexer(source_code)
    tokens = []
    while True:
        token = lexer.get_next_token()
        if token is None:
            break
        tokens.append(token)
    return tokens

    
