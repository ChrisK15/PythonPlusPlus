from src.lexer.lexer import Lexer
from src.lexer.token import Token, TokenType


def test_empty_input():
    lexer = Lexer("")
    tokens = lexer.tokenize()

    assert len(tokens) == 1
    assert tokens[0].type == TokenType.EOF


def test_single_integer():
    lexer = Lexer("8")
    tokens = lexer.tokenize()

    assert len(tokens) == 2
    assert tokens[0].type == TokenType.INTEGER
    assert tokens[0].value == 8
    assert tokens[1].type == TokenType.EOF


def test_multiple_digit_integer():
    lexer = Lexer("42")
    tokens = lexer.tokenize()

    assert len(tokens) == 2
    assert tokens[0].type == TokenType.INTEGER
    assert tokens[0].value == 42
    assert tokens[1].type == TokenType.EOF
