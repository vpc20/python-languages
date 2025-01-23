class Parser:
    def __init__(self, expression):
        self.tokens = expression.replace(" ", "")  # remove all embedded spaces
        self.pos = 0

    def parse(self):
        result = self.expression()
        if self.pos < len(self.tokens):
            raise Exception("Invalid syntax")
        return result

    def expression(self):
        result = self.term()
        while self.pos < len(self.tokens) and self.tokens[self.pos] in ('+', '-'):
            if self.tokens[self.pos] == '+':
                self.pos += 1
                result += self.term()
            elif self.tokens[self.pos] == '-':
                self.pos += 1
                result -= self.term()
        return result

    def term(self):
        result = self.factor()
        while self.pos < len(self.tokens) and self.tokens[self.pos] in ('*', '/'):
            if self.tokens[self.pos] == '*':
                self.pos += 1
                result *= self.factor()
            elif self.tokens[self.pos] == '/':
                self.pos += 1
                result /= self.factor()
        return result

    def factor(self):
        if self.tokens[self.pos] == '(':
            self.pos += 1
            result = self.expression()
            if self.tokens[self.pos] != ')':
                raise Exception("Invalid syntax: unmatched parenthesis")
            self.pos += 1
            return result
        elif self.tokens[self.pos] == '-':
            self.pos += 1
            return -self.number()
        else:
            return self.number()

    def number(self):
        start_pos = self.pos
        while self.pos < len(self.tokens) and self.tokens[self.pos].isdigit():
            self.pos += 1
        if start_pos == self.pos:
            raise Exception("Invalid syntax: expected number")
        return int(self.tokens[start_pos:self.pos])


# Example usage
# parser = Parser("3 + 5 * (2 - 8) / -2")
# parser = Parser("1 + 1")
parser = Parser("(1 + 1) * (2 + 3) / (10 / 5)")
result = parser.parse()
print(result)  # Output: 3.0
