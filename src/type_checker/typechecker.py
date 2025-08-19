from src.parser.ast_nodes import *

class IllTypeError(Exception):
    pass

class Typechecker:
    def __init__(self):
        self.symbol_table = {}

    def visit_integer_node(self, node: IntegerNode):
        return "int"

    def visit_boolean_node(self, node: BooleanNode):
        return "bool"

    def visit_identifier_node(self, node: IdentifierNode):
        if node.value in self.symbol_table:
            return self.symbol_table[node.value]
        else:
            raise IllTypeError(f"Undefined variable: {node.value}")

    def visit_print_node(self, node: PrintNode):
        self.visit(node.inner_expression)
        return "void"

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

    def visit_var_dec(self, node: VarDecStatement):
        if node.var in self.symbol_table:
            raise IllTypeError(f"The variable {node.var} is already defined.")
        val_type = self.visit(node.val)
        if val_type != node.var_type:
            raise IllTypeError(f"Incompatible types being assigned to each other. Cannot assign {val_type} to {node.var_type}.")
        self.symbol_table[node.var] = node.var_type

    def visit_assignment(self, node: AssignmentStatement):
        if node.var not in self.symbol_table:
            raise IllTypeError(f"{node.var} has not been declared.")
        exp_type = self.visit(node.exp)
        if exp_type != self.symbol_table[node.var]:
            raise IllTypeError(f"Incompatible types being assigned to each other. Cannot assign {exp_type} to {self.symbol_table[node.var]}.")

    def visit_expression(self, node: ExpressionStatement):
        self.visit(node.exp)

    def visit_return(self, node: ReturnStatement):
        if node.exp:
            self.visit(node.exp)

    def visit(self, node: Node):
        if isinstance(node, IntegerNode):
            return self.visit_integer_node(node)
        if isinstance(node, BooleanNode):
            return self.visit_boolean_node(node)
        if isinstance(node, IdentifierNode):
            return self.visit_identifier_node(node)
        if isinstance(node, BinaryOpNode):
            return self.visit_binary_op_node(node)
        if isinstance(node, VarDecStatement):
            return self.visit_var_dec(node)
        if isinstance(node, PrintNode):
            return self.visit_print_node(node)
        if isinstance(node, AssignmentStatement):
            return self.visit_assignment(node)
        if isinstance(node, ExpressionStatement):
            return self.visit_expression(node)
        if isinstance(node, ReturnStatement):
            return self.visit_return(node)