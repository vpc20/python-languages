# The production rules of the grammar are stated below:
# expression     → equality ;
# equality       → comparison ( ( "!=" | "==" ) comparison )* ;
# comparison     → term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
# term           → factor ( ( "-" | "+" ) factor )* ;
# factor         → unary ( ( "/" | "*" ) unary )* ;
# unary          → ( "!" | "-" ) unary
#                | primary ;
# primary        → NUMBER | STRING | "true" | "false" | "nil"
#                | "(" expression ")" ;
import sys

# Define token types
# NUMBER, STRING, TRUE, FALSE, NIL, PLUS, MINUS, STAR, SLASH, \
#     EQUAL_EQUAL, BANG_EQUAL, LESS, LESS_EQUAL, GREATER, GREATER_EQUAL, \
#     BANG, LEFT_PAREN, RIGHT_PAREN, IDENTIFIER, EOF = (
#     'NUMBER', 'STRING', 'TRUE', 'FALSE', 'NIL', 'PLUS', 'MINUS', 'STAR', 'SLASH',
#     'EQUAL_EQUAL', 'BANG_EQUAL', 'LESS', 'LESS_EQUAL', 'GREATER', 'GREATER_EQUAL',
#     'BANG', 'LEFT_PAREN', 'RIGHT_PAREN', 'IDENTIFIER', 'EOF')
NUMBER, PLUS, MINUS, STAR, SLASH, \
    LEFT_PAREN, RIGHT_PAREN, END = (
    'NUMBER', 'PLUS', 'MINUS', 'STAR', 'SLASH',
    'LEFT_PAREN', 'RIGHT_PAREN', 'END')

single_char_tokens = {'(': LEFT_PAREN,
                      ')': RIGHT_PAREN,
                      '+': PLUS,
                      '-': MINUS,
                      '*': STAR,
                      '/': SLASH}


# Token class
class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"


class Lexer:
    def __init__(self, text):
        text = str(text)
        self.text = text
        self.pos = 0
        self.char = None if len(text) == 0 else text[self.pos]
        self.tokens = []

    def advance(self):
        self.pos += 1
        if self.pos < len(self.text):
            self.char = self.text[self.pos]
        else:
            self.char = None

    def scan_numbers(self):
        token = ''
        while self.char is not None and self.char != '\n' and self.char.isdigit():
            token += self.char
            self.advance()

        if self.char is None or self.char == '\n' or self.char.isspace() or self.char in single_char_tokens:
            self.tokens.append(Token(NUMBER, float(token)))
            return
        elif self.char == '.':
            self.advance()
            if self.char is None or self.char == '\n' or not self.char.isdigit():
                print(f'Error: Unexpected character: {self.char}', file=sys.stderr)
                exit(1)
            else:
                token2 = ''
                while self.char is not None and self.char != '\n' and self.char.isdigit():
                    token2 += self.char
                    self.advance()
                self.tokens.append(Token(NUMBER, float(token + '.' + token2)))
                self.pos -= 1  # so character will not be skipped
        else:
            print(f'Error: Unexpected character: {self.char}', file=sys.stderr)
            exit(1)

    def scan_tokens(self):
        while self.char is not None and self.char != '\n':
            if self.char is None or self.char == '\n' or self.char.isspace():
                pass
            elif self.char in single_char_tokens:
                self.tokens.append(Token(single_char_tokens[self.char], self.char))
            elif self.char.isdigit():  # numbers
                self.scan_numbers()
            else:
                print(f'Error: Unexpected character: {self.char}', file=sys.stderr)
                exit(1)
            self.advance()
        self.tokens.append(Token(END, None))


class Parser:
    def __init__(self, tokens):
        # self.lexer = lexer
        self.tokens = tokens
        self.token_idx = 0
        self.current_token = self.tokens[self.token_idx]
        self.exit_code = 0

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.token_idx += 1
            self.current_token = self.tokens[self.token_idx]
        # else:
        #     raise Exception(f"Unexpected token: {self.current_token}")
        # print(f"[line {self.current_token.line}] Error at '{self.current_token.lexeme}': Expect expression.")
        # self.exit_code = 65
        # exit(self.exit_code)

    def expression(self):
        return self.term()

    def term(self):
        expr = self.factor()
        while self.current_token.type in (PLUS, MINUS):
            operator = self.current_token
            self.eat(operator.type)
            right = self.factor()
            expr = f"({operator.value} {expr} {right})"
        return expr

    def factor(self):
        expr = self.unary()
        while self.current_token.type in (STAR, SLASH):
            operator = self.current_token
            self.eat(operator.type)
            right = self.unary()
            expr = f"({operator.value} {expr} {right})"
        return expr

    def unary(self):
        if self.current_token.type == MINUS:
            operator = self.current_token
            self.eat(operator.type)
            right = self.unary()
            return f"({operator.value} {right})"
        return self.primary()

    def primary(self):
        token = self.current_token
        if token.type == NUMBER:
            self.eat(NUMBER)
            return token.value
        elif token.type == LEFT_PAREN:
            self.eat(LEFT_PAREN)
            expr = self.expression()
            self.eat(RIGHT_PAREN)
            return f"(group {expr})"
        else:
            raise Exception(f'Unexpected token: ', self.current_token)


def main():
    text = '1 + 1  '
    # text = '(1 + 1)'
    # text = '(1 + 1) * (2 + 3)'
    # text = '(1 + 1) * (2 + (3 - 1) / 5)'
    lexer = Lexer(text)
    lexer.scan_tokens()
    for token in lexer.tokens:
        print(token)

    parser = Parser(lexer.tokens)
    print(parser.expression())


if __name__ == "__main__":
    main()
