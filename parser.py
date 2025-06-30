class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def peek(self):
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return None
    
    


    def consume(self, expected_type):
        token = self.peek()
        if token is None:
            raise Exception(f"Unexpected end of input, expected {expected_type} at position {self.position}")
        if token.type == expected_type:
            self.position += 1
            return token
        raise Exception(f"Expected {expected_type}, but got {token.type} at position {self.position}")

    def parse_expression(self):
        if self.peek() is None:
            raise Exception(f"Unexpected end of input at position {self.position}")
        left = self.parse_arithmetic_expression()
        while self.peek() and self.peek().type in ("GT", "LT", "GE", "LE", "EQ", "NEQ"):
            op = self.consume(self.peek().type)
            right = self.parse_arithmetic_expression()
            left = ("BINARY_OP", op.type, left, right)
        return left

    def parse_arithmetic_expression(self):
        if self.peek() is None:
            raise Exception(f"Unexpected end of input at position {self.position}")
        term = self.parse_term()
        while self.peek() and self.peek().type in ("ADD", "SUB"):
            op = self.consume(self.peek().type)
            next_term = self.parse_term()
            term = ("BINARY_OP", op.type, term, next_term)
        return term

    def parse_term(self):
        if self.peek() is None:
            raise Exception(f"Unexpected end of input at position {self.position}")
        factor = self.parse_factor()
        while self.peek() and self.peek().type in ("MUL", "DIV"):
            op = self.consume(self.peek().type)
            next_factor = self.parse_factor()
            factor = ("BINARY_OP", op.type, factor, next_factor)
        return factor

    def parse_factor(self):
        token = self.peek()
        if token is None:
            raise Exception(f"Unexpected end of input at position {self.position}")
        special_token = {
            "AT", "HASH", "DOLLAR", "MOD", "POW", "AMPERSAND", "OR",
            "LT", "GT", "QUESTION", "BACKSLASH", "NEQ" , "EQ" , "MUL"
        }
        if token.type == "NUMBER":
            return ("NUMBER", self.consume("NUMBER").value)
        
        elif token.type == "IDENTIFIER":
            identifier = self.consume("IDENTIFIER").value
            # Check if it's a function call
            if self.peek() and self.peek().type == "LPAREN":
                self.consume("LPAREN")
                args = []
                if self.peek() and self.peek().type != "RPAREN":
                    args.append(self.parse_expression())
                    while self.peek() and self.peek().type == "COMMA":
                        self.consume("COMMA")
                        args.append(self.parse_expression())
                self.consume("RPAREN")
                return ("FUNC_CALL", identifier, args)
            return ("IDENTIFIER", identifier)

        elif token.type == "LPAREN":
            self.consume("LPAREN")
            expr = self.parse_expression()
            self.consume("RPAREN")
            return expr
        elif token.type == "LBRACE":
            self.consume("LBRACE")
            expr = self.parse_expression()
            self.consume("RBRACE")
            return expr
        elif token.type in special_token:
            token = self.consume(token.type)
            return ("SPECIAL_CHAR", token.value)
        else:
            raise Exception(f"Invalid factor at token {token}")

    def parse_block(self):
        if self.peek() is None:
            raise Exception(f"Unexpected end of input at position {self.position}")
        statements = []
        self.consume("LBRACE")
        while self.peek() and self.peek().type != "RBRACE":
            statements.append(self.parse_statement())
        if self.peek() is None:
            raise Exception(f"Expected RBRACE but found end of input at position {self.position}")
        self.consume("RBRACE")
        return statements

    def parse_statement(self):
        token = self.peek()
        if token is None:
            raise Exception(f"Unexpected end of input at position {self.position}")
        
        if token.type == "IDENTIFIER":
            identifier = self.consume("IDENTIFIER").value
            next_token = self.peek()

            if next_token and next_token.type == "ASSIGN":
                self.consume("ASSIGN")
                expression = self.parse_expression()
                self.consume("SEMICOLON")
                return ("ASSIGNMENT", identifier, expression)


            elif next_token and next_token.type == "LPAREN":
                # Parse function call
                self.consume("LPAREN")
                args = []
                if self.peek() and self.peek().type != "RPAREN":
                    args.append(self.parse_expression())
                    while self.peek() and self.peek().type == "COMMA":
                        self.consume("COMMA")
                        args.append(self.parse_expression())
                self.consume("RPAREN")
                self.consume("SEMICOLON")
                return ("FUNC_CALL", identifier, args)

            
            else:
                raise Exception(f"Unexpected token {next_token} after identifier at position {self.position}")


        elif token.type == "PRINT":
            self.consume("PRINT")
            self.consume("LPAREN")
            expression = self.parse_expression()
            self.consume("RPAREN")
            self.consume("SEMICOLON")
            return ("PRINT", expression)
        elif token.type == "IF":
            self.consume("IF")
            self.consume("LPAREN")
            condition = self.parse_expression()
            self.consume("RPAREN")
            then_branch = self.parse_block()
            else_branch = None
            if self.peek() and self.peek().type == "ELSE":
                self.consume("ELSE")
                else_branch = self.parse_block()
            return ("IF", condition, then_branch, else_branch)
        elif token.type == "WHILE":
            self.consume("WHILE")
            self.consume("LPAREN")
            condition = self.parse_expression()
            self.consume("RPAREN")
            body = self.parse_block()
            return ("WHILE", condition, body)
        elif token.type == "DEF":
            self.consume("DEF")
            func_name = self.consume("IDENTIFIER").value
            self.consume("LPAREN")
            params = []
            if self.peek() and self.peek().type != "RPAREN":
                params.append(self.consume("IDENTIFIER").value)
                while self.peek() and self.peek().type == "COMMA":
                    self.consume("COMMA")
                    params.append(self.consume("IDENTIFIER").value)
            self.consume("RPAREN")
            body = self.parse_block()
            return ("DEF", func_name, params, body)
        elif token.type == "RETURN":
            self.consume("RETURN")
            expression = self.parse_expression()
            self.consume("SEMICOLON")
            return ("RETURN", expression)
        elif token.type in (
            "AT", "HASH", "DOLLAR", "MOD", "POW", "AMPERSAND", "OR",
            "LT", "GT", "QUESTION", "BACKSLASH", "NEQ" , "MUL"
        ):
            return self.parse_special_char()
        else:
            # Fallback: try parsing as an expression statement
            expr = self.parse_expression()
            if self.peek() and self.peek().type == "SEMICOLON":
                self.consume("SEMICOLON")
            return expr
        


    def parse_special_char(self):
        # Example: just consume the special char and return it
        token = self.peek()
        if token is None:
            raise Exception(f"Unexpected end of input at position {self.position}")
        special_token_types = {
            "AT", "HASH", "DOLLAR", "MOD", "POW", "AMPERSAND", "OR",
            "LT", "GT", "QUESTION", "BACKSLASH", "NEQ" , "MUL"
        }
        if token.type in special_token_types:
            return ("SPECIAL_CHAR", self.consume(token.type).value)
        else:
            raise Exception(f"Expected special character, got {token.type}")

    def parse(self):
        statements = []
        while self.peek():
            try:
                statements.append(self.parse_statement())
            except Exception as e:
                token = self.peek()
                line_info = getattr(token, "line", "unknown") if token else "EOF"
                raise Exception(f"Parse error at position {self.position} (token: {token}, line: {line_info}): {e}")
        return statements

