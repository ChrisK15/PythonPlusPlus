from src.lexer.lexer import Lexer
from src.lexer.token import Token, TokenType


def init_lexer(text_input: str):
    lexer = Lexer(text_input)
    return lexer.tokenize()


def test_empty_input():
    tokens = init_lexer("")

    assert len(tokens) == 1
    assert tokens[0].type == TokenType.EOF


def test_single_integer():
    tokens = init_lexer("8")

    assert len(tokens) == 2
    assert tokens[0].type == TokenType.INTEGER
    assert tokens[0].value == 8
    assert tokens[1].type == TokenType.EOF


def test_multiple_digit_integer():
    tokens = init_lexer("42")

    assert len(tokens) == 2
    assert tokens[0].type == TokenType.INTEGER
    assert tokens[0].value == 42
    assert tokens[1].type == TokenType.EOF


def test_whitespace():
    tokens = init_lexer("   ")

    assert len(tokens) == 1
    assert tokens[0].type == TokenType.EOF


def test_whitespace_with_input():
    tokens = init_lexer("  42  ")

    assert len(tokens) == 2
    assert tokens[0].type == TokenType.INTEGER
    assert tokens[0].value == 42
    assert tokens[1].type == TokenType.EOF


def test_whitespace_with_multiple_inputs():
    tokens = init_lexer("  42  73   ")

    assert len(tokens) == 3
    assert tokens[0].type == TokenType.INTEGER
    assert tokens[0].value == 42
    assert tokens[1].type == TokenType.INTEGER
    assert tokens[1].value == 73
    assert tokens[2].type == TokenType.EOF


def test_boolean_true():
    tokens = init_lexer("true")
    assert len(tokens) == 2
    assert tokens[0].type == TokenType.BOOLEAN
    assert tokens[0].value == True
    assert tokens[1].type == TokenType.EOF


def test_boolean_false():
    tokens = init_lexer("false")
    assert len(tokens) == 2
    assert tokens[0].type == TokenType.BOOLEAN
    assert tokens[0].value == False
    assert tokens[1].type == TokenType.EOF


def test_identifier():
    tokens = init_lexer("X Y z")
    assert len(tokens) == 4
    assert tokens[0].type == TokenType.IDENTIFIER
    assert tokens[0].value == "X"
    assert tokens[1].type == TokenType.IDENTIFIER
    assert tokens[1].value == "Y"
    assert tokens[2].type == TokenType.IDENTIFIER
    assert tokens[2].value == "z"
    assert tokens[3].type == TokenType.EOF


def test_keyword_class():
    tokens = init_lexer("class")
    assert len(tokens) == 2
    assert tokens[0].type == TokenType.CLASS
    assert tokens[0].value is None
    assert tokens[1].type == TokenType.EOF


def test_keyword_def():
    tokens = init_lexer("def")
    assert len(tokens) == 2
    assert tokens[0].type == TokenType.DEF
    assert tokens[0].value is None
    assert tokens[1].type == TokenType.EOF


def test_keyword_init():
    tokens = init_lexer("init")
    assert len(tokens) == 2
    assert tokens[0].type == TokenType.INIT
    assert tokens[0].value is None
    assert tokens[1].type == TokenType.EOF


def test_keyword_if():
    tokens = init_lexer("if")
    assert len(tokens) == 2
    assert tokens[0].type == TokenType.IF
    assert tokens[0].value is None
    assert tokens[1].type == TokenType.EOF


def test_keyword_while():
    tokens = init_lexer("while")
    assert len(tokens) == 2
    assert tokens[0].type == TokenType.WHILE
    assert tokens[0].value is None
    assert tokens[1].type == TokenType.EOF


def test_mixed_keywords_and_identifiers():
    tokens = init_lexer("class MyClass def myMethod")
    assert len(tokens) == 5
    assert tokens[0].type == TokenType.CLASS
    assert tokens[1].type == TokenType.IDENTIFIER
    assert tokens[1].value == "MyClass"
    assert tokens[2].type == TokenType.DEF
    assert tokens[3].type == TokenType.IDENTIFIER
    assert tokens[3].value == "myMethod"
    assert tokens[4].type == TokenType.EOF
