# Grammar for the arithmetic interpreter
# term           → factor ( ( "+" | "-" ) factor )* ;
# factor         → unary ( ( "*" | "/" ) unary )* ;
# unary          → ("-") unary
#                | primary ;
# primary        → "(" term ")"
#                | NUMBER

def calc(equation):
    global tokens, pos
    tokens = equation.replace(" ", "")
    pos = 0

    result = term()
    if pos < len(tokens):
        raise Exception("Invalid syntax")
    return result


def term():
    global tokens, pos
    result = factor()
    while pos < len(tokens) and tokens[pos] in ('+', '-'):
        if tokens[pos] == '+':
            pos += 1
            result += factor()
        elif tokens[pos] == '-':
            pos += 1
            result -= factor()
    return result


def factor():
    global tokens, pos
    result = unary()
    while pos < len(tokens) and tokens[pos] in ('*', '/'):
        if tokens[pos] == '*':
            pos += 1
            result *= unary()
        elif tokens[pos] == '/':
            pos += 1
            result /= unary()
    return result


def unary():
    global tokens, pos
    if tokens[pos] == '-':
        pos += 1
        right = unary()
        return -right
    return primary()


def primary():
    global tokens, pos
    if tokens[pos] == '(':
        pos += 1
        result = term()
        if tokens[pos] != ')':
            raise Exception("Invalid syntax: unmatched parenthesis")
        pos += 1
        return result

    start_pos = pos
    while pos < len(tokens) and tokens[pos].isdigit():
        pos += 1
    if start_pos == pos:
        raise Exception("Invalid syntax: expected number")
    return int(tokens[start_pos:pos])


# equation = "(1 + 1) * (2 + 3) / (10 / 5)"
# equation = "-7 * -(6 / 3)"
# equation = "-73 * 64 * 84 / 31 / -5 - -72 * -36 * -11"

equation = "-80- 49- -82- 58"
# equation = "-80- 49"
# equation = "1 +1"
print(calc(equation))
