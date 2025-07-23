from typing import List

from src.lexer.token import Token, TokenType


class Lexer:
    def __init__(self, text: str):
        self.text = text
        self.position = 0

    KEYWORDS = {
        "true": (TokenType.BOOLEAN, True),
        "false": (TokenType.BOOLEAN, False),
        "class": (TokenType.CLASS, None),
        "def": (TokenType.DEF, None),
        "init": (TokenType.INIT, None),
        "if": (TokenType.IF, None),
        "while": (TokenType.WHILE, None),
        "return": (TokenType.RETURN, None),
        "break": (TokenType.BREAK, None),
        "new": (TokenType.NEW, None),
        "this": (TokenType.THIS, None),
    }

    OPERATORS = {"+", "-", "*", "/", "=", "!", "<", ">"}

    SINGLE_CHAR_OPERATORS = {
        "+": TokenType.PLUS,
        "-": TokenType.MINUS,
        "*": TokenType.MULTIPLY,
        "/": TokenType.DIVIDE,
        "(": TokenType.LEFT_PAREN,
        ")": TokenType.RIGHT_PAREN,
        "{": TokenType.LEFT_BRACE,
        "}": TokenType.RIGHT_BRACE,
        ";": TokenType.SEMICOLON,
        ",": TokenType.COMMA,
        ".": TokenType.DOT,
        "=": TokenType.ASSIGN,
        "<": TokenType.LESS_THAN,
        ">": TokenType.GREATER_THAN,
        "!": TokenType.EXCLAMATION,
    }

    MULTI_CHAR_OPERATORS = {
        "==": TokenType.EQUAL,
        "!=": TokenType.NOT_EQUAL,
        "<=": TokenType.LESS_EQUAL,
        ">=": TokenType.GREATER_EQUAL,
    }

    AMBIGUOUS_OPERATORS = {"=", "<", ">", "!"}

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
            elif self.position < len(self.text) and self.text[self.position].isalpha():
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

            # If we find an operator
            elif (
                self.position < len(self.text)
                and self.text[self.position] in self.SINGLE_CHAR_OPERATORS
            ):
                # The operator could consist of two characters, we have to check for this
                if (
                    self.text[self.position] in self.AMBIGUOUS_OPERATORS
                    and self.position + 1 < len(self.text)
                    and self.text[self.position + 1] == "="
                ):
                    current_operator = (
                        self.text[self.position] + self.text[self.position + 1]
                    )
                    tokens.append(
                        Token(self.MULTI_CHAR_OPERATORS[current_operator], None)
                    )
                    self.position += 2
                else:
                    tokens.append(
                        Token(
                            self.SINGLE_CHAR_OPERATORS[self.text[self.position]], None
                        )
                    )
                    self.position += 1

        tokens.append(Token(TokenType.EOF, None))
        return tokens
