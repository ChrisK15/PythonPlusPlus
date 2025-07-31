import pytest

from src.lexer.lexer import Lexer
from src.lexer.token import TokenType
from src.parser.ast_nodes import *
from src.parser.parser import Parser, ParserException, ParserParenthesisException


def init_parser(text_input: str):
    lexer = Lexer(text_input)
    tokens = lexer.tokenize()
    parser = Parser(tokens)

    result = parser.parse_assignment()

    # Makes sure we are at the EOF token
    if parser.current_token.type != TokenType.EOF:
        raise ParserException(
            f"Error! Did not find an EOF Token after the input. Current Token: {parser.current_token}"
        )

    return result


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
        if (
            test_input.op != test_output.op
            or not nodes_equal(test_input.left_child, test_output.left_child)
            or not nodes_equal(test_input.right_child, test_output.right_child)
        ):
            return False
    return True


def test_simple_addition():
    node = init_parser("2 + 3")

    assert nodes_equal(node, BinaryOpNode("+", IntegerNode(2), IntegerNode(3)))


def test_parenthesis():
    node = init_parser("1 + (2 + 3)")

    assert nodes_equal(
        node,
        BinaryOpNode(
            "+", IntegerNode(1), BinaryOpNode("+", IntegerNode(2), IntegerNode(3))
        ),
    )


def test_invalid_parenthesis():
    with pytest.raises(ParserParenthesisException):
        init_parser("1 + (2 + 3")


def test_multiplication():
    node = init_parser("1 / 2 * 3")

    assert nodes_equal(
        node,
        BinaryOpNode(
            "*", BinaryOpNode("/", IntegerNode(1), IntegerNode(2)), IntegerNode(3)
        ),
    )


def test_addition_and_multiplication():
    node = init_parser("1 + 2 * 3")

    assert nodes_equal(
        node,
        BinaryOpNode(
            "+", IntegerNode(1), BinaryOpNode("*", IntegerNode(2), IntegerNode(3))
        ),
    )


def test_addition_and_multiplication_with_parens():
    node = init_parser("(1 + 2) * 3")

    assert nodes_equal(
        node,
        BinaryOpNode(
            "*", BinaryOpNode("+", IntegerNode(1), IntegerNode(2)), IntegerNode(3)
        ),
    )


def test_assignment():
    node = init_parser("x = 10")

    assert nodes_equal(node, BinaryOpNode("=", IdentifierNode("x"), IntegerNode(10)))


def test_boolean():
    node = init_parser("true")

    assert nodes_equal(node, BooleanNode(True))


def test_comparison():
    node = init_parser("x == 10")

    assert nodes_equal(node, BinaryOpNode("==", IdentifierNode("x"), IntegerNode(10)))


def test_invalid_input():
    with pytest.raises(ParserException):
        init_parser("1 * *")


def test_print():
    node = init_parser("println(x)")

    assert nodes_equal(node, PrintNode(IdentifierNode("x")))


def test_print_exception_no_parens():
    with pytest.raises(ParserParenthesisException):
        init_parser("println")


def test_print_exception_no_close_parens():
    with pytest.raises(ParserParenthesisException):
        init_parser("println(x")


def test_print_with_binary_op_expression():
    node = init_parser("println(2 + 3)")

    assert nodes_equal(
        node, PrintNode(BinaryOpNode("+", IntegerNode(2), IntegerNode(3)))
    )


def test_print_with_binary_op_and_parens():
    node = init_parser("println((1 + 2) * 3)")

    assert nodes_equal(
        node,
        PrintNode(
            BinaryOpNode(
                "*", BinaryOpNode("+", IntegerNode(1), IntegerNode(2)), IntegerNode(3)
            )
        ),
    )
