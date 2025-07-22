from enum import Enum, auto
from dataclasses import dataclass


class TokenType(Enum):
    INTEGER = auto()
    EOF = auto()

@dataclass
class Token:
    type: TokenType
    value: any
    line: int
    column: int