from dataclasses import dataclass
from enum import Enum, auto
from typing import Union


class TokenType(Enum):
    # Literals
    INTEGER = auto()
    BOOLEAN = auto()
    IDENTIFIER = auto()  # var names, class names, etc.
    
    # Keywords
    CLASS = auto()
    DEF = auto()
    INIT = auto()
    IF = auto()
    WHILE = auto()
    RETURN = auto()
    BREAK = auto()
    NEW = auto()
    THIS = auto()
    
    # Operators
    PLUS = auto()          # +
    MINUS = auto()         # -
    MULTIPLY = auto()      # *
    DIVIDE = auto()        # /
    ASSIGN = auto()        # =
    EQUAL = auto()         # ==
    NOT_EQUAL = auto()     # !=
    LESS_THAN = auto()     # <
    LESS_EQUAL = auto()    # <=
    GREATER_THAN = auto()  # >
    GREATER_EQUAL = auto() # >=
    
    # Punctuation
    LEFT_PAREN = auto()    # (
    RIGHT_PAREN = auto()   # )
    LEFT_BRACE = auto()    # {
    RIGHT_BRACE = auto()   # }
    SEMICOLON = auto()     # ;
    COMMA = auto()         # ,
    DOT = auto()           # .
    
    EOF = auto()


@dataclass
class Token:
    type: TokenType
    value: Union[int, bool, str, None]
