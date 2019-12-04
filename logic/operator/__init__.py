class Operator:
    symbols = []
    arguments = []
    numberOfArguments = 2 # for most cases

    def __init__(self, arguments):
        self.arguments = arguments

    def __repr__(self):
        if self.numberOfArguments == 2:
            return "{} {} {}".format(
                self.bracketize(self.arguments[0]),
                self.symbols[0],
                self.bracketize(self.arguments[1])
            )
        else:
            return "{} {}".format(self.symbols[0], self.arguments[0])

    def __str__(self):
        return self.__repr__()

    @staticmethod
    def bracketize(entity):
        if isinstance(entity, Operator):
            return '({})'.format(entity)
        else:
            return entity


    @classmethod
    def test(cls, expression):
        return expression in cls.symbols