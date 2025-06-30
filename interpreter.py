def run_full_interpreter(instructions, functions, debug=False):
    variables = {}
    stack = []
    output_lines = []
    instruction_pointer = 0
    call_stack = []  # stack of (instructions, instruction_pointer, variables)

    # Map labels in current instructions
    def map_labels(instrs):
        lbls = {}
        for idx, instr in enumerate(instrs):
            if instr[0] == "LABEL" and len(instr) > 1:
                lbls[instr[1]] = idx
        return lbls

    labels = map_labels(instructions)

    current_instructions = instructions

    while True:
        if instruction_pointer >= len(current_instructions):
            # If call stack empty, end execution
            if not call_stack:
                break
            # Otherwise return from function (shouldn't happen normally)
            current_instructions, instruction_pointer, variables = call_stack.pop()
            continue

        instruction = current_instructions[instruction_pointer]
        op = instruction[0]

        if op == "PUSH":
            stack.append(instruction[1])

        elif op == "LOAD":
            stack.append(variables.get(instruction[1], 0))

        elif op == "STORE":
            if stack:
                variables[instruction[1]] = stack.pop()

        elif op == "ADD":
            b = stack.pop()
            a = stack.pop()
            stack.append(a + b)

        elif op == "SUB":
            b = stack.pop()
            a = stack.pop()
            stack.append(a - b)

        elif op == "MUL":
            b = stack.pop()
            a = stack.pop()
            stack.append(a * b)

        elif op == "DIV":
            b = stack.pop()
            a = stack.pop()
            stack.append(a // b if b != 0 else 0)

        elif op == "MOD":
            b = stack.pop()
            a = stack.pop()
            stack.append(a % b if b != 0 else 0)

        elif op == "POW":
            exponent = stack.pop()
            base = stack.pop()
            stack.append(base ** exponent)

        elif op == "GT":
            b = stack.pop()
            a = stack.pop()
            stack.append(1 if a > b else 0)

        elif op == "LT":
            b = stack.pop()
            a = stack.pop()
            stack.append(1 if a < b else 0)

        elif op == "EQ":
            b = stack.pop()
            a = stack.pop()
            stack.append(1 if a == b else 0)

        elif op == "NEQ":
            b = stack.pop()
            a = stack.pop()
            stack.append(1 if a != b else 0)

        elif op == "PRINT":
            if stack:
                output_lines.append(str(stack[-1]))

        elif op == "JUMP":
            label = instruction[1]
            if label in labels:
                instruction_pointer = labels[label]
                continue

        elif op == "JUMP_IF_FALSE":
            condition = stack.pop()
            if condition == 0:
                label = instruction[1]
                if label in labels:
                    instruction_pointer = labels[label]
                    continue

        elif op == "LABEL":
            pass

        elif op == "CALL":
            func_name = instruction[1]
            arg_count = instruction[2]
            if func_name not in functions:
                raise Exception(f"Undefined function {func_name}")

            # Pop arguments in reverse order
            args = [stack.pop() for _ in range(arg_count)][::-1]

            # Save current execution context
            call_stack.append((current_instructions, instruction_pointer + 1, variables.copy()))

            # Setup new function context
            func_info = functions[func_name]
            current_instructions = func_info["body"]
            instruction_pointer = 0
            variables = {}

            # Map parameters to arguments
            for param, arg in zip(func_info["params"], args):
                variables[param] = arg

            # Remap labels for new instructions
            labels = map_labels(current_instructions)

            continue  # immediately execute next instruction

        elif op == "RETURN":
            ret_val = stack.pop() if stack else None
            if not call_stack:
                # No caller, program end
                return "\n".join(output_lines).strip()
            # Restore previous context
            current_instructions, instruction_pointer, variables = call_stack.pop()
            labels = map_labels(current_instructions)
            if ret_val is not None:
                stack.append(ret_val)
            continue

        instruction_pointer += 1

    return "\n".join(output_lines).strip()
