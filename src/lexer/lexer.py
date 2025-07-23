from typing import List

from src.lexer.lexer_constants import (AMBIGUOUS_OPERATORS, RESERVED_WORDS,
                                       MULTI_CHAR_OPERATORS,
                                       SINGLE_CHAR_OPERATORS)
from src.lexer.token import Token, TokenType

class TokenizerExceptions(Exception):
    pass

class Lexer:
    def __init__(self, text: str):
        self.text = text
        self.position = 0

    def tokenize(self) -> List[Token]:
        tokens = []

        while self.position < len(self.text):  # While we still have input remaining
            # Ignores whitespace
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
            elif self.position < len(self.text) and self.text[self.position].isalpha():
                current_output = ""
                while (
                    self.position < len(self.text)
                    and self.text[self.position].isalnum()
                ):
                    current_output += self.text[self.position]
                    self.position += 1
                if current_output in RESERVED_WORDS:
                    token_type, token_value = RESERVED_WORDS[current_output]
                    tokens.append(Token(token_type, token_value))
                else:
                    tokens.append(Token(TokenType.IDENTIFIER, current_output))

            # If we find an operator
            elif (
                self.position < len(self.text)
                and self.text[self.position] in SINGLE_CHAR_OPERATORS
            ):
                # The operator could consist of two characters, we have to check for this
                if (
                    self.text[self.position] in AMBIGUOUS_OPERATORS
                    and self.position + 1 < len(self.text)
                    and self.text[self.position + 1] == "="
                ):
                    current_operator = (
                        self.text[self.position] + self.text[self.position + 1]
                    )
                    tokens.append(Token(MULTI_CHAR_OPERATORS[current_operator], None))
                    self.position += 2
                else:
                    tokens.append(
                        Token(SINGLE_CHAR_OPERATORS[self.text[self.position]], None)
                    )
                    self.position += 1

            # If character is NOT valid (i.e: '$', '@')
            else:
                raise TokenizerExceptions(
                    "Invalid character: '"
                    + self.text[self.position]
                    + "' cannot be tokenized!"
                )

        tokens.append(Token(TokenType.EOF, None))
        return tokens
