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
NUMBER, STRING, TRUE, FALSE, NIL, PLUS, MINUS, STAR, SLASH, \
    EQUAL_EQUAL, BANG_EQUAL, LESS, LESS_EQUAL, GREATER, GREATER_EQUAL, \
    BANG, LEFT_PAREN, RIGHT_PAREN, IDENTIFIER, EOF = (
    'NUMBER', 'STRING', 'TRUE', 'FALSE', 'NIL', 'PLUS', 'MINUS', 'STAR', 'SLASH',
    'EQUAL_EQUAL', 'BANG_EQUAL', 'LESS', 'LESS_EQUAL', 'GREATER', 'GREATER_EQUAL',
    'BANG', 'LEFT_PAREN', 'RIGHT_PAREN', 'IDENTIFIER', 'EOF'
)

single_char_tokens = {'(': 'LEFT_PAREN',
                      ')': 'RIGHT_PAREN',
                      '{': 'LEFT_BRACE',
                      '}': 'RIGHT_BRACE',
                      '*': 'STAR',
                      '.': 'DOT',
                      ',': 'COMMA',
                      '+': 'PLUS',
                      '-': 'MINUS',
                      ';': 'SEMICOLON'}

slash_token = {'/': 'SLASH'}

one_or_two_char_tokens = {'<': 'LESS',
                          '>': 'GREATER',
                          '=': 'EQUAL',
                          '!': 'BANG'}
double_char_tokens = {'==': 'EQUAL_EQUAL',
                      '!=': 'BANG_EQUAL',
                      '<=': 'LESS_EQUAL',
                      '>=': 'GREATER_EQUAL'}

keyword_tokens = {'and': 'AND',
                  'class': 'CLASS',
                  'else': 'ELSE',
                  'false': 'FALSE',
                  'for': 'FOR',
                  'fun': 'FUN',
                  'if': 'IF',
                  'nil': 'NIL',
                  'or': 'OR',
                  'print': 'PRINT',
                  'return': 'RETURN',
                  'super': 'SUPER',
                  'this': 'THIS',
                  'true': 'TRUE',
                  'var': 'VAR',
                  'while': 'WHILE'}


# Token class
class Token:
    def __init__(self, type, lexeme, literal, line):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __repr__(self):
        return f"Token({self.type}, {self.lexeme})"


