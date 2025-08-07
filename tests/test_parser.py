import pytest

from src.lexer.lexer import Lexer
from src.lexer.token import TokenType
from src.parser.ast_nodes import *
from src.parser.parser import Parser, ParserException, ParserParenthesisException


def init_parser(text_input: str):
    lexer = Lexer(text_input)
    tokens = lexer.tokenize()
    parser = Parser(tokens)

    result = parser.parse_program()

    # Break Glass in case of Emergency
    # print ("TOKENS PRODUCED BY LEXER:")
    # print("-------------------------")
    # for token in tokens:
    #     print(f"{token.type}, Value: {token.value}")
    # print("\nPARSER OUTPUT:")
    # print("--------------")
    # if isinstance(result, VarDecStatement):
    #     print(f"TYPE: {result.var_type}, VAR: {result.var}, VAL: {result.val.value}")

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
        assert isinstance(test_output, IntegerNode)
        return test_input.value == test_output.value
    elif isinstance(test_input, IdentifierNode):
        assert isinstance(test_output, IdentifierNode)
        return test_input.value == test_output.value
    elif isinstance(test_input, BooleanNode):
        assert isinstance(test_output, BooleanNode)
        return test_input.value == test_output.value
    elif isinstance(test_input, BinaryOpNode):
        assert isinstance(test_output, BinaryOpNode)
        return (
            test_input.op == test_output.op
            and nodes_equal(test_input.left_child, test_output.left_child)
            and nodes_equal(test_input.right_child, test_output.right_child)
        )
    elif isinstance(test_input, PrintNode):
        assert isinstance(test_output, PrintNode)
        return nodes_equal(test_input.inner_expression, test_output.inner_expression)
    elif isinstance(test_input, ThisNode):
        return True  # ThisNode has no attributes to compare
    elif isinstance(test_input, NewNode):
        assert isinstance(test_output, NewNode)
        if test_input.class_name != test_output.class_name:
            return False
        if len(test_input.arguments) != len(test_output.arguments):
            return False
        for arg1, arg2 in zip(test_input.arguments, test_output.arguments):
            if not nodes_equal(arg1, arg2):
                return False
        return True
    elif isinstance(test_input, CallNode):
        assert isinstance(test_output, CallNode)
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
        assert isinstance(test_output, ExpressionStatement)
        return nodes_equal(test_input.exp, test_output.exp)
    elif isinstance(test_input, VarDecStatement):
        assert isinstance(test_output, VarDecStatement)
        return (
            test_input.var_type == test_output.var_type
            and test_input.var == test_output.var
            and nodes_equal(test_input.val, test_output.val)
        )
    elif isinstance(test_input, AssignmentStatement):
        assert isinstance(test_output, AssignmentStatement)
        return test_input.var == test_output.var and nodes_equal(
            test_input.exp, test_output.exp
        )
    elif isinstance(test_input, WhileStatement):
        assert isinstance(test_output, WhileStatement)
        return nodes_equal(test_input.exp, test_output.exp) and nodes_equal(
            test_input.stmt, test_output.stmt
        )
    elif isinstance(test_input, BreakStatement):
        return True
    elif isinstance(test_input, ReturnStatement):
        assert isinstance(test_output, ReturnStatement)
        if test_input.exp is None and test_output.exp is None:
            return True
        elif test_input.exp is None or test_output.exp is None:
            return False
        else:
            return nodes_equal(test_input.exp, test_output.exp)
    elif isinstance(test_input, IfStatement):
        assert isinstance(test_output, IfStatement)
        if test_input.else_stmt is None and test_output.else_stmt is None:
            return nodes_equal(test_input.exp, test_output.exp) and nodes_equal(
                test_input.then_stmt, test_output.then_stmt
            )
        elif test_input.else_stmt is None or test_output.else_stmt is None:
            return False
        else:
            return (
                nodes_equal(test_input.exp, test_output.exp)
                and nodes_equal(test_input.then_stmt, test_output.then_stmt)
                and nodes_equal(test_input.else_stmt, test_output.else_stmt)
            )
    elif isinstance(test_input, BlockStatement):
        assert isinstance(test_output, BlockStatement)
        if len(test_input.stmts) == len(test_output.stmts):
            for input_stmt, output_stmt in zip(test_input.stmts, test_output.stmts):
                if not nodes_equal(input_stmt, output_stmt):
                    return False
            return True
        return False

    # Declarations
    elif isinstance(test_input, MethodDef):
        assert isinstance(test_output, MethodDef)
        if (
            test_input.method_type != test_output.method_type
            or test_input.method_name != test_output.method_name
        ):
            return False
        if len(test_input.parameters) == len(test_output.parameters):
            for input_param, output_param in zip(
                test_input.parameters, test_output.parameters
            ):
                if input_param != output_param:
                    return False
        else:
            return False
        if len(test_input.statements) == len(test_output.statements):
            for input_statement, output_statement in zip(
                test_input.statements, test_output.statements
            ):
                if not nodes_equal(input_statement, output_statement):
                    return False
            return True
        else:
            return False
    elif isinstance(test_input, Constructor):
        assert isinstance(test_output, Constructor)
        if len(test_input.parameters) == len(test_output.parameters):
            for input_param, output_param in zip(
                test_input.parameters, test_output.parameters
            ):
                if input_param != output_param:
                    return False
        else:
            return False
        if len(test_input.statements) == len(test_output.statements):
            for input_statement, output_statement in zip(
                test_input.statements, test_output.statements
            ):
                if not nodes_equal(input_statement, output_statement):
                    return False
        if test_input.super_args is None and test_output.super_args is None:
            return True
        elif test_input.super_args is None or test_output.super_args is None:
            return False
        else:
            if len(test_input.super_args) == len(test_output.super_args):
                for input_super_arg, output_super_arg in zip(
                    test_input.super_args, test_output.super_args
                ):
                    if not nodes_equal(input_super_arg, output_super_arg):
                        return False
            else:
                return False
            return True
    elif isinstance(test_input, ClassDef):
        assert isinstance(test_output, ClassDef)
        if test_input.class_name != test_output.class_name:
            return False

        if test_input.extend_class_name is None and test_output.extend_class_name is None:
            pass
        elif test_input.extend_class_name is None or test_output.extend_class_name is None:
            return False
        elif test_input.extend_class_name != test_output.extend_class_name:
            return False

        if len(test_input.class_instance_vars) == len(test_output.class_instance_vars):
            for test_input_tuple, test_output_tuple in zip(test_input.class_instance_vars, test_output.class_instance_vars):
                if test_input_tuple != test_output_tuple:
                    return False

        else:
            return False

        if not nodes_equal(test_input.constructor, test_output.constructor):
            return False

        if len(test_input.methods) == len(test_output.methods):
            for test_input_method, test_output_method in zip(test_input.methods, test_output.methods):
                if not nodes_equal(test_input_method, test_output_method):
                    return False
        else:
            return False
        return True

    elif isinstance(test_input, ProgramNode):
        assert isinstance(test_output, ProgramNode)
        if len(test_input.class_defs) == len(test_output.class_defs):
            for test_input_classdef, test_output_classdef in zip(test_input.class_defs, test_output.class_defs):
                if not nodes_equal(test_input_classdef, test_output_classdef):
                    return False
        if len(test_input.statements) == len(test_output.statements):
            for test_input_statement, test_output_statement in zip(test_input.statements, test_output.statements):
                if not nodes_equal(test_input_statement, test_output_statement):
                    return False
        return True


    else:
        # Unknown node type - this should not happen
        raise ValueError(f"Unknown node type: {type(test_input)}")


