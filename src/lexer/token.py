from dataclasses import dataclass
from enum import Enum, auto
from typing import Union


class TokenType(Enum):
    INTEGER = auto()
    EOF = auto()


@dataclass
class Token:
    type: TokenType
    value: Union[int, None]
