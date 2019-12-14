import re

class Predicate:
    args = []
    numberOfArguments = 0
    name = 'p'

    def __init__(self, expression, args):
        self.name = expression[0]
        self.args = args
        self.numberOfArguments = len(args)

    def __repr__(self):
        return ("{}(" + ', '.join(["{}"]*self.numberOfArguments) + ")").format(self.name, *self.args)

    def __str__(self):
        return self.__repr__()

    @staticmethod
    def test(expression):
        pattern = re.compile('^\\w/\\d+$')
        if pattern.match(expression):
            if 'p' <= expression[0] <= 'z':
                return True
            else:
                return False
        else:
            return False

    @staticmethod
    def calculateNumberOfArugments(expression):
        return int(expression[2::])

    def __eq__(self, other):
        if not isinstance(other, Predicate):
            return False
        if self.name != other.name:
            return False
        if self.numberOfArguments != other.numberOfArguments:
            return False
        if self.args != other.args:
            return False
        return True