def test_simple_addition():
    node = init_parser("2 + 3;")

    assert nodes_equal(
        node, ProgramNode([], [ExpressionStatement(BinaryOpNode("+", IntegerNode(2), IntegerNode(3)))])
    )


def test_parenthesis():
    node = init_parser("1 + (2 + 3);")

    assert nodes_equal(
        node,
        ProgramNode([], [ExpressionStatement(
            BinaryOpNode(
                "+", IntegerNode(1), BinaryOpNode("+", IntegerNode(2), IntegerNode(3))
            )
        )]),
    )


def test_invalid_parenthesis():
    with pytest.raises(ParserParenthesisException):
        init_parser("1 + (2 + 3;")


def test_multiplication():
    node = init_parser("1 / 2 * 3;")

    assert nodes_equal(
        node,
        ProgramNode([], [ExpressionStatement(
            BinaryOpNode(
                "*", BinaryOpNode("/", IntegerNode(1), IntegerNode(2)), IntegerNode(3)
            )
        )]),
    )


def test_addition_and_multiplication():
    node = init_parser("1 + 2 * 3;")

    assert nodes_equal(
        node,
        ProgramNode([], [ExpressionStatement(
            BinaryOpNode(
                "+", IntegerNode(1), BinaryOpNode("*", IntegerNode(2), IntegerNode(3))
            )
        )]),
    )


