import pytest

from src.lexer.lexer import Lexer, TokenizerExceptions
from src.lexer.token import TokenType


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


# Single character operators
def test_arithmetic_operators():
    tokens = init_lexer("+ - * /")
    assert len(tokens) == 5
    assert tokens[0].type == TokenType.PLUS
    assert tokens[0].value == '+'
    assert tokens[1].type == TokenType.MINUS
    assert tokens[1].value == '-'
    assert tokens[2].type == TokenType.MULTIPLY
    assert tokens[2].value == '*'
    assert tokens[3].type == TokenType.DIVIDE
    assert tokens[3].value == '/'
    assert tokens[4].type == TokenType.EOF


def test_punctuation():
    tokens = init_lexer("( ) { } ; , .")
    assert len(tokens) == 8
    assert tokens[0].type == TokenType.LEFT_PAREN
    assert tokens[0].value == '('
    assert tokens[1].type == TokenType.RIGHT_PAREN
    assert tokens[1].value == ')'
    assert tokens[2].type == TokenType.LEFT_BRACE
    assert tokens[2].value == '{'
    assert tokens[3].type == TokenType.RIGHT_BRACE
    assert tokens[3].value == '}'
    assert tokens[4].type == TokenType.SEMICOLON
    assert tokens[4].value == ';'
    assert tokens[5].type == TokenType.COMMA
    assert tokens[5].value == ','
    assert tokens[6].type == TokenType.DOT
    assert tokens[6].value == '.'
    assert tokens[7].type == TokenType.EOF


def test_assign_vs_equal():
    tokens = init_lexer("= ==")
    assert len(tokens) == 3
    assert tokens[0].type == TokenType.ASSIGN
    assert tokens[0].value == '='
    assert tokens[1].type == TokenType.EQUAL
    assert tokens[1].value == '=='
    assert tokens[2].type == TokenType.EOF


def test_comparison_operators():
    tokens = init_lexer("< <= > >= != ==")
    assert len(tokens) == 7
    assert tokens[0].type == TokenType.LESS_THAN
    assert tokens[0].value == '<'
    assert tokens[1].type == TokenType.LESS_EQUAL
    assert tokens[1].value == '<='
    assert tokens[2].type == TokenType.GREATER_THAN
    assert tokens[2].value == '>'
    assert tokens[3].type == TokenType.GREATER_EQUAL
    assert tokens[3].value == '>='
    assert tokens[4].type == TokenType.NOT_EQUAL
    assert tokens[4].value == '!='
    assert tokens[5].type == TokenType.EQUAL
    assert tokens[5].value == '=='
    assert tokens[6].type == TokenType.EOF


def test_arithmetic_expression():
    tokens = init_lexer("x + 5 * y")
    assert len(tokens) == 6
    assert tokens[0].type == TokenType.IDENTIFIER
    assert tokens[0].value == "x"
    assert tokens[1].type == TokenType.PLUS
    assert tokens[2].type == TokenType.INTEGER
    assert tokens[2].value == 5
    assert tokens[3].type == TokenType.MULTIPLY
    assert tokens[4].type == TokenType.IDENTIFIER
    assert tokens[4].value == "y"
    assert tokens[5].type == TokenType.EOF


def test_method_call_syntax():
    tokens = init_lexer("obj.method(42, true)")
    assert len(tokens) == 9
    assert tokens[0].type == TokenType.IDENTIFIER
    assert tokens[0].value == "obj"
    assert tokens[1].type == TokenType.DOT
    assert tokens[2].type == TokenType.IDENTIFIER
    assert tokens[2].value == "method"
    assert tokens[3].type == TokenType.LEFT_PAREN
    assert tokens[4].type == TokenType.INTEGER
    assert tokens[4].value == 42
    assert tokens[5].type == TokenType.COMMA
    assert tokens[6].type == TokenType.BOOLEAN
    assert tokens[6].value == True
    assert tokens[7].type == TokenType.RIGHT_PAREN
    assert tokens[8].type == TokenType.EOF


def test_complex_class_inheritance_program():
    program = """class Animal {
    init() {}
    def void speak() { return println(0); }
}

class Cat extends Animal {
    init() { super(); }
    def void speak() { return println(1); }
}

class Dog extends Animal {
    init() { super(); }
    def void speak() { return println(2); }
}

Animal cat;
Animal dog;
cat = New Cat();
dog = new Dog();
cat.speak();
dog.speak();"""

    tokens = init_lexer(program)

    token_types = [token.type for token in tokens]
    token_values = [token.value for token in tokens if token.value is not None]

    assert TokenType.CLASS in token_types
    assert TokenType.EXTENDS in token_types
    assert TokenType.INIT in token_types
    assert TokenType.DEF in token_types
    assert TokenType.VOID in token_types
    assert TokenType.RETURN in token_types
    assert TokenType.SUPER in token_types
    assert TokenType.NEW in token_types

    assert "Animal" in token_values
    assert "Cat" in token_values
    assert "Dog" in token_values
    assert "speak" in token_values
    assert "println" in token_values
    assert "cat" in token_values
    assert "dog" in token_values

    assert 0 in token_values
    assert 1 in token_values
    assert 2 in token_values

    assert TokenType.LEFT_BRACE in token_types
    assert TokenType.RIGHT_BRACE in token_types
    assert TokenType.LEFT_PAREN in token_types
    assert TokenType.RIGHT_PAREN in token_types
    assert TokenType.SEMICOLON in token_types
    assert TokenType.DOT in token_types
    assert TokenType.ASSIGN in token_types

    assert tokens[-1].type == TokenType.EOF


def test_invalid_input():
    with pytest.raises(TokenizerExceptions):
        tokens = init_lexer("$")
