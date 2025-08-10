from src.parser.ast_nodes import *


class CodeGeneratorException(Exception):
    pass


class CodeGenerator:
    def __init__(self):
        pass

    def visit(self, node: Node):
        if isinstance(node, IntegerNode):
            return str(node.value)
        if isinstance(node, BooleanNode):
            return str(node.value).lower()
        if isinstance(node, IdentifierNode):
            return node.value
        if isinstance(node, BinaryOpNode):
            left = self.visit(node.left_child)
            right = self.visit(node.right_child)
            return f"{left} {node.op} {right}"
        if isinstance(node, PrintNode):
            inner_expression = self.visit(node.inner_expression)
            return f"console.log({inner_expression})"
        if isinstance(node, ThisNode):
            return "this"
        if isinstance(node, NewNode):
            visited_args = [self.visit(argument) for argument in node.arguments]
            arguments = ', '.join(visited_args)
            return f"new {node.class_name}({arguments})"
        if isinstance(node, CallNode):
            obj_name = self.visit(node.obj_node)
            visited_args = [self.visit(argument) for argument in node.arguments]
            arguments = ', '.join(visited_args)
            return f"{obj_name}.{node.method_name}({arguments})"
        if isinstance(node, ExpressionStatement):
            exp = self.visit(node.exp)
            return f"{exp};"
        if isinstance(node, VarDecStatement):
            val = self.visit(node.val)
            return f"{node.var_type} {node.var} = {val}"
        if isinstance(node, AssignmentStatement):
            exp = self.visit(node.exp)
            return f"{node.var} = {exp};"
        else:
            raise CodeGeneratorException()
