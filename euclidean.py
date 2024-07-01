from z3 import *
from model_check import FrameClass
import encoding_functions

'''
Euclidean Algorithm for finding the gcd(a, b)
Algorithm is gcd(a,b)
a and b are positive integers
a >= b

'''
a = Int('a')
a_next = Int('a_next')
b = Int('b')
b_next = Int('b_next')
r = Int('r')
pid = Int('pid')

m = Int('m')
n = Int('n')

# Transition Relation
C = b > 0
a1 = And(r == a % b, a == a, b == b, a_next == b, b_next == r)
a2 = And(a_next == a, b_next == b)

transition = [
    encoding_functions.ITE(C, a1, a2),
]

# transition = [Or(
#     And(pc == 0, a != 0, pc_next == 1),
#     And(pc == 1, a_next == b % a, b_next == a, pc_next == 0),
#     And(pc == 0, a == 0, a_next == a, b_next == b, b == b, pc_next == pc)
# )]

frameClass1 = FrameClass([a, b, pid],[a_next, b_next, pid])


frameClass1.solver.add(And(a > 0, a <= 15))
frameClass1.solver.add(And(a_next > 0, a_next <= 15))
frameClass1.solver.add(And(b > 0, b <= 15))
frameClass1.solver.add(r == a % b)
frameClass1.solver.add(And(b_next >= 0, b_next <= 15))

cur_frame = {a : (12,12),
            b : (10,10),
            pid : (1,1),
            }

frameClass1.AddFrame(cur_frame)
encoding = encoding_functions.Compose(pid, transition)
frameClass1.solver.add(encoding)

print("----------------")
print("ITE Encoding")
print(encoding)
print("----------------")



#frameClass1.AddProperty(And(r == 0, a_next == (m*a) + (n*b)))
frameClass1.DoReachability()
