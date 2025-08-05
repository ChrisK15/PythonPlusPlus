import pytest

from src.lexer.lexer import Lexer
from src.lexer.token import TokenType
from src.parser.ast_nodes import *
from src.parser.parser import Parser, ParserException, ParserParenthesisException


def init_parser(text_input: str):
    lexer = Lexer(text_input)
    tokens = lexer.tokenize()
    parser = Parser(tokens)

    result = parser.parse_statement()

    # Break Glass in case of Emergency
    # print ("TOKENS PRODUCED BY LEXER:")
    # print("-------------------------")
    # for token in tokens:
    #     print(f"{token.type}, Value: {token.value}")
    # print("\nPARSER OUTPUT:")
    # print("--------------")
    # if isinstance(result, IfStatement):
    #     print(f"EXP: {result.exp}, THEN: {result.then_stmt}, ELSE: {result.else_stmt}")

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

    # Expressions
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

    # Statements
    elif isinstance(test_input, ExpressionStatement):
        return nodes_equal(test_input.exp, test_output.exp)
    elif isinstance(test_input, VarDecStatement):
        return test_input.type == test_output.type and test_input.var == test_output.var
    elif isinstance(test_input, AssignmentStatement):
        return test_input.var == test_output.var and nodes_equal(
            test_input.exp, test_output.exp
        )
    elif isinstance(test_input, WhileStatement):
        return nodes_equal(test_input.exp, test_output.exp) and nodes_equal(test_input.stmt, test_output.stmt)
    elif isinstance(test_input, BreakStatement):
        return True
    elif isinstance(test_input, ReturnStatement):
        return nodes_equal(test_input.exp, test_output.exp)
    elif isinstance(test_input, IfStatement):
        if test_input.else_stmt is None and test_output.else_stmt is None:
            return nodes_equal(test_input.exp, test_output.exp) and nodes_equal(test_input.then_stmt,test_output.then_stmt)
        elif test_input.else_stmt is None or test_output.else_stmt is None:
            return False
        else:
            return nodes_equal(test_input.exp, test_output.exp) and nodes_equal(test_input.then_stmt, test_output.then_stmt) and nodes_equal(test_input.else_stmt, test_output.else_stmt)
    elif isinstance(test_input, BlockStatement):
        if len(test_input.stmts) == len(test_output.stmts):
            for input_stmt, output_stmt in zip(test_input.stmts, test_output.stmts):
                if not nodes_equal(input_stmt, output_stmt):
                    return False
            return True
        return False

    else:
        # Unknown node type - this should not happen
        raise ValueError(f"Unknown node type: {type(test_input)}")


def test_simple_addition():
    node = init_parser("2 + 3;")

    assert nodes_equal(
        node, ExpressionStatement(BinaryOpNode("+", IntegerNode(2), IntegerNode(3)))
    )


def test_parenthesis():
    node = init_parser("1 + (2 + 3);")

    assert nodes_equal(
        node,
        ExpressionStatement(
            BinaryOpNode(
                "+", IntegerNode(1), BinaryOpNode("+", IntegerNode(2), IntegerNode(3))
            )
        ),
    )


def test_invalid_parenthesis():
    with pytest.raises(ParserParenthesisException):
        init_parser("1 + (2 + 3;")


def test_multiplication():
    node = init_parser("1 / 2 * 3;")

    assert nodes_equal(
        node,
        ExpressionStatement(
            BinaryOpNode(
                "*", BinaryOpNode("/", IntegerNode(1), IntegerNode(2)), IntegerNode(3)
            )
        ),
    )


def test_addition_and_multiplication():
    node = init_parser("1 + 2 * 3;")

    assert nodes_equal(
        node,
        ExpressionStatement(
            BinaryOpNode(
                "+", IntegerNode(1), BinaryOpNode("*", IntegerNode(2), IntegerNode(3))
            )
        ),
    )


def test_addition_and_multiplication_with_parens():
    node = init_parser("(1 + 2) * 3;")

    assert nodes_equal(
        node,
        ExpressionStatement(
            BinaryOpNode(
                "*", BinaryOpNode("+", IntegerNode(1), IntegerNode(2)), IntegerNode(3)
            )
        ),
    )


def test_assignment():
    node = init_parser("x = 10;")

    assert nodes_equal(node, AssignmentStatement("x", IntegerNode(10)))


def test_boolean():
    node = init_parser("true;")

    assert nodes_equal(node, ExpressionStatement(BooleanNode(True)))


def test_comparison():
    node = init_parser("x == 10;")

    assert nodes_equal(
        node,
        ExpressionStatement(BinaryOpNode("==", IdentifierNode("x"), IntegerNode(10))),
    )


def test_invalid_input():
    with pytest.raises(ParserException):
        init_parser("1 * *;")


def test_print():
    node = init_parser("println(x);")

    assert nodes_equal(node, ExpressionStatement(PrintNode(IdentifierNode("x"))))


