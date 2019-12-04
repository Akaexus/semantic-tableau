class Variable:
    letter = None

    def __init__(self, symbol):
        self.symbol = symbol

    def __str__(self):
        return self.symbol

    def __repr__(self):
        return self.symbol

    @staticmethod
    def test(expression):
        return len(expression) == 1 and expression.isupper()