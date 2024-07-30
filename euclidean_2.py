from z3 import *
from model_check import FrameClass
import encoding_functions

'''
Euclidean Algorithm for finding the gcd(a, b)
Algorithm is gcd(a,b)
r = a % b
a = b
b = r
'''
a = Int('a')
a_next = Int('a_next')
b = Int('b')
r = Int('r')
c = Int('c')
b_next = Int('b_next')
pc = Int('pc')
pc_next = Int('pc_next')
pid = Int('pid')

m = Int('m')
n = Int('n')

# Transition Relation
# C = b > 0
# a1 = r == a % b, a_next == b, b_next == r, pc_next == 0
# a2 = a_next == a, b_next == b, pc_next == 0
#transition = [encoding_functions.ITE(a != 0, [pc, pc_next], a_next == b % a, And(a_next == a, b_next == a))]
transition = [Or(
    And(pc == 0, b != 0, pc_next == 1),
    And(pc == 1, r == a % b, a_next == b, b_next == r, pc_next == 0),
    And(pc == 0, b == 0, pc_next == 2),
    And(pc == 2, a_next == a, b_next == b, pc_next == 2),
)]

frameClass1 = FrameClass([a, b, pid, pc],[a_next, b_next, pid, pc_next])

frameClass1.solver.add(And(a > 0, a <= 15))
frameClass1.solver.add(And(a_next > 0, a_next <= 15))
frameClass1.solver.add(And(b > 0, b <= 15))
frameClass1.solver.add(And(b_next > 0, b_next <= 15))
frameClass1.solver.add(And(c > 0, c <= b_next))


cur_frame = {a : (15,15),
            b : (15,15),
            pid : (1,1),
            pc : (0,0),
            }

frameClass1.AddFrame(cur_frame)

'''
property: gcd(a,b) = d, a/d = 1 and b/d = 1
'''

print("----------------")
print("Normal Encoding")
encoding = encoding_functions.Compose(pid, transition)
frameClass1.solver.add(encoding)
print(simplify(encoding))
print("----------------")

frameClass1.AddProperty(Not(And(r == 0, b_next == 0, a_next == (m*a) + (n*b), m > 0, n > 0, b > 0, c == (m*a) + (n*b), 0 == c % a_next)))

frameClass1.DoReachability()
