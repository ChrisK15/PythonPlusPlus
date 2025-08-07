from src.parser.ast_nodes import *
from src.parser.parser_constants import *


class ParserParenthesisException(Exception):
    pass


class ParserException(Exception):
    pass


class Parser:
    def __init__(self, tokens: list):
        self.tokens = tokens
        self.position = 0
        self.current_token = tokens[0] if tokens else None

    def next_token(self):
        if self.position < len(self.tokens) - 1:
            self.position += 1
            self.current_token = self.tokens[self.position]

    def parse_comma_exp(self):
        arguments = []
        while self.current_token.type != TokenType.RIGHT_PAREN:
            expression = self.parse_equality()
            arguments.append(expression)
            if self.current_token.type != TokenType.COMMA:
                break
            self.next_token()
        if self.current_token.type == TokenType.RIGHT_PAREN:
            self.next_token()
            return arguments
        else:
            raise ParserParenthesisException("Error! No closing parenthesis.")

    def parse_comma_params(self):
        parameters = []
        while self.current_token.type != TokenType.RIGHT_PAREN:
            if self.current_token.type in TYPES:
                param_type = self.current_token.value
                self.next_token()
                if self.current_token.type == TokenType.IDENTIFIER:
                    param_name = self.current_token.value
                    self.next_token()
                    parameters.append((param_type, param_name))
                    if self.current_token.type != TokenType.COMMA:
                        break
                    self.next_token()
                else:
                    raise ParserException(
                        "Unexpected error when parsing parameters. No identifier."
                    )
            else:
                raise ParserException(
                    "Unexpected error when parsing parameters. No type provided."
                )
        if self.current_token.type == TokenType.RIGHT_PAREN:
            self.next_token()
            return parameters
        else:
            raise ParserParenthesisException("Missing right paren on parameters.")

    def parse_vardec(self):
        vardec_type = self.current_token.value
        self.next_token()
        if self.current_token.type == TokenType.IDENTIFIER:
            vardec_id = self.current_token.value
            self.next_token()
            if self.current_token.type == TokenType.ASSIGN:
                self.next_token()
                vardec_val = self.parse_equality()
                if self.current_token.type == TokenType.SEMICOLON:
                    self.next_token()
                    return VarDecStatement(vardec_type, vardec_id, vardec_val)
                else:
                    raise ParserException("Missing semi colon in variable declaration.")
            else:
                raise ParserException("Error in variable declaration.")
        else:
            raise ParserException("Error in variable declaration.")

    def parse_assignment(self):
        assignment_var = self.current_token.value
        self.next_token()
        self.next_token()  # Skip '='
        assignment_exp = self.parse_equality()
        if self.current_token.type == TokenType.SEMICOLON:
            self.next_token()
            return AssignmentStatement(assignment_var, assignment_exp)
        else:
            raise ParserException("Error! Missing semi colon in assignment.")

    def parse_while(self):
        self.next_token()
        if self.current_token.type == TokenType.LEFT_PAREN:
            self.next_token()
            while_expression = self.parse_equality()
            if self.current_token.type == TokenType.RIGHT_PAREN:
                self.next_token()
                while_stmt = self.parse_statement()
                return WhileStatement(while_expression, while_stmt)
            else:
                raise ParserException("Error! Missing right paren on while.")
        else:
            raise ParserException("Error! Missing left paren on while.")

    def parse_break(self):
        self.next_token()
        if self.current_token.type == TokenType.SEMICOLON:
            self.next_token()
            return BreakStatement()
        else:
            raise ParserException("Error! Missing semicolon from break.")

    def parse_return(self):
        self.next_token()
        if self.current_token.type == TokenType.SEMICOLON:
            self.next_token()
            return ReturnStatement()
        else:
            return_exp = self.parse_equality()
            if self.current_token.type == TokenType.SEMICOLON:
                self.next_token()
                return ReturnStatement(return_exp)
            else:
                raise ParserException("Error! Missing semicolon from return.")

    def parse_if(self):
        self.next_token()
        if self.current_token.type == TokenType.LEFT_PAREN:
            self.next_token()
            if_expression = self.parse_equality()
            if self.current_token.type == TokenType.RIGHT_PAREN:
                self.next_token()
                then_stmt = self.parse_statement()
                if self.current_token.type == TokenType.ELSE:
                    self.next_token()
                    else_stmt = self.parse_statement()
                    return IfStatement(if_expression, then_stmt, else_stmt)
                else:
                    return IfStatement(if_expression, then_stmt)
            else:
                raise ParserParenthesisException("Error! Missing right paren on if.")
        else:
            raise ParserParenthesisException("Error! Missing left paren on if.")

    def parse_block(self):
        block_stmts = []
        while self.current_token.type != TokenType.RIGHT_BRACE:
            stmt = self.parse_statement()
            block_stmts.append(stmt)
        if self.current_token.type == TokenType.RIGHT_BRACE:
            self.next_token()
            return BlockStatement(block_stmts)
        else:
            raise ParserException("Error!")

    def parse_program(self):
        class_defs = []
        statements = []

        while self.current_token.type == TokenType.CLASS:
            self.next_token()
            class_defs.append(self.parse_classdef())
        while self.current_token.type != TokenType.EOF:
            statements.append(self.parse_statement())

        if not statements and not class_defs:
            raise ParserException("No statements provided.")
        return ProgramNode(class_defs, statements)

    def parse_classdef(self):
        extend_class_name = None
        if self.current_token.type == TokenType.IDENTIFIER:
            class_name = self.current_token.value
            self.next_token()
            if self.current_token.type == TokenType.EXTENDS:
                self.next_token()
                if self.current_token.type == TokenType.IDENTIFIER:
                    extend_class_name = self.current_token.value
                    self.next_token()
            if self.current_token.type == TokenType.LEFT_BRACE:
                # If not extending another class
                self.next_token()
                params = []
                while self.current_token.type != TokenType.INIT:
                    if self.current_token.type in TYPES:
                        param_type = self.current_token.value
                        self.next_token()
                        if self.current_token.type == TokenType.IDENTIFIER:
                            param_name = self.current_token.value
                            self.next_token()
                            if self.current_token.type == TokenType.SEMICOLON:
                                self.next_token()
                                params.append((param_type, param_name))
                            else:
                                raise ParserException(
                                    "Missing semicolon from params in classdef"
                                )
                        else:
                            raise ParserException()
                    else:
                        raise ParserException()
                self.next_token()
                class_constructor = self.parse_constructor()
                methods = []
                while self.current_token.type != TokenType.RIGHT_BRACE:
                    if self.current_token.type == TokenType.DEF:
                        self.next_token()
                        method = self.parse_methoddef()
                        methods.append(method)
                    else:
                        raise ParserException(f"Expected 'def' or '}}' but found {self.current_token.type}")
                self.next_token()
                return ClassDef(
                    class_name, extend_class_name, params, class_constructor, methods
                )
        raise ParserException("No identifier after class token.")

    def parse_constructor(self):
        if self.current_token.type == TokenType.LEFT_PAREN:
            self.next_token()
            parameters = self.parse_comma_params()
            if self.current_token.type == TokenType.LEFT_BRACE:
                self.next_token()
                if self.current_token.type == TokenType.SUPER:
                    self.next_token()
                    if self.current_token.type == TokenType.LEFT_PAREN:
                        self.next_token()
                        super_args = self.parse_comma_exp()
                        if self.current_token.type == TokenType.SEMICOLON:
                            self.next_token()
                            statements = self.parse_block().stmts
                            return Constructor(parameters, super_args, statements)
                        else:
                            raise ParserException("Missing semicolon on constructor")
                    else:
                        raise ParserException("No Parens on constructor")
                else:
                    super_args = None
                    statements = self.parse_block().stmts
                    return Constructor(parameters, super_args, statements)
            else:
                raise ParserException("Missing block for constructor")
        else:
            raise ParserException("No parens for init constructor")

    def parse_methoddef(self):
        if self.current_token.type in TYPES:
            method_type = self.current_token.value
            self.next_token()
            if self.current_token.type == TokenType.IDENTIFIER:
                method_name = self.current_token.value
                self.next_token()
                if self.current_token.type == TokenType.LEFT_PAREN:
                    self.next_token()
                    parameters = self.parse_comma_params()
                    if self.current_token.type == TokenType.LEFT_BRACE:
                        self.next_token()
                        statements = self.parse_block().stmts
                        return MethodDef(
                            method_type, method_name, parameters, statements
                        )
                    else:
                        raise ParserException(
                            "Couldn't find a block after method def attempt."
                        )

                else:
                    raise ParserException("Missing parens on methoddef")
            else:
                raise ParserException("Invalid syntax")
        else:
            raise ParserException("No 'type' after def")

    # START OF CHAIN
    def parse_statement(self):
        if self.current_token.type in TYPES:
            return self.parse_vardec()
        elif self.current_token.type == TokenType.IDENTIFIER:
            if (
                self.position + 1 < len(self.tokens)
                and self.tokens[self.position + 1].type == TokenType.ASSIGN
            ):
                return self.parse_assignment()
        elif self.current_token.type == TokenType.WHILE:
            return self.parse_while()
        elif self.current_token.type == TokenType.BREAK:
            return self.parse_break()
        elif self.current_token.type == TokenType.RETURN:
            return self.parse_return()
        elif self.current_token.type == TokenType.IF:
            return self.parse_if()
        elif self.current_token.type == TokenType.LEFT_BRACE:
            self.next_token()
            return self.parse_block()
        # Default case
        exp = self.parse_equality()
        if self.current_token.type == TokenType.SEMICOLON:
            self.next_token()
            return ExpressionStatement(exp)
        else:
            raise ParserException("Error! Missing semicolon on expression.")

    def parse_equality(self):
        left_expression = self.parse_comparison()
        while self.current_token.type in EQUAL_OPERATORS:
            current_operator_token = self.current_token
            self.next_token()
            right_expression = self.parse_comparison()
            left_expression = BinaryOpNode(
                current_operator_token.value, left_expression, right_expression
            )
        return left_expression

    def parse_comparison(self):
        left_expression = self.parse_addition()
        while self.current_token.type in COMPARISON_OPERATORS:
            current_operator_token = self.current_token
            self.next_token()
            right_expression = self.parse_addition()
            left_expression = BinaryOpNode(
                current_operator_token.value, left_expression, right_expression
            )
        return left_expression

    def parse_addition(self):
        left_expression = self.parse_multiplication()
        while (
            self.current_token.type == TokenType.PLUS
            or self.current_token.type == TokenType.MINUS
        ):
            current_operator_token = self.current_token
            self.next_token()
            right_expression = self.parse_multiplication()
            left_expression = BinaryOpNode(
                current_operator_token.value, left_expression, right_expression
            )
        return left_expression

    def parse_multiplication(self):
        left_expression = self.parse_call()
        while (
            self.current_token.type == TokenType.MULTIPLY
            or self.current_token.type == TokenType.DIVIDE
        ):
            current_operator_token = self.current_token
            self.next_token()
            right_expression = self.parse_call()
            left_expression = BinaryOpNode(
                current_operator_token.value, left_expression, right_expression
            )
        return left_expression

    def parse_call(self):
        obj_node = self.parse_primary()
        while self.current_token.type == TokenType.DOT:
            self.next_token()
            if self.current_token.type == TokenType.IDENTIFIER:
                method_name = self.current_token.value
                self.next_token()
            else:
                raise ParserException("Error! Invalid method type.")
            if self.current_token.type == TokenType.LEFT_PAREN:
                self.next_token()
                arguments = self.parse_comma_exp()
                obj_node = CallNode(obj_node, method_name, arguments)
            else:
                raise ParserParenthesisException("Error! Missing parenthesis.")
        return obj_node

    def parse_primary(self):
        if self.current_token.type == TokenType.INTEGER:
            value = self.current_token.value
            self.next_token()
            return IntegerNode(value)
        elif self.current_token.type == TokenType.BOOLEAN:
            value = self.current_token.value
            self.next_token()
            return BooleanNode(value)
        elif self.current_token.type == TokenType.IDENTIFIER:
            value = self.current_token.value
            self.next_token()
            return IdentifierNode(value)
        elif self.current_token.type == TokenType.THIS:
            self.next_token()
            return ThisNode()
        elif self.current_token.type == TokenType.NEW:
            self.next_token()
            if self.current_token.type == TokenType.IDENTIFIER:
                class_name = self.current_token.value
                self.next_token()
            else:
                raise ParserException("Error! No class name after 'new'.")
            if self.current_token.type == TokenType.LEFT_PAREN:
                self.next_token()
                arguments = self.parse_comma_exp()
                return NewNode(class_name, arguments)
            else:
                raise ParserParenthesisException(
                    "Error! No opening parenthesis on new class."
                )
        elif self.current_token.type == TokenType.PRINT:
            self.next_token()
            if self.current_token.type == TokenType.LEFT_PAREN:
                self.next_token()
                inner_expression = self.parse_equality()
                if self.current_token.type == TokenType.RIGHT_PAREN:
                    self.next_token()
                    return PrintNode(inner_expression)
                else:
                    raise ParserParenthesisException(
                        "Error! Missing closing parenthesis."
                    )
            else:
                raise ParserParenthesisException(
                    "Error! Missing open parenthesis after print"
                )
        elif self.current_token.type == TokenType.LEFT_PAREN:
            self.next_token()
            inner_expression = self.parse_equality()
            if self.current_token.type == TokenType.RIGHT_PAREN:
                self.next_token()
                return inner_expression
            else:
                raise ParserParenthesisException("Error! Missing closing parenthesis.")
        else:
            raise ParserException(
                f"Error! Unexpected invalid input: {self.current_token.value} of type {self.current_token.type}"
            )
