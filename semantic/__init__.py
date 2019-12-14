from logic import *
import copy

class Semantic:
    semanticTables = {
        'alfa': [
            {  # not not A
                'test': lambda e: isinstance(e, Not) and isinstance(e.args[0], Not),
                'convert': lambda e: [e.args[0].args[0]]
            }, {  # A and B
                'test': lambda e: isinstance(e, And),
                'convert': lambda e: e.args
            }, {  # not (A or B)
                'test': lambda e: isinstance(e, Not) and isinstance(e.args[0], Or),
                'convert': lambda e: [Not([e.args[0].args[0]]), Not([e.args[0].args[1]])]
            }, {  # not (A impl B)
                'test': lambda e: isinstance(e, Not) and isinstance(e.args[0], Implication),
                'convert': lambda e: [e.args[0].args[0], Not([e.args[0].args[1]])]
            }, {  # not (A xor B)
                'test': lambda e: isinstance(e, Not) and isinstance(e.args[0], Xor),
                'convert': lambda e: [Implication([e.args[0], e.args[0]]), Implication([e.args[0], e.args[0]])]
            }, {  # (A xnor B)
                'test': lambda e: isinstance(e, Xnor),
                'convert': lambda e: [Implication([e.args[0], e.args[0]]), Implication([e.args[0], e.args[0]])]
            }
        ],
        'beta': [
            {  # not (A and B)
                'test': lambda e: isinstance(e, Not) and isinstance(e.args[0], And),
                'convert': lambda e: [Not(e.args[0].args[0]), Not(e.args[0].args[1])]
            }, {  # A or B
                'test': lambda e: isinstance(e, Or),
                'convert': lambda e: e.args
            }, {  # not (A xnor B)
                'test': lambda e: isinstance(e, Not) and isinstance(e.args[0], Xnor),
                'convert': lambda e: [Not(Implication([e.args[0], e.args[1]])), Not(Implication([e.args[1], e.args[0]]))]
            }, {  # A xor B
                'test': lambda e: isinstance(e, Not) and isinstance(e.args[0], Xnor),
                'convert': lambda e: [Not(Implication([e.args[0], e.args[1]])), Not(Implication([e.args[1], e.args[0]]))]
            }
        ],
        'delta': [
            {
                'test': lambda e: isinstance(e, ExistentialQuantifier),
                'convert': lambda e: [e.domain, e.quantifiedExpression]
            }, {
                'test': lambda e: isinstance(e, Not) and isinstance(e.args[0], UniversalQuantifier),
                'convert': lambda e: [e.args[0].domain, e.args[0].quantifiedExpression]
            }
        ]
    }
    formula = None
    constants = []
    availableConstants = []

    def __init__(self, formula, constants = []):
        self.formula = formula
        self.constants = constants

    def generateNextConstant(self):
        return self.availableConstants.pop(0)

    def getConstants(self):
        def grab(f):
            if isinstance(f, Constant):
                return [f]
            elif isinstance(f, Operator) or isinstance(f, Predicate) or isinstance(f, Function):
                consts = []
                for arg in f.args:
                    consts += grab(arg)
                return consts
            elif isinstance(f, Quantifier):
                return grab(f.quantifiedExpression)
            else:
                return []

        constants = set(grab(self.formula))

        for c in map(Constant, map(chr, range(ord('a'), ord('z')))): # generate more constants
            if c not in self.constants:
                self.availableConstants.append(c)
                
        if len(constants) == 0:
            return {self.generateNextConstant()}
        else:
            return constants

    @staticmethod
    def canEndResolving(formula):
        for subformula in formula:
            if not (isinstance(subformula, Predicate) or (isinstance(subformula, Not) and isinstance(subformula.args[0], Predicate))):
                return False
        return True

    @staticmethod
    def resolveFlatStructure(formula):
        for subformula in formula:
            if isinstance(subformula, Not):
                if subformula.args[0] in formula:
                    return False
        return True

    @staticmethod
    def changeVariableInFormula(f, variable, constant):
        if isinstance(f, Quantifier):
            return Semantic.changeVariableInFormula(f.quantifiedExpression, variable, constant)
        elif isinstance(f, Operator) or isinstance(f, Function) or isinstance(f, Predicate):
            f.args = list(map(lambda arg: Semantic.changeVariableInFormula(arg, variable, constant), f.args))
            return f
        elif isinstance(f, Variable) and f == variable:
            return constant



    def resolve(self):
        constants = self.constants if len(self.constants) else self.getConstants()
        formulas = [self.formula]

        while not self.canEndResolving(formulas):
            for index, subformula in enumerate(formulas):
                # alfa
                for case in self.semanticTables['alfa']:
                    if (case['test'])(subformula):
                        newSubformulas = (case['convert'])(formulas.pop(index))
                        formulas.extend(newSubformulas)
                        break

                # beta
                for case in self.semanticTables['beta']:
                    if (case['test'])(subformula):
                        newSubformulas = (case['convert'])(formulas.pop(index))
                        aFormula = copy.deepcopy(formulas)
                        aFormula.insert(index, newSubformulas[0])
                        a = Semantic(aFormula[0], copy.deepcopy(constants))

                        bFormula = copy.deepcopy(formulas)
                        bFormula.insert(index, newSubformulas[1])
                        b = Semantic(bFormula[0], copy.deepcopy(constants))
                        return a.resolve() or b.resolve()
                # delta

                for case in self.semanticTables['delta']:
                    if (case['test'])(subformula):
                        variable, quantifiedExpression = (case['convert'])(subformula)
                        newConst = self.generateNextConstant()
                        constants.add(newConst)
                        formulas[index] = Semantic.changeVariableInFormula(subformula, variable, newConst)
                print(formulas, constants)
        return self.resolveFlatStructure(formulas)
