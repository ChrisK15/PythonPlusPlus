import sys
from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.code_generator.code_generator import CodeGenerator

def main():
    if len(sys.argv) < 2:
        print("Usage: ppp <input.pp>")
        return
    input_file = sys.argv[1]
    print(f"Compiling: {input_file}")