def test_addition_and_multiplication_with_parens():
    node = init_parser("(1 + 2) * 3;")

    assert nodes_equal(
        node,
        ProgramNode([], [ExpressionStatement(
            BinaryOpNode(
                "*", BinaryOpNode("+", IntegerNode(1), IntegerNode(2)), IntegerNode(3)
            )
        )]),
    )


def test_assignment():
    node = init_parser("x = 10;")

    assert nodes_equal(node, ProgramNode([], [AssignmentStatement("x", IntegerNode(10))]))


def test_boolean():
    node = init_parser("true;")

    assert nodes_equal(node, ProgramNode([], [ExpressionStatement(BooleanNode(True))]))


def test_comparison():
    node = init_parser("x == 10;")

    assert nodes_equal(
        node,
        ProgramNode([], [ExpressionStatement(BinaryOpNode("==", IdentifierNode("x"), IntegerNode(10)))]),
    )


def test_invalid_input():
    with pytest.raises(ParserException):
        init_parser("1 * *;")


def test_print():
    node = init_parser("println(x);")

    assert nodes_equal(node, ProgramNode([], [ExpressionStatement(PrintNode(IdentifierNode("x")))]))


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
        ProgramNode([], [ExpressionStatement(
            PrintNode(BinaryOpNode("+", IntegerNode(2), IntegerNode(3)))
        )]),
    )


def test_print_with_binary_op_and_parens():
    node = init_parser("println((1 + 2) * 3);")

    assert nodes_equal(
        node,
        ProgramNode([], [ExpressionStatement(
            PrintNode(
                BinaryOpNode(
                    "*",
                    BinaryOpNode("+", IntegerNode(1), IntegerNode(2)),
                    IntegerNode(3),
                )
            )
        )]),
    )


def test_this_node():
    node = init_parser("this;")

    assert nodes_equal(node, ProgramNode([], [ExpressionStatement(ThisNode())]))


def test_new_class_node():
    node = init_parser("new Cat();")

    assert nodes_equal(node, ProgramNode([], [ExpressionStatement(NewNode("Cat", []))]))


def test_new_class_node_with_arguments():
    node = init_parser("new Dog(5, true);")

    assert nodes_equal(
        node, ProgramNode([], [ExpressionStatement(NewNode("Dog", [IntegerNode(5), BooleanNode(True)]))])
    )


def test_new_class_node_exception_with_no_parens():
    with pytest.raises(ParserParenthesisException):
        init_parser("new Dog;")


def test_call_exp():
    node = init_parser("dog.bark();")

    assert nodes_equal(
        node, ProgramNode([], [ExpressionStatement(CallNode(IdentifierNode("dog"), "bark", []))])
    )


