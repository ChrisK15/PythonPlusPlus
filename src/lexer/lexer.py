from typing import List
from .token import Token, TokenType

class Lexer:
    def __init__(self, text: str):
        self.text = text

    def tokenize(self) -> List[Token]:
        return [Token(TokenType.EOF, None)]