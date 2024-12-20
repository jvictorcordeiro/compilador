from lexer import Lexer

class SintaticalAnalyzer:
    def __init__(self, token_list, symbol_table):
        self.token_list = token_list
        self.symbol_table = symbol_table
        self.look_ahead = 0

    def start(self):
        print("Início da Análise Sintática")
        self.program()
        print("Fim da Análise Sintática")

    def match(self, expected_token):
        if self.token_list[self.look_ahead].token == expected_token:
            self.look_ahead += 1
        else:
            self.error(f"Esperado: {expected_token}, encontrado: {self.token_list[self.look_ahead].token}")

    def error(self, message):
        print(f"Erro de Sintaxe: {message} na linha {self.token_list[self.look_ahead].line}")
        exit()

    
    def program(self):
        self.match("<programa>")  
        self.match("<variavel>") 
        self.match("<abre_chaves>")  
        self.block()
        self.match("<fecha_chaves>") 
        if self.token_list[self.look_ahead].token == "<fim_arquivo>":
            self.match("<fim_arquivo>") 
        else:
            self.error(f"Esperado: <fim_arquivo>, encontrado: {self.token_list[self.look_ahead].token}")

    
    def block(self):
        while self.token_list[self.look_ahead].token != "<fecha_chaves>" and self.look_ahead < len(self.token_list):
            current_token = self.token_list[self.look_ahead]
            if current_token.token == "<tipo>":
                self.variable_declaration()
            elif current_token.token == "<declaracao_funcao>":
                self.function_declaration()
            elif current_token.token == "<declaracao_procedimento>":
                self.procedure_declaration()
            elif current_token.token == "<retorno>":
                self.return_command()
            else:
                self.command()


    def function_declaration(self):
        self.match("<declaracao_funcao>")
        self.match("<variavel>") 
        self.match("<abre_parenteses>")
        if self.token_list[self.look_ahead].token == "<tipo>":
            self.parameter_list()
        self.match("<fecha_parenteses>")
        self.match("<abre_chaves>")
        self.block() 
        self.match("<fecha_chaves>") 

    def procedure_declaration(self):

        self.match("<declaracao_procedimento>")
        self.match("<variavel>") 
        self.match("<abre_parenteses>")
        if self.token_list[self.look_ahead].token == "<tipo>": 
            self.parameter_list()
        self.match("<fecha_parenteses>")
        self.match("<abre_chaves>")
        self.block()
        self.match("<fecha_chaves>")
    
    def parameter_list(self):
        self.match("<tipo>")
        self.match("<variavel>")
        while self.token_list[self.look_ahead].token == "<virgula>":
            self.match("<virgula>")
            self.match("<tipo>")
            self.match("<variavel>")


    def variable_declaration(self):
        self.match("<tipo>") 
        self.match("<variavel>")  
        while self.token_list[self.look_ahead].token == "<virgula>":
            self.match("<virgula>")
            self.match("<variavel>")
        self.match("<fim_comando>") 


    def command(self):
        current_token = self.token_list[self.look_ahead]

        if current_token.token == "<variavel>":
            self.assignment()
        elif current_token.token == "<imprime>":
            self.print_command()
        elif current_token.token == "<se>":
            self.conditional()
        elif current_token.token == "<laco>":
            self.loop()
        elif current_token.token == "<retorno>":
            self.return_command()
        elif current_token.token == "<pare>" or current_token.token == "<continue>":
            self.break_continue()
        else:
            self.error(f"Comando inesperado: {current_token.token}")



    def assignment(self):
        self.match("<variavel>") 
        self.match("<atribuicao>") 
        if self.token_list[self.look_ahead].token == "<variavel>":
            if self.token_list[self.look_ahead + 1].token == "<abre_parenteses>":
                self.function_call()
            else:
                self.expression()
        else:
            self.expression() 
        self.match("<fim_comando>")


    def print_command(self):
        self.match("<imprime>")
        self.match("<abre_parenteses>")
        self.expression()
        self.match("<fecha_parenteses>")
        self.match("<fim_comando>")

    def conditional(self):
        self.match("<se>")
        self.match("<abre_parenteses>")
        self.expression()
        self.match("<fecha_parenteses>")
        self.match("<abre_chaves>")
        self.block()
        self.match("<fecha_chaves>")
        if self.token_list[self.look_ahead].token == "<senao>":
            self.match("<senao>")
            self.match("<abre_chaves>")
            self.block()
            self.match("<fecha_chaves>")

    def loop(self):
        self.match("<laco>")
        self.match("<abre_parenteses>")
        self.expression()
        self.match("<fecha_parenteses>")
        self.match("<abre_chaves>")
        self.block()
        self.match("<fecha_chaves>")

    def return_command(self):

        self.match("<retorno>") 
        self.expression() 
        self.match("<fim_comando>")


    def break_continue(self):
        if self.token_list[self.look_ahead].token == "<pare>":
            self.match("<pare>")
        elif self.token_list[self.look_ahead].token == "<continue>":
            self.match("<continue>")
        self.match("<fim_comando>")

    def expression(self):
        self.simple_expression()
        if self.token_list[self.look_ahead].token in ["<operador_relacional>"]:
            self.match("<operador_relacional>")
            self.simple_expression()

    def simple_expression(self):
        if self.token_list[self.look_ahead].token in ["<operador_aritmetico>"]:
            self.match("<operador_aritmetico>")
        self.term()
        while self.token_list[self.look_ahead].token in ["<operador_aritmetico>"]:
            self.match("<operador_aritmetico>")
            self.term()

    def term(self):
        self.factor()
        while self.token_list[self.look_ahead].token in ["<operador_aritmetico>"]:
            self.match("<operador_aritmetico>")
            self.factor()

    def factor(self):
        current_token = self.token_list[self.look_ahead]
        if current_token.token == "<variavel>":
            self.match("<variavel>")
            if self.token_list[self.look_ahead].token == "<abre_parenteses>":
                self.function_call() 
        elif current_token.token == "<numero>":
            self.match("<numero>")
        elif current_token.token == "<abre_parenteses>":
            self.match("<abre_parenteses>")
            self.expression()
            self.match("<fecha_parenteses>")
        elif current_token.token in ["<operador_booleano>"]:
            self.match("<operador_booleano>")
        else:
            self.error(f"Fator inválido: {current_token.token}")

    def function_call(self):
        self.match("<variavel>")
        self.match("<abre_parenteses>")
        if self.token_list[self.look_ahead].token not in ["<fecha_parenteses>"]:
            self.expression()
            while self.token_list[self.look_ahead].token == "<virgula>":
                self.match("<virgula>")
                self.expression()
        self.match("<fecha_parenteses>")
