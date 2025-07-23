from typing import List

from src.lexer.token import Token, TokenType


class Lexer:
    def __init__(self, text: str):
        self.text = text
        self.position = 0

    KEYWORDS = {"true": (TokenType.BOOLEAN, True),
                "false": (TokenType.BOOLEAN, False),
                "class": (TokenType.CLASS, None),
                "def": (TokenType.DEF, None),
                "init": (TokenType.INIT, None),
                "if": (TokenType.IF, None),
                "while": (TokenType.WHILE, None),
                "return": (TokenType.RETURN, None),
                "break": (TokenType.BREAK, None),
                "new": (TokenType.NEW, None),
                "this": (TokenType.THIS, None)
                }

    def tokenize(self) -> List[Token]:
        tokens = []

        while self.position < len(self.text):  # While we still have input remaining
            if self.text[self.position].isspace():
                self.position += 1
                continue

            # If we find a digit
            if self.position < len(self.text) and self.text[self.position].isdigit():
                current_output = ""
                while (
                    self.position < len(self.text)
                    and self.text[self.position].isdigit()
                ):
                    current_output += self.text[self.position]
                    self.position += 1
                final_integer = int(current_output)
                tokens.append(Token(TokenType.INTEGER, final_integer))

            # If we find a word
            if self.position < len(self.text) and self.text[self.position].isalpha():
                current_output = ""
                while (
                    self.position < len(self.text)
                    and self.text[self.position].isalnum()
                ):
                    current_output += self.text[self.position]
                    self.position += 1
                if current_output in self.KEYWORDS:
                    token_type, token_value = self.KEYWORDS[current_output]
                    tokens.append(Token(token_type, token_value))
                else:
                    tokens.append(Token(TokenType.IDENTIFIER, current_output))

        tokens.append(Token(TokenType.EOF, None))
        return tokens