def test_call_with_args():
    node = init_parser("dog.bark(3);")

    assert nodes_equal(
        node,
        ProgramNode([], [ExpressionStatement(CallNode(IdentifierNode("dog"), "bark", [IntegerNode(3)]))]),
    )


def test_var_dec_int():
    node = init_parser("int x = 0;")

    assert nodes_equal(node, ProgramNode([], [VarDecStatement("int", "x", IntegerNode(0))]))


def test_var_dec_bool():
    node = init_parser("bool x = true;")

    assert nodes_equal(node, ProgramNode([], [VarDecStatement("bool", "x", BooleanNode(True))]))


def test_var_dec_with_complex_expression():
    node = init_parser("int x = 16 + 3;")

    expected = ProgramNode([], [VarDecStatement(
        "int", "x", BinaryOpNode("+", IntegerNode(16), IntegerNode(3))
    )])
    assert nodes_equal(node, expected)


def test_if_without_else():
    node = init_parser("if (x == 5) x = 10;")

    expected = ProgramNode([], [IfStatement(
        BinaryOpNode("==", IdentifierNode("x"), IntegerNode(5)),
        AssignmentStatement("x", IntegerNode(10)),
    )])
    assert nodes_equal(node, expected)


def test_if_with_else():
    node = init_parser("if (x == 5) x = 10; else x = 20;")

    expected = ProgramNode([], [IfStatement(
        BinaryOpNode("==", IdentifierNode("x"), IntegerNode(5)),
        AssignmentStatement("x", IntegerNode(10)),
        AssignmentStatement("x", IntegerNode(20)),
    )])
    assert nodes_equal(node, expected)


def test_if_with_boolean_condition():
    node = init_parser("if (true) println(x);")

    expected = ProgramNode([], [IfStatement(
        BooleanNode(True), ExpressionStatement(PrintNode(IdentifierNode("x")))
    )])
    assert nodes_equal(node, expected)


def test_while_statement():
    node = init_parser("while (x < 10) x = x + 1;")

    expected = ProgramNode([], [WhileStatement(
        BinaryOpNode("<", IdentifierNode("x"), IntegerNode(10)),
        AssignmentStatement(
            "x", BinaryOpNode("+", IdentifierNode("x"), IntegerNode(1))
        ),
    )])
    assert nodes_equal(node, expected)


def test_while_with_expression_statement():
    node = init_parser("while (true) println(x);")

    expected = ProgramNode([], [WhileStatement(
        BooleanNode(True), ExpressionStatement(PrintNode(IdentifierNode("x")))
    )])
    assert nodes_equal(node, expected)


def test_return_with_expression():
    node = init_parser("return x + 5;")

    expected = ProgramNode([], [ReturnStatement(BinaryOpNode("+", IdentifierNode("x"), IntegerNode(5)))])
    assert nodes_equal(node, expected)


def test_return_with_simple_value():
    node = init_parser("return 42;")

    expected = ProgramNode([], [ReturnStatement(IntegerNode(42))])
    assert nodes_equal(node, expected)


def test_empty_return():
    node = init_parser("return;")

    expected = ProgramNode([], [ReturnStatement()])
    assert nodes_equal(node, expected)


def test_break_statement():
    node = init_parser("break;")

    expected = ProgramNode([], [BreakStatement()])
    assert nodes_equal(node, expected)


def test_empty_block_statement():
    node = init_parser("{ }")

    expected = ProgramNode([], [BlockStatement([])])
    assert nodes_equal(node, expected)


def test_block_statement():
    node = init_parser("{ return 7; }")

    expected = ProgramNode([], [BlockStatement([ReturnStatement(IntegerNode(7))])])
    assert nodes_equal(node, expected)


