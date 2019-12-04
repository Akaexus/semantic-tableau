import re
class Function():
    arguments = []
    numberOfArguments = 0
    name = "f"

    def __init__(self, expression, arguments):
        self.name = expression[0]
        self.arguments = arguments
        self.numberOfArguments = len(arguments)

    def __repr__(self):
        return ("{}(" + ', '.join(["{}"]*self.numberOfArguments) + ")").format(self.name, *self.arguments)

    def __str__(self):
        return self.__repr__()

    @staticmethod
    def test(expression):
        pattern = re.compile('^\\w/\\d+$')
        if pattern.match(expression):
            if 'f' <= expression[0] <= 'n':
                return True
            else:
                return False
        else:
            return False

    @staticmethod
    def calculateNumberOfArugments(expression):
        return int(expression[2::])