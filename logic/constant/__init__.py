class Constant:
    letter = None

    def __init__(self, letter):
        self.letter = letter

    def __str__(self):
        return self.letter

    def __repr__(self):
        return self.letter

    @staticmethod
    def test(expression):
        if len(expression) != 1:
            return False
        letter = expression[0]
        return 'a' <= letter <= 'e'
