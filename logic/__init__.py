from logic.operator import Operator
from logic.quantifier import Quantifier
from logic.constant import Constant
from logic.function import Function
from logic.operator._not import Not
from logic.operator._and import And
from logic.operator._or import Or
from logic.operator.implication import Implication
from logic.operator.xnor import Xnor
from logic.operator.xor import Xor
from logic.predicate import Predicate
from logic.quantifier.existential import ExistentialQuantifier
from logic.quantifier.universal import UniversalQuantifier
from logic.variable import Variable
from stack import Stack

class Logic:
    @staticmethod
    def buildFormula(rpn):
        stack = Stack()
        entities = [Constant, Function, Not, And, Or, Implication,
                    Xnor, Xor, Predicate, ExistentialQuantifier,
                    UniversalQuantifier, Variable]
        for element in rpn:
            for entity in entities:
                if entity.test(element):
                    # put to stack if Variable or Constant
                    if entity in [Variable, Constant]:
                        stack.push(entity(element))
                    else:
                        if entity in [Predicate, Function]:
                            numberOfArguments = entity.calculateNumberOfArugments(element)
                            args = stack.pop(numberOfArguments)
                            stack.push(entity(element, args))
                        else:
                            args = stack.pop(entity.numberOfArguments)
                            stack.push(entity(args))
        return stack.stack[0]
