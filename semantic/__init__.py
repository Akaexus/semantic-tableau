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
                'convert': lambda e: [e.domain, copy.deepcopy(e.quantifiedExpression)]
            }, {
                'test': lambda e: isinstance(e, Not) and isinstance(e.args[0], UniversalQuantifier),
                'convert': lambda e: [e.args[0].domain, list(map(copy.deepcopy,e.args[0].quantifiedExpression))]
            }
        ],
        'gamma': [
            {
                'test': lambda e: isinstance(e, UniversalQuantifier),
                'convert': lambda e: [e.domain, e.quantifiedExpression]
            }, {
                'test': lambda e: isinstance(e, Not) and isinstance(e.args[0], ExistentialQuantifier),
                'convert': lambda e: [e.args[0].domain, e.args[0].quantifiedExpression]
            }
        ]
    }
    formula = None
    constants = []
    availableConstants = []
    gammaUsedConstants = []

    def __init__(self, formula, constants = [], gammaUsedConstants = []):
        self.formula = formula
        self.constants = constants
        self.gammaUsedConstants = gammaUsedConstants

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
    def changeVariableInFormula(x, v, c):
        f = copy.deepcopy(x)
        variable = copy.deepcopy(v)
        constant = copy.deepcopy(c)

        if isinstance(f, Quantifier):
            return Semantic.changeVariableInFormula(f.quantifiedExpression, variable, constant)
        elif isinstance(f, Operator) or isinstance(f, Function) or isinstance(f, Predicate):
            f.args = list(map(lambda argument: Semantic.changeVariableInFormula(argument, variable, constant), f.args))
            return f
        elif isinstance(f, Variable) and f == variable:
            return copy.deepcopy(constant)
        else:
            return f



    def resolve(self):
        if len(self.constants) == 0:
            self.constants = self.getConstants()
        formulas = [self.formula]
        changedAnySubformula = True
        while not self.canEndResolving(formulas) and changedAnySubformula:
            changedAnySubformula = False
            for index, subformula in enumerate(formulas):
                usedAnyTable = False
                # alfa
                for case in self.semanticTables['alfa']:
                    if (case['test'])(subformula):
                        newSubformulas = (case['convert'])(formulas.pop(index))
                        formulas.extend(newSubformulas)
                        usedAnyTable = True
                        changedAnySubformula = True
                        break

                # beta
                for case in self.semanticTables['beta']:
                    if (case['test'])(subformula):
                        newSubformulas = (case['convert'])(formulas.pop(index))
                        aFormula = copy.deepcopy(formulas)
                        aFormula.insert(index, newSubformulas[0])
                        a = Semantic(aFormula[0], copy.deepcopy(self.constants), copy.deepcopy(self.gammaUsedConstants))

                        bFormula = copy.deepcopy(formulas)
                        bFormula.insert(index, newSubformulas[1])
                        b = Semantic(bFormula[0], copy.deepcopy(self.constants), copy.deepcopy(self.gammaUsedConstants))
                        return a.resolve() or b.resolve()

                # delta
                for case in self.semanticTables['delta']:
                    if (case['test'])(subformula):
                        variable, quantifiedExpression = (case['convert'])(subformula)
                        newConst = self.generateNextConstant()
                        self.constants.add(newConst)
                        formulas[index] = Semantic.changeVariableInFormula(subformula, variable, newConst)
                        usedAnyTable = True
                        changedAnySubformula = True
                        break

                # gamma
                if not usedAnyTable and len(self.gammaUsedConstants) != len(self.constants):
                    for case in self.semanticTables['gamma']:
                        if (case['test'])(subformula):
                            variable, quantifiedExpression = (case['convert'])(subformula)
                            uc = None
                            for c in self.constants:
                                if c not in self.gammaUsedConstants:
                                    uc = copy.deepcopy(c)
                                    break
                            if uc:
                                formulas.append(Semantic.changeVariableInFormula(quantifiedExpression, variable, uc))
                                self.gammaUsedConstants.append(uc)
                                changedAnySubformula = True
            print(formulas)
        return self.resolveFlatStructure(formulas)
