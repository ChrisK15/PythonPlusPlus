import sys
from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.code_generator.code_generator import CodeGenerator

def compile_file(input_path: str):
    with open(input_path, "r") as file:
        source_code = file.read()
    # print(f"Source Code: {source_code}")

    # Create Lexer and tokenize
    lexer = Lexer(source_code)
    tokens = lexer.tokenize()

    # Create Parser and parse tokens
    parser = Parser(tokens)
    ast = parser.parse_program()

    # Create Code Generator and generate JavaScript code
    code_generator = CodeGenerator()
    output_js_code = code_generator.visit(ast)

    print(output_js_code)

def main():
    if len(sys.argv) < 2:
        print("Usage: ppp <input.pp>")
        return
    input_file = sys.argv[1]
    print(f"Compiling: {input_file}")
    compile_file(input_file)