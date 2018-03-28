
class Element:
    def bracket(self, outer_precedence):
        if self.precedence() < outer_precedence:
            return '(' + str(self) + ')'
        else:
            return str(self)

    def precedence(self):
        pass

    def __repr__(self):
        return '/' + str(self) + '/' 


class Empty(Element):
    def __str__(self):
        return ""

    def precedence(self):
        return 3

class Literal(Element):
    def __init__(self, char):
        self.char = char

    def __str__(self):
        return self.char

    def precedence(self):
        return 3

class Concatenate(Element):
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def __str__(self):
        return str(self.first.bracket(self.precedence())) + \
            str(self.second.bracket(self.precedence()))

    def precedence(self):
        return 1

class Choose(Element):
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def __str__(self):
        return str(self.first.bracket(self.precedence())) + '|' + \
            str(self.second.bracket(self.precedence()))

    def precedence(self):
        return 0

class Repeat(Element):
    def __init__(self, pattern):
        self.pattern = pattern

    def __str__(self):
        return str(self.pattern.bracket(self.precedence())) + '*'

    def precedence(self):
        return 2

# test pattern
exp = Repeat(Choose(Concatenate(Literal('a'), Literal('b')), 
    Literal('c')))
exp
print(exp)
