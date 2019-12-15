from semantic import *

# rpn = input().split()
# rpn = 'Z Z p/1 Z p/1 NOT AND FORALL'.split()

# xd = Logic.buildFormula(rpn)

#alpha only formula
# formula = And([Not(Predicate('p', [Constant('a')])), And([Predicate('p', [Constant('a')]), Predicate('p', [Constant('a')])])])


# beta only formula true
# formula = Or([Predicate('p', [Constant('a')]), Predicate('p', [Constant('b')])])

# delta only
# formula = ExistentialQuantifier([Variable('Z'), Predicate('p', [Variable('Z')])])

#gamma
# formula = UniversalQuantifier([Variable('Z'), Predicate('p', [Variable('Z')])])
# formula = ExistentialQuantifier([Variable('y'), UniversalQuantifier([Variable('x'), Implication([Predicate('p', [Variable('y')]), Predicate('p', [Variable('x')])])])])

rpn = input().split()
formula = Logic.buildFormula(rpn)
print(formula)
s = Semantic(formula)
print('SPEŁNIALNA' if s.resolve() else 'NIESPEŁNIALNA')
