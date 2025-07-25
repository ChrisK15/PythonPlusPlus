import pytest

from src.lexer.lexer import Lexer
from src.parser.ast_nodes import *
from src.parser.parser import Parser


def init_lexer(text_input: str):
    lexer = Lexer(text_input)
    return lexer.tokenize()

def test_simple_addition():
    tokens = init_lexer("2 + 3")
    parser = Parser(tokens)
    node = parser.parse_addition()

    assert isinstance(node, BinaryOpNode)
    assert node.op == '+'
    assert isinstance(node.left_child, IntegerNode)
    assert node.left_child.value == 2
    assert isinstance(node.right_child, IntegerNode)
    assert node.right_child.value == 3

