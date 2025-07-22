from dataclasses import dataclass
from enum import Enum, auto


class TokenType(Enum):
    INTEGER = auto()
    EOF = auto()


@dataclass
class Token:
    type: TokenType
    value: any