def test_print_exception_no_parens():
    with pytest.raises(ParserParenthesisException):
        init_parser("println;")


def test_print_exception_no_close_parens():
    with pytest.raises(ParserParenthesisException):
        init_parser("println(x;")


def test_print_with_binary_op_expression():
    node = init_parser("println(2 + 3);")

    assert nodes_equal(
        node,
        ExpressionStatement(
            PrintNode(BinaryOpNode("+", IntegerNode(2), IntegerNode(3)))
        ),
    )


def test_print_with_binary_op_and_parens():
    node = init_parser("println((1 + 2) * 3);")

    assert nodes_equal(
        node,
        ExpressionStatement(
            PrintNode(
                BinaryOpNode(
                    "*",
                    BinaryOpNode("+", IntegerNode(1), IntegerNode(2)),
                    IntegerNode(3),
                )
            )
        ),
    )


def test_this_node():
    node = init_parser("this;")

    assert nodes_equal(node, ExpressionStatement(ThisNode()))


def test_new_class_node():
    node = init_parser("new Cat();")

    assert nodes_equal(node, ExpressionStatement(NewNode("Cat", [])))


def test_new_class_node_with_arguments():
    node = init_parser("new Dog(5, true);")

    assert nodes_equal(
        node, ExpressionStatement(NewNode("Dog", [IntegerNode(5), BooleanNode(True)]))
    )


def test_new_class_node_exception_with_no_parens():
    with pytest.raises(ParserParenthesisException):
        init_parser("new Dog;")


def test_call_exp():
    node = init_parser("dog.bark();")

    assert nodes_equal(
        node, ExpressionStatement(CallNode(IdentifierNode("dog"), "bark", []))
    )


def test_call_with_args():
    node = init_parser("dog.bark(3);")

    assert nodes_equal(
        node,
        ExpressionStatement(CallNode(IdentifierNode("dog"), "bark", [IntegerNode(3)])),
    )


def test_var_dec_int():
    node = init_parser("int x;")

    assert nodes_equal(node, VarDecStatement("int", "x"))


def test_var_dec_bool():
    node = init_parser("bool x;")

    assert nodes_equal(node, VarDecStatement("bool", "x"))


def test_if_without_else():
    node = init_parser("if (x == 5) x = 10;")
    
    expected = IfStatement(
        BinaryOpNode("==", IdentifierNode("x"), IntegerNode(5)),
        AssignmentStatement("x", IntegerNode(10))
    )
    assert nodes_equal(node, expected)


def test_if_with_else():
    node = init_parser("if (x == 5) x = 10; else x = 20;")
    
    expected = IfStatement(
        BinaryOpNode("==", IdentifierNode("x"), IntegerNode(5)),
        AssignmentStatement("x", IntegerNode(10)),
        AssignmentStatement("x", IntegerNode(20))
    )
    assert nodes_equal(node, expected)


def test_if_with_boolean_condition():
    node = init_parser("if (true) println(x);")
    
    expected = IfStatement(
        BooleanNode(True),
        ExpressionStatement(PrintNode(IdentifierNode("x")))
    )
    assert nodes_equal(node, expected)


def test_while_statement():
    node = init_parser("while (x < 10) x = x + 1;")
    
    expected = WhileStatement(
        BinaryOpNode("<", IdentifierNode("x"), IntegerNode(10)),
        AssignmentStatement("x", BinaryOpNode("+", IdentifierNode("x"), IntegerNode(1)))
    )
    assert nodes_equal(node, expected)


def test_while_with_expression_statement():
    node = init_parser("while (true) println(x);")
    
    expected = WhileStatement(
        BooleanNode(True),
        ExpressionStatement(PrintNode(IdentifierNode("x")))
    )
    assert nodes_equal(node, expected)


def test_return_with_expression():
    node = init_parser("return x + 5;")
    
    expected = ReturnStatement(
        BinaryOpNode("+", IdentifierNode("x"), IntegerNode(5))
    )
    assert nodes_equal(node, expected)


def test_return_with_simple_value():
    node = init_parser("return 42;")
    
    expected = ReturnStatement(IntegerNode(42))
    assert nodes_equal(node, expected)


def test_break_statement():
    node = init_parser("break;")
    
    expected = BreakStatement()
    assert nodes_equal(node, expected)

def test_empty_block_statement():
    node = init_parser("{ }")

    expected = BlockStatement([])
    assert nodes_equal(node, expected)

def test_block_statement():
    node = init_parser("{ return 7; }")

    expected = BlockStatement([ReturnStatement(IntegerNode(7))])
    assert nodes_equal(node, expected)

def test_block_statement_with_multiple_statements():
    node = init_parser("{ x + 5; y + 3; }")

    expected = BlockStatement([BinaryOpNode("+", IdentifierNode("x"), IntegerNode(5)), BinaryOpNode("+", IdentifierNode("y"), IntegerNode(3))])
    assert nodes_equal(node, expected)



