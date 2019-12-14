
class Variable:
    letter = None

    def __init__(self, letter):
        self.letter = letter

    def __str__(self):
        return self.letter

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash(self.letter)

    def __eq__(self, other):
        return self.letter == other.letter

    @staticmethod
    def test(expression):
        return len(expression) == 1 and expression.isupper()