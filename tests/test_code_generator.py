from src.code_generator.code_generator import CodeGenerator
from src.lexer.lexer import Lexer
from src.parser.parser import Parser


def init_code_generator(text_input: str):
    lexer = Lexer(text_input)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse_program()
    code_generator = CodeGenerator()
    result = code_generator.visit(ast)

    return result

def test_integer():
    # TEMPORARY #
    lexer = Lexer("5")
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse_primary()
    code_generator = CodeGenerator()
    result = code_generator.visit(ast)
    ##############

    expected = "5"
    assert result == expected

def test_boolean():
    # TEMPORARY #
    lexer = Lexer("true")
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse_primary()
    code_generator = CodeGenerator()
    result = code_generator.visit(ast)
    ##############

    expected = "true"
    assert result == expected

def test_binary_op():
    # TEMPORARY #
    lexer = Lexer("x + 5")
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse_addition()
    code_generator = CodeGenerator()
    result = code_generator.visit(ast)
    ##############

    expected = "x + 5"
    assert result == expected

def test_print():
    # TEMPORARY #
    lexer = Lexer("println(x)")
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse_primary()
    code_generator = CodeGenerator()
    result = code_generator.visit(ast)
    ##############

    expected = "console.log(x)"
    assert result == expected

def test_this():
    # TEMPORARY #
    lexer = Lexer("this")
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse_primary()
    code_generator = CodeGenerator()
    result = code_generator.visit(ast)
    ##############

    expected = "this"
    assert result == expected

def test_new():
    # TEMPORARY #
    lexer = Lexer("new Cat(7)")
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse_primary()
    code_generator = CodeGenerator()
    result = code_generator.visit(ast)
    ##############

    expected = "new Cat(7)"
    assert result == expected

def test_call_exp():
    # TEMPORARY #
    lexer = Lexer("cat.meow(0)")
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse_call()
    code_generator = CodeGenerator()
    result = code_generator.visit(ast)
    ##############

    expected = "cat.meow(0)"
    assert result == expected

def test_exp_statements():
    # TEMPORARY #
    lexer = Lexer("x + 5;")
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse_statement()
    code_generator = CodeGenerator()
    result = code_generator.visit(ast)
    ##############

    expected = "x + 5;"
    assert result == expected

def test_vardec_statement():
    # TEMPORARY #
    lexer = Lexer("int y = x + 5;")
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse_statement()
    code_generator = CodeGenerator()
    result = code_generator.visit(ast)
    ##############

    expected = "int y = x + 5"
    assert result == expected