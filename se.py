from semantic import *

# rpn = input().split()
# rpn = 'Z Z p/1 Z p/1 NOT AND FORALL'.split()

# xd = Logic.buildFormula(rpn)

#alpha only formula
formula = And([Not(Predicate('p', [Constant('a')])), And([Predicate('p', [Constant('a')]), Predicate('p', [Constant('a')])])])


# beta only formula true
# formula = Or([Predicate('p', [Constant('a')]), Predicate('p', [Constant('b')])])
s = Semantic(formula)
print(s.resolve())
