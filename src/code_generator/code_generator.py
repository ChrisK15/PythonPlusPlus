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
            arguments = ", ".join(visited_args)
            return f"new {node.class_name}({arguments})"
        if isinstance(node, CallNode):
            obj_name = self.visit(node.obj_node)
            visited_args = [self.visit(argument) for argument in node.arguments]
            arguments = ", ".join(visited_args)
            return f"{obj_name}.{node.method_name}({arguments})"
        if isinstance(node, ExpressionStatement):
            exp = self.visit(node.exp)
            return f"{exp};"
        if isinstance(node, VarDecStatement):
            val = self.visit(node.val)
            return f"{node.var} = {val};"
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
            stmts = " ".join(visited_stmts)
            return f"{{ {stmts} }}"
        if isinstance(node, MethodDef):
            list_params = [param[1] for param in node.parameters]
            visited_stmts = [self.visit(stmt) for stmt in node.statements]
            params = ", ".join(list_params)
            stmts = " ".join(visited_stmts)
            return f"{node.method_name}({params}) {{ {stmts} }}"
        if isinstance(node, Constructor):
            list_params = [param[1] for param in node.parameters]
            visited_stmts = [self.visit(stmt) for stmt in node.statements]
            params = ", ".join(list_params)
            stmts = " ".join(visited_stmts)
            if node.super_args:
                visited_super_args = [
                    self.visit(super_arg) for super_arg in node.super_args
                ]
                super_args = ", ".join(visited_super_args)
                return f"constructor({params}) {{ super({super_args}); {stmts} }}"
            # If no super:
            return f"constructor({params}) {{ {stmts} }}"
        if isinstance(node, ClassDef):
            list_instance_vars = [
                instance_var[1] for instance_var in node.class_instance_vars
            ]
            constructor = self.visit(node.constructor)
            visited_methods = [self.visit(method) for method in node.methods]
            methods = " ".join(visited_methods)
            instance_vars = "; ".join(list_instance_vars)
            if instance_vars:
                instance_vars += ";"
            if node.extend_class_name:
                return f"class {node.class_name} extends {node.extend_class_name} {{ {instance_vars} {constructor} {methods} }}"
            # If no extend:
            return (
                f"class {node.class_name} {{{instance_vars} {constructor} {methods} }}"
            )
        if isinstance(node, ProgramNode):
            visited_classes = [self.visit(classdef) for classdef in node.class_defs]
            visited_statements = [self.visit(stmt) for stmt in node.statements]
            classes = " ".join(visited_classes)
            statements = " ".join(visited_statements)
            return f"{classes}{statements}"
        else:
            raise CodeGeneratorException()
