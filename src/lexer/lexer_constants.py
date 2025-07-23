from src.lexer.token import TokenType

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
