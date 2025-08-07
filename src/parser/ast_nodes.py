from typing import Optional


class Node:
    pass


class IntegerNode(Node):
    def __init__(self, value: int):
        self.value = value


class IdentifierNode(Node):
    def __init__(self, value: str):
        self.value = value


class BinaryOpNode(Node):
    def __init__(self, op: str, left_child: Node, right_child: Node):
        self.op = op
        self.left_child = left_child
        self.right_child = right_child


class BooleanNode(Node):
    def __init__(self, value: bool):
        self.value = value


class PrintNode(Node):
    def __init__(self, inner_expression: Node):
        self.inner_expression = inner_expression


class ThisNode(Node):
    pass


class NewNode(Node):
    def __init__(self, class_name: str, arguments: list):
        self.class_name = class_name
        self.arguments = arguments


class CallNode(Node):
    def __init__(self, obj_node: Node, method_name: str, arguments: list):
        self.obj_node = obj_node
        self.method_name = method_name
        self.arguments = arguments


class StatementNode(Node):
    pass


class ExpressionStatement(StatementNode):
    def __init__(self, exp: Node):
        self.exp = exp


class VarDecStatement(StatementNode):
    def __init__(self, var_type: str, var: str, val: Node):
        self.var_type = var_type
        self.var = var
        self.val = val


class AssignmentStatement(StatementNode):
    def __init__(self, var: str, exp: Node):
        self.var = var
        self.exp = exp


class WhileStatement(StatementNode):
    def __init__(self, exp: Node, stmt: StatementNode):
        self.exp = exp
        self.stmt = stmt


class BreakStatement(StatementNode):
    pass


class ReturnStatement(StatementNode):
    def __init__(self, exp: Optional[Node] = None):
        self.exp = exp


class IfStatement(StatementNode):
    def __init__(
        self,
        exp: Node,
        then_stmt: StatementNode,
        else_stmt: Optional[StatementNode] = None,
    ):
        self.exp = exp
        self.then_stmt = then_stmt
        self.else_stmt = else_stmt


class BlockStatement(StatementNode):
    def __init__(self, stmts: list):
        self.stmts = stmts


class DeclarationNode(Node):
    pass


class MethodDef(DeclarationNode):
    def __init__(
        self, method_type: str, method_name: str, parameters: list, statements: list
    ):
        self.method_type = method_type
        self.method_name = method_name
        self.parameters = parameters
        self.statements = statements


class Constructor(DeclarationNode):
    def __init__(self, parameters: list, super_args: Optional[list], statements: list):
        self.parameters = parameters
        self.super_args = super_args
        self.statements = statements


class ClassDef(DeclarationNode):
    def __init__(self, class_name: str, extend_class_name: Optional[str], class_instance_vars: list, constructor: Constructor, methods: list):
        self.class_name = class_name
        self.extend_class_name = extend_class_name
        self.class_instance_vars = class_instance_vars
        self.constructor = constructor
        self.methods = methods