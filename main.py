import os
import traceback
from flask import Flask, request, jsonify, render_template
from compiler.lexer import tokenize
from compiler.parser import Parser
from compiler.codegen import CodeGenerator
from compiler.interpreter import run_full_interpreter 

from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/compile', methods=['POST'])
def compile_code():
    try:
        code = request.form.get('code', '')
        print("Received code:", repr(code))

        if not code.strip():
            return jsonify({'error': 'No code provided'}), 400

        tokens = tokenize(code)
        parser_instance = Parser(tokens)
        ast = parser_instance.parse()

        codegen = CodeGenerator(ast)
        instructions = codegen.generate()
        functions = codegen.functions
        output = run_full_interpreter(instructions,functions , debug=True)
        
        


        return jsonify({
            'lexer_output': '\n'.join(str(token) for token in tokens),
            'parser_output': str(ast),
            'codegen_output': '\n'.join(' '.join(map(str, instr)) for instr in instructions),
            'final_output' :output
        })

    except Exception as e:
        print("Compilation error:", str(e))  # Log the error
        traceback.print_exc()
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_DEBUG', 'True') == 'True'
    app.run(debug=debug_mode)
