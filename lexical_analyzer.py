from lexer import Lexer
from expressions import Expression, ExpressionFunction

class LexicalAnalyzer:
    def __init__(self, text):
        self.text = text
        self.tokens = []
        self.simbols_table = {}

    def analyze(self, text):
        buffer = ""
        now_line = 1
        for line in text:
            for i in range(len(line)):
                if i + 1 < len(line):
                    buffer += line[i]
                    if self.verify_delimiters(buffer, now_line):
                        buffer = ""
                        continue
                    elif line[i + 1] in [" ", "\n", "{", "}", "(", ")", ";", ","]:
                        buffer = buffer.strip()
                        self.verify_reserved_simbols(buffer, now_line, line, i)
                        buffer = ""
            buffer = ""
            now_line += 1
        self.tokens.append(Lexer("<fim_arquivo>", "EOF", now_line + 1))

        # for token in self.tokens:
        #     print(f"Token: {token.token}, Lexema: {token.lexer}, Linha: {token.line}")


    def verify_delimiters(self, buffer, line):
        delimiters = {
            " ": None,
            "{": "<abre_chaves>",
            "}": "<fecha_chaves>",
            "(": "<abre_parenteses>",
            ")": "<fecha_parenteses>",
            ";": "<fim_comando>",
            ",": "<virgula>",
            ":": "<dois_pontos>"
        }
        if buffer in delimiters:
            if delimiters[buffer]:
                self.tokens.append(Lexer(delimiters[buffer], buffer, line))
            return True
        return False

    def verify_reserved_simbols(self, buffer, line, text, i):
        reserved = {
            "program": "<programa>",
            "int": "<tipo>",
            "bool": "<tipo>",
            "procedure": "<declaracao_procedimento>",
            "function": "<declaracao_funcao>",
            "return": "<retorno>",
            "if": "<se>",
            "else": "<senao>",
            "while": "<laco>",
            "break": "<pare>",
            "continue": "<continue>",
            "print": "<imprime>",
            "true": "<operador_booleano>",
            "false": "<operador_booleano>"
        }
        operators = {
            "+": "<operador_aritmetico>",
            "-": "<operador_aritmetico>",
            "*": "<operador_aritmetico>",
            "/": "<operador_aritmetico>",
            "==": "<operador_relacional>",
            "!=": "<operador_relacional>",
            "<": "<operador_relacional>",
            "<=": "<operador_relacional>",
            ">": "<operador_relacional>",
            ">=": "<operador_relacional>",
            "=": "<atribuicao>"
        }

        if buffer in reserved:
            self.tokens.append(Lexer(reserved[buffer], buffer, line))
            return True
        elif buffer in operators:
            self.tokens.append(Lexer(operators[buffer], buffer, line))
            return True
        else:
            self.variables(buffer, line, text, i)

    def variables(self, buffer, line, text, i):
        if buffer.isidentifier():
            if buffer not in self.simbols_table:
                self.simbols_table[buffer] = Expression("variavel", line)
            self.tokens.append(Lexer("<variavel>", buffer, line))
        elif buffer.isdigit():
            self.tokens.append(Lexer("<numero>", buffer, line))
        else:
            print(f"Erro léxico: Identificador inválido '{buffer}' na linha {line}")
            quit()


    def print_simbols_table(self):
        print("Tabela de símbolos:")
        for key, value in self.simbols_table.items():
            print(f"{key}: {value.type} (linha {value.line})")
