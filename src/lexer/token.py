from dataclasses import dataclass
from enum import Enum, auto
from typing import Union


class TokenType(Enum):
    INTEGER = auto()
    BOOLEAN = auto()
    IDENTIFIER = auto() # var names, class names, etc.
    EOF = auto()


@dataclass
class Token:
    type: TokenType
    value: Union[int, bool, str, None]
