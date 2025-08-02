import pytest

from src.lexer.lexer import Lexer
from src.lexer.token import TokenType
from src.parser.ast_nodes import *
from src.parser.parser import Parser, ParserException, ParserParenthesisException


def init_parser(text_input: str):
    lexer = Lexer(text_input)
    tokens = lexer.tokenize()
    parser = Parser(tokens)

    for token in tokens:
        print(token)

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
        return test_input.value == test_output.value
    elif isinstance(test_input, IdentifierNode):
        return test_input.value == test_output.value
    elif isinstance(test_input, BooleanNode):
        return test_input.value == test_output.value
    elif isinstance(test_input, BinaryOpNode):
        return (
            test_input.op == test_output.op
            and nodes_equal(test_input.left_child, test_output.left_child)
            and nodes_equal(test_input.right_child, test_output.right_child)
        )
    elif isinstance(test_input, PrintNode):
        return nodes_equal(test_input.inner_expression, test_output.inner_expression)
    elif isinstance(test_input, ThisNode):
        return True  # ThisNode has no attributes to compare
    elif isinstance(test_input, NewNode):
        if test_input.class_name != test_output.class_name:
            return False
        if len(test_input.arguments) != len(test_output.arguments):
            return False
        for arg1, arg2 in zip(test_input.arguments, test_output.arguments):
            if not nodes_equal(arg1, arg2):
                return False
        return True
    elif isinstance(test_input, CallNode):
        if test_input.method_name != test_output.method_name:
            return False
        if not nodes_equal(test_input.obj_node, test_output.obj_node):
            return False
        if len(test_input.arguments) != len(test_output.arguments):
            return False
        for arg1, arg2 in zip(test_input.arguments, test_output.arguments):
            if not nodes_equal(arg1, arg2):
                return False
        return True
    else:
        # Unknown node type - this should not happen
        raise ValueError(f"Unknown node type: {type(test_input)}")


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

def test_this_node():
    node = init_parser("this")

    assert nodes_equal(node, ThisNode())


def test_new_class_node():
    node = init_parser("new Cat()")

    assert nodes_equal(node, NewNode("Cat", []))


def test_new_class_node_with_arguments():
    node = init_parser("new Dog(5, true)")

    assert nodes_equal(node, NewNode("Dog", [IntegerNode(5), BooleanNode(True)]))

def test_new_class_node_exception_with_no_parens():
    with pytest.raises(ParserParenthesisException):
        init_parser("new Dog")


def test_call_exp():
    node = init_parser("dog.bark()")

    assert nodes_equal(node, CallNode(IdentifierNode("dog"), "bark", []))

def test_call_with_args():
    node = init_parser("dog.bark(3)")

    assert nodes_equal(node, CallNode(IdentifierNode("dog"), "bark", [IntegerNode(3)]))