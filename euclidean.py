from z3 import *
from model_check import FrameClass
import encoding_functions

'''
Euclidean Algorithm for finding the gcd(a, b)
Algorithm is gcd(a,b)


property: gcd(a,b) = d, a/d = 1 and b/d = 1

'''
a = Int('a')
a_next = Int('a_next')
b = Int('b')
b_next = Int('b_next')
d = Int('d')
pc1 = Int('pc1')
pc1_next = Int('pc1_next')
pc2 = Int('pc2')
pc2_next = Int('pc2_next')
pid = Int('pid')

# Transition Relation
transition = [
    encoding_functions.ITE(a != 0, [pc1, pc1_next], And(a_next == b % a, b_next == a), And(a_next == a, b_next == b)),
    encoding_functions.ITE(a < b, [pc2, pc2_next], And(b_next == a, a_next == b), And(a_next == a, b_next == b)),
    ]
# transition = [Or(
#     And(pc == 0, a != 0, pc_next == 1),
#     And(pc == 1, a_next == b % a, b_next == a, pc_next == 0),
#     And(pc == 0, a == 0, a_next == a, b_next == b, b == b, pc_next == pc)
# )]

frameClass1 = FrameClass([a, b, pid, pc1, pc2],[a_next, b_next, pid, pc1_next, pc2_next])

frameClass1.solver.add(And(a > 0, a <= 15))
frameClass1.solver.add(And(a_next > 0, a_next <= 15))
frameClass1.solver.add(And(b > 0, b <= 15))
frameClass1.solver.add(d == a%b)
frameClass1.solver.add(And(b_next > 0, b_next <= 15))

cur_frame = {a : (1,1),
            b : (1,1),
            pid : (1,1),
            pc1 : (0,0),
            pc2 : (0,0),
            }

frameClass1.AddFrame(cur_frame)
encoding = encoding_functions.Compose(pid, transition)
frameClass1.solver.add(encoding)

print("----------------")
print("ITE Encoding")
print(encoding)
print("----------------")


frameClass1.AddProperty(And(a/d == 1, b/d == 1))
frameClass1.DoReachability()
