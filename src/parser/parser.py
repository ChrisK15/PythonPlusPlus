from src.parser.ast_nodes import *
from src.parser.parser_constants import *


class ParserParenthesisException(Exception):
    pass


class ParserException(Exception):
    pass


class Parser:
    def __init__(self, tokens: list):
        self.tokens = tokens
        self.position = 0
        self.current_token = tokens[0] if tokens else None

    def next_token(self):
        if self.position < len(self.tokens) - 1:
            self.position += 1
            self.current_token = self.tokens[self.position]
        else:
            return  # Would return our results here

    def parse_comma_exp(self):
        arguments = []
        while self.current_token.type != TokenType.RIGHT_PAREN:
            expression = self.parse_assignment()
            arguments.append(expression)
            if self.current_token.type != TokenType.COMMA:
                break
            self.next_token()
        if self.current_token.type == TokenType.RIGHT_PAREN:
            self.next_token()
            return arguments
        else:
            raise ParserParenthesisException("Error! No closing parenthesis.")

    # START OF CHAIN
    def parse_statement(self):
        pass

    def parse_equality(self):
        left_expression = self.parse_comparison()
        while self.current_token.type in EQUAL_OPERATORS:
            current_operator_token = self.current_token
            self.next_token()
            right_expression = self.parse_comparison()
            left_expression = BinaryOpNode(
                current_operator_token.value, left_expression, right_expression
            )
        return left_expression

    def parse_comparison(self):
        left_expression = self.parse_addition()
        while self.current_token.type in COMPARISON_OPERATORS:
            current_operator_token = self.current_token
            self.next_token()
            right_expression = self.parse_addition()
            left_expression = BinaryOpNode(
                current_operator_token.value, left_expression, right_expression
            )
        return left_expression

    def parse_addition(self):
        left_expression = self.parse_multiplication()
        while (
            self.current_token.type == TokenType.PLUS
            or self.current_token.type == TokenType.MINUS
        ):
            current_operator_token = self.current_token
            self.next_token()
            right_expression = self.parse_multiplication()
            left_expression = BinaryOpNode(
                current_operator_token.value, left_expression, right_expression
            )
        return left_expression

    def parse_multiplication(self):
        left_expression = self.parse_call()
        while (
            self.current_token.type == TokenType.MULTIPLY
            or self.current_token.type == TokenType.DIVIDE
        ):
            current_operator_token = self.current_token
            self.next_token()
            right_expression = self.parse_call()
            left_expression = BinaryOpNode(
                current_operator_token.value, left_expression, right_expression
            )
        return left_expression

    def parse_call(self):
        obj_node = self.parse_primary()
        while self.current_token.type == TokenType.DOT:
            self.next_token()
            if self.current_token.type == TokenType.IDENTIFIER:
                method_name = self.current_token.value
                self.next_token()
            else:
                raise ParserException("Error! Invalid method type.")
            if self.current_token.type == TokenType.LEFT_PAREN:
                self.next_token()
                arguments = self.parse_comma_exp()
                obj_node = CallNode(obj_node, method_name, arguments)
            else:
                raise ParserParenthesisException("Error! Missing parenthesis.")
        return obj_node

    def parse_primary(self):
        if self.current_token.type == TokenType.INTEGER:
            value = self.current_token.value
            self.next_token()
            return IntegerNode(value)
        elif self.current_token.type == TokenType.BOOLEAN:
            value = self.current_token.value
            self.next_token()
            return BooleanNode(value)
        elif self.current_token.type == TokenType.IDENTIFIER:
            value = self.current_token.value
            self.next_token()
            return IdentifierNode(value)
        elif self.current_token.type == TokenType.THIS:
            self.next_token()
            return ThisNode()
        elif self.current_token.type == TokenType.NEW:
            self.next_token()
            if self.current_token.type == TokenType.IDENTIFIER:
                class_name = self.current_token.value
                self.next_token()
            else:
                raise ParserException("Error! No class name after 'new'.")
            if self.current_token.type == TokenType.LEFT_PAREN:
                self.next_token()
                arguments = self.parse_comma_exp()
                return NewNode(class_name, arguments)
            else:
                raise ParserParenthesisException(
                    "Error! No opening parenthesis on new class."
                )
        elif self.current_token.type == TokenType.PRINT:
            self.next_token()
            if self.current_token.type == TokenType.LEFT_PAREN:
                self.next_token()
                inner_expression = self.parse_assignment()
                if self.current_token.type == TokenType.RIGHT_PAREN:
                    self.next_token()
                    return PrintNode(inner_expression)
                else:
                    raise ParserParenthesisException(
                        "Error! Missing closing parenthesis."
                    )
            else:
                raise ParserParenthesisException(
                    "Error! Missing open parenthesis after print"
                )
        elif self.current_token.type == TokenType.LEFT_PAREN:
            self.next_token()
            inner_expression = self.parse_assignment()
            if self.current_token.type == TokenType.RIGHT_PAREN:
                self.next_token()
                return inner_expression
            else:
                raise ParserParenthesisException("Error! Missing closing parenthesis.")
        else:
            raise ParserException(
                f"Error! Unexpected invalid input: {self.current_token.value} of type {self.current_token.type}"
            )
