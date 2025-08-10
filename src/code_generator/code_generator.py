from src.parser.ast_nodes import *


class CodeGeneratorException(Exception):
    pass


class CodeGenerator:
    def __init__(self):
        pass

    def visit(self, node: Node):
        if isinstance(node, IntegerNode):
            return str(node.value)
        elif isinstance(node, BooleanNode):
            return str(node.value).lower()
        elif isinstance(node, IdentifierNode):
            return node.value
        elif isinstance(node, BinaryOpNode):
            left = self.visit(node.left_child)
            right = self.visit(node.right_child)
            return f"{left} {node.op} {right}"
        else:
            raise CodeGeneratorException()