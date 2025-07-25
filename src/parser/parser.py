from src.lexer.token import TokenType

from src.parser.ast_nodes import *

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
            return # Would return our results here

    def parse_addition(self):
        pass

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
                raise ParserException(f"Error! Missing closing parenthesis.")
        else:
            raise ParserException(f"Error! Unknown input: {self.current_token}")