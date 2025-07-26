import pytest

from src.lexer.lexer import Lexer
from src.parser.ast_nodes import *
from src.parser.parser import Parser


def init_lexer(text_input: str):
    lexer = Lexer(text_input)
    return lexer.tokenize()


def nodes_equal(test_input: Node, test_output: Node):
    # Early exit for invalid input
    if type(test_input) != type(test_output):
        return False
    if isinstance(test_input, IntegerNode):
        assert isinstance(test_output, IntegerNode)
        if test_input.value != test_output.value:
            return False
    elif isinstance(test_input, IdentifierNode):
        assert isinstance(test_output, IdentifierNode)
        if test_input.value != test_output.value:
            return False
    elif isinstance(test_input, BinaryOpNode):
        assert isinstance(test_output, BinaryOpNode)
        if test_input.op != test_output.op or not nodes_equal(test_input.left_child, test_output.left_child) or not nodes_equal(test_input.right_child, test_output.right_child):
            return False
    return True


def test_simple_addition():
    tokens = init_lexer("2 + 3")
    parser = Parser(tokens)
    node = parser.parse_addition()

    assert isinstance(node, BinaryOpNode)
    assert node.op == "+"
    assert isinstance(node.left_child, IntegerNode)
    assert node.left_child.value == 2
    assert isinstance(node.right_child, IntegerNode)
    assert node.right_child.value == 3
