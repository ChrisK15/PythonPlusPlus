from src.parser.ast_nodes import *

"""
THE FOLLOWING FUNCTION IS FOR TESTING PURPOSES ONLY.

MAKES TESTING EASIER BY RECURSIVELY CHECKING NESTED NODES.
"""


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

        if (
            test_input.extend_class_name is None
            and test_output.extend_class_name is None
        ):
            pass
        elif (
            test_input.extend_class_name is None
            or test_output.extend_class_name is None
        ):
            return False
        elif test_input.extend_class_name != test_output.extend_class_name:
            return False

        if len(test_input.class_instance_vars) == len(test_output.class_instance_vars):
            for test_input_tuple, test_output_tuple in zip(
                test_input.class_instance_vars, test_output.class_instance_vars
            ):
                if test_input_tuple != test_output_tuple:
                    return False

        else:
            return False

        if not nodes_equal(test_input.constructor, test_output.constructor):
            return False

        if len(test_input.methods) == len(test_output.methods):
            for test_input_method, test_output_method in zip(
                test_input.methods, test_output.methods
            ):
                if not nodes_equal(test_input_method, test_output_method):
                    return False
        else:
            return False
        return True

    elif isinstance(test_input, ProgramNode):
        assert isinstance(test_output, ProgramNode)
        if len(test_input.class_defs) == len(test_output.class_defs):
            for test_input_classdef, test_output_classdef in zip(
                test_input.class_defs, test_output.class_defs
            ):
                if not nodes_equal(test_input_classdef, test_output_classdef):
                    return False
        if len(test_input.statements) == len(test_output.statements):
            for test_input_statement, test_output_statement in zip(
                test_input.statements, test_output.statements
            ):
                if not nodes_equal(test_input_statement, test_output_statement):
                    return False
        return True

    else:
        # Unknown node type - this should not happen
        raise ValueError(f"Unknown node type: {type(test_input)}")
