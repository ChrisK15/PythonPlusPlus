from src.lexer.token import TokenType

COMPARISON_OPERATORS = {
    TokenType.LESS_THAN,
    TokenType.GREATER_THAN,
    TokenType.LESS_EQUAL,
    TokenType.GREATER_EQUAL,
}

EQUAL_OPERATORS = {
    TokenType.EQUAL,
    TokenType.NOT_EQUAL,
}

TYPES = {
    TokenType.INT_TYPE,
    TokenType.BOOL_TYPE,
}
