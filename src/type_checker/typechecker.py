from src.parser.ast_nodes import *

class IllTypeError(Exception):
    pass

class Typechecker:
    def __init__(self):
        pass

    def visit_integer_node(self, node: IntegerNode):
        return "int"

    def visit_boolean_node(self, node: BooleanNode):
        return "bool"

    def visit_identifier_node(self, node: IdentifierNode):
        pass

    def visit_binary_op_node(self, node: BinaryOpNode):
        left_type = self.visit(node.left_child)
        right_type = self.visit(node.right_child)
        if node.op in {"+", "-", "*", "/", "<", "<=", ">", ">="}:
            if left_type != "int" or right_type != "int":
                raise IllTypeError(f"Cannot '{node.op}' on non-int operands.")
            return "int"
        elif node.op in {"==", "!="}:
            if left_type != right_type:
                raise IllTypeError(f"Cannot '{node.op}' on different type operands.")
            return left_type
        raise IllTypeError()


    def visit(self, node: Node):
        if isinstance(node, IntegerNode):
            return self.visit_integer_node(node)
        if isinstance(node, BooleanNode):
            return self.visit_boolean_node(node)
        if isinstance(node, IdentifierNode):
            return self.visit_identifier_node()
        if isinstance(node, BinaryOpNode):
            return self.visit_binary_op_node(node)