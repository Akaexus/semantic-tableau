class Operator:
    symbols = []
    args = []
    numberOfArguments = 2  # for most cases

    def __init__(self, args):
        if isinstance(args, list):
            self.args = args
        else:
            self.args = [args]

    def __repr__(self):
        if self.numberOfArguments == 2:
            return "{} {} {}".format(
                self.bracketize(self.args[0]),
                self.symbols[0],
                self.bracketize(self.args[1])
            )
        else:
            return "{} {}".format(self.symbols[0], self.bracketize(self.args[0]))

    def __str__(self):
        return self.__repr__()

    @staticmethod
    def bracketize(entity):
        if isinstance(entity, Operator) and entity.numberOfArguments > 1:
            return '({})'.format(entity)
        else:
            return entity

    @classmethod
    def test(cls, expression):
        return expression in cls.symbols
