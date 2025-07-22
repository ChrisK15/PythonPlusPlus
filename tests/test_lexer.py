from src.lexer.token import Token, TokenType
from src.lexer.lexer import Lexer

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