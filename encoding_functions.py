from z3 import *

'''

ITE (condition C, action a1, action a2):
C, a1, a2

If C is true, action a1 occurs.
If C is false, action a2 occurs.
Outputs the encoding of the above action

'''
def ITE(C, a1, a2):
    encoding = And(Implies(C, a1), Implies(Not(C), a2))
    return simplify(encoding)


def Compose(pid, encoding_list):
    size = len(encoding_list)
    composition = None
    for index in range(size):
        if composition == None:
            composition = And(pid == index + 1, encoding_list[index])
        composition = Or(composition, And(pid == index + 1, encoding_list[index]))
    composition = And(pid >= 1, pid <= size, composition) 
    return simplify(composition)

