from typing import List

from src.lexer.token import Token, TokenType


class Lexer:
    def __init__(self, text: str):
        self.text = text
        self.position = 0

    def tokenize(self) -> List[Token]:
        tokens = []

        # If we find a digit
        if self.position < len(self.text) and self.text[self.position].isdigit():
            current_output = ""
            # If more digits follow
            while self.position < len(self.text) and self.text[self.position].isdigit():
                current_output += self.text[self.position]
                self.position += 1
            final_integer = int(current_output)
            tokens.append(Token(TokenType.INTEGER, final_integer))

        tokens.append(Token(TokenType.EOF, None))
        return tokens
