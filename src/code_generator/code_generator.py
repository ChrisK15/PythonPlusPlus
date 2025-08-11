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
        if isinstance(node, WhileStatement):
            exp = self.visit(node.exp)
            stmt = self.visit(node.stmt)
            return f"while ({exp}) {stmt}"
        if isinstance(node, BreakStatement):
            return "break;"
        if isinstance(node, ReturnStatement):
            if node.exp:
                exp = self.visit(node.exp)
                return f"return {exp};"
            return "return;"
        if isinstance(node, IfStatement):
            exp = self.visit(node.exp)
            then_stmt = self.visit(node.then_stmt)
            if node.else_stmt:
                else_stmt = self.visit(node.else_stmt)
                return f"if ({exp}) {then_stmt} else {else_stmt}"
            return f"if ({exp}) {then_stmt}"
        if isinstance(node, BlockStatement):
            visited_stmts = [self.visit(stmt) for stmt in node.stmts]
            stmts = ' '.join(visited_stmts)
            return f"{{ {stmts} }}"
        if isinstance(node, MethodDef):
            visited_params = [param[1] for param in node.parameters]
            visited_stmts = [self.visit(stmt) for stmt in node.statements]
            params = ", ".join(visited_params)
            stmts = " ".join(visited_stmts)
            return f"function {node.method_name}({params}) {{ {stmts} }}"
        else:
            raise CodeGeneratorException()