class Lexer:
    def __init__(self, text, print_flag=True):
        text = str(text)
        self.text = text
        self.print_flag = print_flag
        self.pos = 0
        self.char = None if len(text) == 0 else text[self.pos]
        self.line_num = 1
        self.tokens = []
        self.exit_code = 0

    def advance(self):
        self.pos += 1
        if self.pos < len(self.text):
            self.char = self.text[self.pos]
        else:
            self.char = None

    def format_number(self, token):
        if '.' in token:
            literal_val = token.rstrip('0')
            if literal_val[-1] == '.':
                literal_val += '0'
            return Token('NUMBER', token, literal_val, self.line_num)
        else:
            return Token('NUMBER', token, token + '.0', self.line_num)

    def scan_one_or_two_char(self):
        next_char = None
        if self.pos + 1 >= len(self.text):  # end of text
            self.tokens.append(Token(one_or_two_char_tokens[self.char], self.char, 'null', self.line_num))
            return
        else:
            next_char = self.text[self.pos + 1]
        if next_char == '=':
            double_char = self.char + next_char
            self.tokens.append(Token(double_char_tokens[double_char], double_char, 'null', self.line_num))
            self.advance()
        else:
            # if next_char is not None and next_char != '\n':
            self.tokens.append(Token(one_or_two_char_tokens[self.char], self.char, 'null', self.line_num))

    def scan_slash_or_double_slash(self):
        # next_char = None
        if self.pos + 1 >= len(self.text):  # end of text
            self.tokens.append(Token(slash_token[self.char], self.char, 'null', self.line_num))
            return
        else:
            next_char = self.text[self.pos + 1]
        if next_char == '/':
            while self.char and self.char != '\n':
                self.advance()
            self.line_num += 1
        else:
            self.tokens.append(Token(slash_token[self.char], self.char, 'null', self.line_num))

    def scan_strings(self):
        token = ''
        while True:
            self.advance()
            if not self.char or self.char == '\n':
                print(f'[line {self.line_num}] Error: Unterminated string.', file=sys.stderr)
                self.exit_code = 65
                self.line_num += 1
                break
            if self.char == '"':
                self.tokens.append(Token("STRING", '"' + token + '"', token, self.line_num))
                break
            token += self.char

    def scan_numbers(self):
        token = ''
        while self.char is not None and self.char.isdigit():
            token += self.char
            self.advance()
        if self.char is None or self.char == '\n':
            self.tokens.append(self.format_number(token))
            self.line_num += 1
        elif self.char == '.':
            self.advance()
            if self.char is None or self.char == '\n' or not self.char.isdigit():
                self.tokens.append(self.format_number(token))
                self.tokens.append(Token(single_char_tokens[self.char], self.char, 'null', self.line_num))
                if self.char == '\n':
                    self.line_num += 1
            else:
                token2 = ''
                while self.char is not None and self.char.isdigit():
                    token2 += self.char
                    self.advance()
                self.tokens.append(self.format_number(token + '.' + token2))
                if self.char == '\n':
                    self.line_num += 1
                self.pos -= 1  # so character will not be skipped
        else:
            self.tokens.append(self.format_number(token))
            self.pos -= 1  # so character will not be skipped

    def scan_identifier_or_keyword(self):
        token = ''
        while self.char is not None and (self.char.isalpha() or self.char.isdigit() or self.char == '_'):
            token += self.char
            self.advance()
        if token in keyword_tokens:
            self.tokens.append(Token(keyword_tokens[token], token, 'null', self.line_num))
        else:
            self.tokens.append(Token('IDENTIFIER', token, 'null', self.line_num))
        self.pos -= 1  # so that current char will not be bypassed

    def scan_tokens(self):
        while self.char is not None:
            if self.char == '\n':
                self.line_num += 1
            elif self.char in single_char_tokens:
                self.tokens.append(Token(single_char_tokens[self.char], self.char, 'null', self.line_num))
            elif self.char in one_or_two_char_tokens:  # could be =, !, <, >, ==, !=, <=, >=
                self.scan_one_or_two_char()
            elif self.char == '/':  # either / or // (comments)
                self.scan_slash_or_double_slash()
            elif self.char == '"':  # string literals enclosed in double quotes
                self.scan_strings()
            elif self.char.isdigit():  # numbers
                self.scan_numbers()
            elif self.char.isalpha() or self.char == '_':  # identifiers
                self.scan_identifier_or_keyword()
            elif self.char in ['$', '#', '@', '%']:
                print(f'[line {self.line_num}] Error: Unexpected character: {self.char}', file=sys.stderr)
                self.exit_code = 65
            self.advance()

        self.tokens.append(Token('EOF ', 'null', '', self.line_num))
        if self.print_flag is True:
            for token in self.tokens:
                print(f'{token.type} {token.lexeme} {token.literal}'.strip())
        if self.exit_code != 0:
            exit(self.exit_code)


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
        else:
            # raise Exception(f"Unexpected token: {self.current_token}")
            # print(f"[line {self.current_token.line}] Error at '{self.current_token.lexeme}': Expect expression.")
            self.exit_code = 65
            exit(self.exit_code)

    def expression(self):
        return self.equality()

    def equality(self):
        expr = self.comparison()
        while self.current_token.type in (BANG_EQUAL, EQUAL_EQUAL):
            operator = self.current_token
            self.eat(operator.type)
            right = self.comparison()
            expr = f"({operator.lexeme} {expr} {right})"
        return expr

    def comparison(self):
        expr = self.term()
        while self.current_token.type in (LESS, LESS_EQUAL, GREATER, GREATER_EQUAL):
            operator = self.current_token
            self.eat(operator.type)
            right = self.term()
            expr = f"({operator.lexeme} {expr} {right})"
        return expr

    def term(self):
        expr = self.factor()
        while self.current_token.type in (PLUS, MINUS):
            operator = self.current_token
            self.eat(operator.type)
            right = self.factor()
            if right is None:
                self.exit_code = 65
                exit(self.exit_code)
            else:
                expr = f"({operator.lexeme} {expr} {right})"
        return expr

    def factor(self):
        expr = self.unary()
        while self.current_token.type in (STAR, SLASH):
            operator = self.current_token
            self.eat(operator.type)
            right = self.unary()
            expr = f"({operator.lexeme} {expr} {right})"
        return expr

    def unary(self):
        if self.current_token.type in (BANG, MINUS):
            operator = self.current_token
            self.eat(operator.type)
            right = self.unary()
            return f"({operator.lexeme} {right})"
        return self.primary()

    def primary(self):
        token = self.current_token
        if token.type == NUMBER:
            self.eat(NUMBER)
            return token.literal
        elif token.type == STRING:
            self.eat(STRING)
            return token.literal
        elif token.type == LEFT_PAREN:
            self.eat(LEFT_PAREN)
            expr = self.expression()
            self.eat(RIGHT_PAREN)
            return f"(group {expr})"
        elif token.type in (TRUE, FALSE, NIL):
            self.eat(token.type)
            return token.lexeme
        # else:
        #     raise Exception(f"Unexpected token: {token}")


def main():
    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command not in ('tokenize', 'parse'):
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

    file = open(filename)
    text = file.read()
    lexer = Lexer(text, print_flag=command == 'tokenize')
    lexer.scan_tokens()
    file.close()

    if command == 'parse':
        parser = Parser(lexer.tokens)
        print(parser.expression())


if __name__ == "__main__":
    main()
