from src.parser.ast_nodes import *


class CodeGenerator:
    def __init__(self, node: Node):
        self.node = node

    def visit(self):
        if isinstance(self.node, IntegerNode):
            return str(self.node.value)
        elif isinstance(self.node, BooleanNode):
            return str(self.node.value).lower()
        elif isinstance(self.node, IdentifierNode):
            return self.node.value