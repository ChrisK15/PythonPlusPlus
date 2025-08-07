from typing import List

from src.lexer.lexer_constants import (AMBIGUOUS_OPERATORS,
                                       MULTI_CHAR_OPERATORS, RESERVED_WORDS,
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
                while self.position < len(self.text) and (
                    self.text[self.position].isalnum()
                    or self.text[self.position] == "_"
                ):
                    current_output += self.text[self.position]
                    self.position += 1
                if current_output in RESERVED_WORDS:
                    reserved_token_type, reserved_token_value = RESERVED_WORDS[
                        current_output
                    ]
                    tokens.append(Token(reserved_token_type, reserved_token_value))
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
                    multi_token_type, multi_token_value = MULTI_CHAR_OPERATORS[
                        current_operator
                    ]
                    tokens.append(Token(multi_token_type, multi_token_value))
                    self.position += 2
                else:
                    single_token_type, single_token_value = SINGLE_CHAR_OPERATORS[
                        self.text[self.position]
                    ]
                    tokens.append(Token(single_token_type, single_token_value))
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
