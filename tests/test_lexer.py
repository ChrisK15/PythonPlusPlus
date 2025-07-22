from src.lexer.token import Token, TokenType
from src.lexer.lexer import Lexer

def test_empty_input():
    lexer = Lexer("")
    tokens = lexer.tokenize()

    assert len(tokens) == 1
    assert tokens[0].type == TokenType.EOF