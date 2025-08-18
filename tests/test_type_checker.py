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
