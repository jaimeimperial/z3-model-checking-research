from z3 import *

'''

ITE (condition C, array PC, action a1, action a2, optional action o1):
C, a1, a2, o1 should be z3 constraints
array pc should consist of list [pc, pc_next]

If C is true, action a1 occurs.
If C is false, action a2 occurs.
Outputs the encoding of the above action

'''
def ITE(C, pc_list, a1, a2, o1 = False):
    pc = pc_list[0]
    pc_next = pc_list[1]
    if o1 == False:
        encoding = Or(
            And(C, pc == 0, pc_next == 1),
            And(pc == 1, a1, pc_next == 0),
            And(Not(C), a2, pc == 0, pc_next == pc),
        )
    else:
        encoding = Or(
            And(C, pc == 0, o1, pc_next == 1),
            And(pc == 1, a1, pc_next == 0),
            And(Not(C), a2, pc == 0, pc_next == pc),
        )
    return simplify(encoding)


def Compose(pid, encoding_list):
    size = len(encoding_list)
    composition = And(1 <= pid, pid <= size)
    for index in range(size):
        composition = And(composition, pid == index + 1, encoding_list[index])
    return composition

