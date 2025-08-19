import pytest

from src.type_checker.typechecker import Typechecker, IllTypeError
from src.lexer.lexer import Lexer
from src.parser.parser import Parser

def test_integer():
    lexer = Lexer("5")
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse_primary()
    typechecker = Typechecker()
    result = typechecker.visit(ast)

    expected = "int"
    assert result == expected

def test_boolean():
    lexer = Lexer("true")
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse_primary()
    typechecker = Typechecker()
    result = typechecker.visit(ast)

    expected = "bool"
    assert result == expected

def test_bin_op_arithmetic():
    lexer = Lexer("3 + 8")
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse_addition()
    typechecker = Typechecker()
    result = typechecker.visit(ast)

    expected = "int"
    assert result == expected

def test_bin_op_arithmetic_error():
    lexer = Lexer("3 + true")
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse_addition()
    typechecker = Typechecker()

    with pytest.raises(IllTypeError):
        typechecker.visit(ast)

def test_bin_op_equality_integers():
    lexer = Lexer("3 == 8")
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse_equality()
    typechecker = Typechecker()
    result = typechecker.visit(ast)

    expected = "int"
    assert result == expected

def test_bin_op_equality_bools():
    lexer = Lexer("true == false")
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse_equality()
    typechecker = Typechecker()
    result = typechecker.visit(ast)

    expected = "bool"
    assert result == expected

def test_bin_op_equality_error():
    lexer = Lexer("true == 8")
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse_equality()
    typechecker = Typechecker()

    with pytest.raises(IllTypeError):
        typechecker.visit(ast)

def test_var_dec_int():
    lexer = Lexer("int x = 3;")
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse_statement()
    typechecker = Typechecker()
    typechecker.visit(ast)

    assert "x" in typechecker.symbol_table
    assert typechecker.symbol_table["x"] == "int"

def test_var_dec_bool():
    lexer = Lexer("bool res = true;")
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse_statement()
    typechecker = Typechecker()
    typechecker.visit(ast)

    assert "res" in typechecker.symbol_table
    assert typechecker.symbol_table["res"] == "bool"

def test_var_dec_incompatible_type_error():
    lexer = Lexer("int x = true;")
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse_statement()
    typechecker = Typechecker()

    with pytest.raises(IllTypeError):
        typechecker.visit(ast)

def test_print_node():
    lexer = Lexer("println(0)")
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse_primary()
    typechecker = Typechecker()
    result = typechecker.visit(ast)

    expected = "void"
    assert result == expected

def test_exp_statement():
    lexer = Lexer("8 + 9;")
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse_statement()
    typechecker = Typechecker()
    result = typechecker.visit(ast)

    assert result is None # Checking if we don't crash

def test_exp_statement_undefined_assignment():
    lexer = Lexer("x + 9;")
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse_statement()
    typechecker = Typechecker()
    with pytest.raises(IllTypeError):
        typechecker.visit(ast)

def test_return():
    lexer = Lexer("return(8);")
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse_statement()
    typechecker = Typechecker()
    result = typechecker.visit(ast)

    assert result is None  # Checking if we don't crash

def test_empty_return():
    lexer = Lexer("return;")
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse_statement()
    typechecker = Typechecker()
    result = typechecker.visit(ast)

    assert result is None  # Checking if we don't crash

def test_if_no_else():
    lexer = Lexer("if(true == true) return(7);")
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse_statement()
    typechecker = Typechecker()
    result = typechecker.visit(ast)

    assert result is None # Checking if we don't crash

def test_if_with_else():
    lexer = Lexer("if(true == true) return(7); else return(36);")
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse_statement()
    typechecker = Typechecker()
    result = typechecker.visit(ast)

    assert result is None  # Checking if we don't crash

def test_while():
    lexer = Lexer("while(true) return(0);")
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse_statement()
    typechecker = Typechecker()
    result = typechecker.visit(ast)

    assert result is None  # Checking if we don't crash

def test_block():
    lexer = Lexer("{int x = 0; int y = 1; int z = 2;}")
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse_statement()
    typechecker = Typechecker()
    result = typechecker.visit(ast)

    assert result is None  # Checking if we don't crash