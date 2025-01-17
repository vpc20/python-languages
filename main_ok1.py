import sys

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


def print_number(token):
    if '.' in token:
        literal_val = token.rstrip('0')
        if literal_val[-1] == '.':
            literal_val += '0'
        print(f'NUMBER {token} {literal_val}')
    else:
        print(f'NUMBER {token} {token}.0')


def lexer(file):
    def scan_one_or_two_char():
        nonlocal char, read_next_char
        while char in one_or_two_char_tokens:
            char2 = file.read(1)
            if char2.isspace():
                continue
            if char2 == '=':
                print(f'{double_char_tokens[char + char2]} {char + char2} null')
                read_next_char = True
                break
            else:
                print(f'{one_or_two_char_tokens[char]} {char} null')
                char = char2
                read_next_char = False

    def scan_slash_or_double_slash():
        nonlocal char, line_num, read_next_char
        char2 = file.read(1)
        if char2 == '/':
            while char and char != '\n':
                char = file.read(1)
            line_num += 1
        else:
            print(f'{slash_token[char]} {char} null')
            char = char2
            read_next_char = False

    def scan_string_literal():
        nonlocal char, exit_code, line_num
        token = ''
        while True:
            char = file.read(1)
            if not char or char == '\n':
                print(f'[line {line_num}] Error: Unterminated string.', file=sys.stderr)
                exit_code = 65
                line_num += 1
                break
            if char == '"':
                print(f'STRING "{token}" {token}')
                break
            token += char

    def scan_numbers():
        nonlocal char, line_num, read_next_char
        token = char
        while char.isdigit():
            char = file.read(1)
            if not char or char == '\n':
                print_number(token)
                line_num += 1
            elif char.isdigit():
                token += char
        if not char or char == '\n':
            return

        if char == '.':
            char = file.read(1)
            if not char or char == '\n' or not char.isdigit():
                print_number(token)
                print(f'{single_char_tokens[char]} {char} null')
                if char == '\n':
                    line_num += 1
            else:
                token2 = char
                while char.isdigit():
                    char = file.read(1)
                    if not char or char == '\n':
                        print_number(token + '.' + token2)
                        line_num += 1
                    elif char.isdigit():
                        token2 += char
                if char and char != '\n':
                    print_number(token + '.' + token2)
                    read_next_char = False
        else:
            print_number(token)
            read_next_char = False

    def scan_identifier_or_keyword():
        nonlocal char, line_num, read_next_char
        token = char
        while char.isalpha() or char == '_' or char.isdigit():
            char = file.read(1)
            if not char or char == '\n':
                line_num += 1
            elif char.isalpha() or char == '_' or char.isdigit():
                token += char
        if token in keyword_tokens:
            print(f'{keyword_tokens[token]} {token} null')
        else:
            print(f'IDENTIFIER {token} null')
        read_next_char = False

    exit_code = 0
    line_num = 1
    read_next_char = True
    char = ''

    while True:
        if read_next_char:
            char = file.read(1)
        read_next_char = True

        if not char:  # end of file
            break

        if char == '\n':
            line_num += 1
        elif char in single_char_tokens:
            print(f'{single_char_tokens[char]} {char} null')
        elif char in one_or_two_char_tokens:  # could be =, !, <, >, ==, !=, <=, >=
            scan_one_or_two_char()
        elif char == '/':  # either / or // (comments)
            scan_slash_or_double_slash()
        elif char == '"':  # string literals enclosed in double quotes
            scan_string_literal()
        elif char.isdigit():  # numbers
            scan_numbers()
        elif char.isalpha() or char == '_':  # identifiers
            scan_identifier_or_keyword()
        elif char in ['$', '#', '@', '%']:
            print(f'[line {line_num}] Error: Unexpected character: {char}', file=sys.stderr)
            exit_code = 65

    print('EOF  null')
    exit(exit_code)


def parser(file):
    pass


def main():
    # if len(sys.argv) < 3:
    #     print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
    #     exit(1)
    #
    # command = sys.argv[1]
    # filename = sys.argv[2]
    #
    # if command != "tokenize":
    #     print(f"Unknown command: {command}", file=sys.stderr)
    #     exit(1)

    # file = open('test.lox')
    file = open('test5.lox')
    lexer(file)
    # parser(file)
    file.close()


if __name__ == "__main__":
    main()
