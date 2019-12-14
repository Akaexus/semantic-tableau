from semantic import *

# rpn = input().split()
# rpn = 'Z Z p/1 Z p/1 NOT AND FORALL'.split()

# xd = Logic.buildFormula(rpn)

formula = And([Predicate('p', [Constant('a')]), And([Predicate('p', [Constant('a')]), Predicate('p', [Constant('a')])])])
print(formula)

s = Semantic(formula)
print(s.resolve())
