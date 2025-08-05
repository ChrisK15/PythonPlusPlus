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
    def __init__(self, type: str, var: str):
        self.type = type
        self.var = var


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
    def __init__(self, exp: Node = None):
        self.exp = exp


class IfStatement(StatementNode):
    def __init__(
        self, exp: Node, then_stmt: StatementNode, else_stmt: StatementNode = None
    ):
        self.exp = exp
        self.then_stmt = then_stmt
        self.else_stmt = else_stmt


class BlockStatement(StatementNode):
    def __init__(self, stmts: list):
        self.stmts = stmts
