from logic.constant import Constant

class Variable(Constant):
    @staticmethod
    def test(expression):
        return len(expression) == 1 and expression.isupper()