from src.lexer.token import TokenType
from src.parser.ast_nodes import *

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
        left_expression = self.parse_primary()
        while (
            self.current_token.type == TokenType.MULTIPLY
            or self.current_token.type == TokenType.DIVIDE
        ):
            current_operator_token = self.current_token
            self.next_token()
            right_expression = self.parse_primary()
            left_expression = BinaryOpNode(
                current_operator_token.value, left_expression, right_expression
            )
        return left_expression

    def parse_primary(self):
        if self.current_token.type == TokenType.INTEGER:
            value = self.current_token.value
            self.next_token()
            return IntegerNode(value)
        elif self.current_token.type == TokenType.IDENTIFIER:
            value = self.current_token.value
            self.next_token()
            return IdentifierNode(value)
        elif self.current_token.type == TokenType.LEFT_PAREN:
            self.next_token()
            inner_expression = self.parse_addition()
            if self.current_token.type == TokenType.RIGHT_PAREN:
                self.next_token()
                return inner_expression
            else:
                raise ParserParenthesisException(f"Error! Missing closing parenthesis.")
        else:
            raise ParserException(f"Error! Unknown input: {self.current_token}")
