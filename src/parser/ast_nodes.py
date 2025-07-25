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
