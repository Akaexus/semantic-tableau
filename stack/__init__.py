class Stack:
    stack = []

    def push(self, element):
        self.stack.append(element)

    def pop(self, n=1):
        elements = []
        for i in range(n):
            elements.append(self.stack.pop())
        return list(reversed(elements))