def test_block_statement_with_multiple_statements():
    node = init_parser("{ x + 5; y + 3; }")

    expected = ProgramNode([], [BlockStatement(
        [
            ExpressionStatement(BinaryOpNode("+", IdentifierNode("x"), IntegerNode(5))),
            ExpressionStatement(BinaryOpNode("+", IdentifierNode("y"), IntegerNode(3))),
        ]
    )])
    assert nodes_equal(node, expected)


def test_method_declaration():
    result = init_parser("class TestClass { init() {} def int add(int x, int y) { return x + y; } } return 0;")

    expected = ProgramNode([ClassDef(
        "TestClass",
        None,
        [],
        Constructor([], None, []),
        [MethodDef(
            "int",
            "add",
            [("int", "x"), ("int", "y")],
            [ReturnStatement(BinaryOpNode("+", IdentifierNode("x"), IdentifierNode("y")))],
        )]
    )], [ReturnStatement(IntegerNode(0))])
    assert nodes_equal(result, expected)


def test_method_declaration_with_no_params():
    result = init_parser("class TestClass { init() {} def int add() { return; } } return 0;")

    expected = ProgramNode([ClassDef(
        "TestClass",
        None,
        [],
        Constructor([], None, []),
        [MethodDef("int", "add", [], [ReturnStatement()])]
    )], [ReturnStatement(IntegerNode(0))])
    assert nodes_equal(result, expected)


def test_void_method():
    result = init_parser("class TestClass { init() {} def void foo() { } } return 0;")

    expected = ProgramNode([ClassDef(
        "TestClass",
        None,
        [],
        Constructor([], None, []),
        [MethodDef("void", "foo", [], [])]
    )], [ReturnStatement(IntegerNode(0))])
    assert nodes_equal(result, expected)


def test_constructor():
    result = init_parser("class TestClass { init() { super(); } } return 0;")
    expected = ProgramNode([ClassDef(
        "TestClass",
        None,
        [],
        Constructor([], [], []),
        []
    )], [ReturnStatement(IntegerNode(0))])

    assert nodes_equal(result, expected)


def test_constructor_no_super():
    result = init_parser("class TestClass { init() { } } return 0;")
    expected = ProgramNode([ClassDef(
        "TestClass",
        None,
        [],
        Constructor([], None, []),
        []
    )], [ReturnStatement(IntegerNode(0))])

    assert nodes_equal(result, expected)

def test_constructor_with_super_args():
    result = init_parser("class TestClass { init() { super( x + 5 ); } } return 0;")
    expected = ProgramNode([ClassDef(
        "TestClass",
        None,
        [],
        Constructor([], [BinaryOpNode("+", IdentifierNode("x"), IntegerNode(5))], []),
        []
    )], [ReturnStatement(IntegerNode(0))])

    assert nodes_equal(result, expected)

def test_class():
    class_input = """class Animal {
    init() {}
    def int speak() { return 0; }
    }
    return 0;
    """

    result = init_parser(class_input)
    expected = ProgramNode([ClassDef("Animal", None, [], Constructor([], None, []),
                        [MethodDef("int", "speak", [], [ReturnStatement(IntegerNode(0))])])], [ReturnStatement(IntegerNode(0))])

    assert nodes_equal(result, expected)

def test_class_2():
    class_input = """class Animal extends Lifeform {
        int x;
        int y;
        init() {}
        def int speak() { return 0; }
        }
        return 0;
        """

    result = init_parser(class_input)
    expected = ProgramNode([ClassDef("Animal", "Lifeform", [("int", "x"), ("int", "y")], Constructor([], None, []),
                        [MethodDef("int", "speak", [], [ReturnStatement(IntegerNode(0))])])], [ReturnStatement(IntegerNode(0))])

    assert nodes_equal(result, expected)

def test_program():
    program = init_parser("int x = 0;")

    expected = ProgramNode([], [VarDecStatement("int", "x", IntegerNode(0))])

    assert nodes_equal(program, expected)