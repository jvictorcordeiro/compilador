class Lexer:
    def __init__(self, token, lexer, line):
        self.token = token
        self.lexer = lexer
        self.line = line

    def print(self):
        print(f"Token: {self.token}\nLexer: {self.lexer}\nLine: {self.line}")
