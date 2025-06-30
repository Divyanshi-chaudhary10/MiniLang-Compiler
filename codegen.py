
class CodeGenerator:
    def __init__(self, ast):
        self.ast = ast
        self.variables = {}
        self.instructions = []
        self.functions = {}
    def generate_expression(self, expr):
        print(f"Generating expression for: {expr}")
        if expr[0] == "NUMBER":
            self.instructions.append(("PUSH", expr[1]))
        elif expr[0] == "IDENTIFIER":
            self.instructions.append(("LOAD", expr[1]))
        elif expr[0] == "FUNC_CALL":
            func_name = expr[1]
            args = expr[2]

            # First evaluate all arguments
            for arg in args:
                self.generate_expression(arg)

                # Then call the function
            self.instructions.append(("CALL", func_name, len(args)))
        elif expr[0] == "BINARY_OP":
            self.generate_expression(expr[2])
            self.generate_expression(expr[3])
            op = expr[1]
            if op == "ADD":
                self.instructions.append(("ADD",))
            elif op == "SUB":
                self.instructions.append(("SUB",))
            elif op == "MUL":
                self.instructions.append(("MUL",))
            elif op == "DIV":
                self.instructions.append(("DIV",))
            elif op == "LT":  
                self.instructions.append(("LT",))
            elif op == "GT":  
                self.instructions.append(("GT",))
            elif op == "EQ":  
                self.instructions.append(("EQ",))
            elif op == "NEQ":  
                self.instructions.append(("NEQ",))
            elif op == "POW":  
                self.instructions.append(("POW",))
            elif op == "MOD":  
                self.instructions.append(("MOD",))
        


            else:
                raise Exception(f"Unknown binary operator {op}")




    def generate_statement(self, statement):
        print(f"Generating stmt: {statement}")
        if statement[0] == "ASSIGNMENT":
            self.generate_expression(statement[2])
            self.instructions.append(("STORE", statement[1]))
        
        elif statement[0] == "PRINT":
            self.generate_expression(statement[1])
            self.instructions.append(("PRINT",))
        
        elif statement[0] == "SPECIAL_CHAR":
            self.instructions.append(("SPECIAL", statement[1]))
        

        elif statement[0] == "IF":
            condition, then_branch, else_branch = statement[1], statement[2], statement[3]
            self.generate_expression(condition)
            else_label = f"ELSE_{len(self.instructions)}"
            end_label = f"END_IF_{len(self.instructions)}"
            self.instructions.append(("JUMP_IF_FALSE", else_label))
            for stmt in then_branch:
                self.generate_statement(stmt)
            self.instructions.append(("JUMP", end_label))
            self.instructions.append(("LABEL", else_label))
            if else_branch:
                for stmt in else_branch:
                    self.generate_statement(stmt)
            self.instructions.append(("LABEL", end_label))
        
        
        elif statement[0] == "WHILE":
            condition, body = statement[1], statement[2]
            start_label = f"START_WHILE_{len(self.instructions)}"
            end_label = f"END_WHILE_{len(self.instructions)}"
            self.instructions.append(("LABEL", start_label))
            self.generate_expression(condition)
            self.instructions.append(("JUMP_IF_FALSE", end_label))
            for stmt in body:
                self.generate_statement(stmt)
            self.instructions.append(("JUMP", start_label))
            self.instructions.append(("LABEL", end_label))
        
        elif statement[0] == "RETURN":
            self.generate_expression(statement[1])
            self.instructions.append(("RETURN",))


        elif statement[0] == "DEF":
            func_name = statement[1]
            params = statement[2]
            # Safely access the body block statements
            body = statement[3]
            if isinstance(body, tuple) and len(body) > 1:
                body_stmts = body[1]
            else:
                body_stmts = body  # maybe already a list

            # Compile function body in a separate instruction list
            prev_instructions = self.instructions
            self.instructions = []

            for stmt in body_stmts:
                self.generate_statement(stmt)

            self.functions[func_name] = {
                "params": params,
                "body": self.instructions.copy()
            }

            self.instructions = prev_instructions

        else:
            self.generate_expression(statement)
    
    
    def generate(self):
        for statement in self.ast:
            self.generate_statement(statement)
        return self.instructions
    
