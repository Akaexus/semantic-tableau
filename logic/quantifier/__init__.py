from logic.operator import Operator

class Quantifier:
    quantifiedExpression = None
    domain = None
    numberOfArguments = 2
    symbols = []

    def __init__(self, arguments):
        self.domain = arguments[0]
        self.quantifiedExpression = arguments[1]

    def __str__(self):
        return '{} {} {}'.format(self.symbols[0], self.domain, self.bracketize(self.quantifiedExpression))

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def bracketize(entity):
        return Operator.bracketize(entity)

    @classmethod
    def test(cls, expression):
        return expression in cls.symbols
