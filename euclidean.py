from z3 import *
from model_check import FrameClass

'''
Euclidean Algorithm for finding the gcd(a, b)
Algorithm is gcd(a,b)
'''
a = Int('a')
a_next = Int('a_next')
b = Int('b')
b_next = Int('b_next')
pc = Int('pc')
pc_next = Int('pc_next')
pid = Int('pid')

flip = Or(
    And(pc == 1)
)

# Transition Relation
transition = [Or(
    And(pc == 0, a != 0, pc_next == 1),
    And(pc == 1, a_next == b % a, b_next == a, pc_next == 0),
    And(pc == 0, a == 0, a_next == a, b_next == b, b == b, pc_next == pc)
)]

frameClass1 = FrameClass([a, b, pid, pc],[a_next, b_next, pid, pc_next])

frameClass1.solver.add(And(a > 0, a <= 15))
frameClass1.solver.add(And(a_next > 0, a_next <= 15))
frameClass1.solver.add(And(b > 0, b <= 15))
frameClass1.solver.add(And(b_next > 0, b_next <= 15))

cur_frame = {a : (0,0),
            b : (0,0),
            pid : (1,1),
            pc : (0,0),
            }

frameClass1.AddFrame(cur_frame)

'''
property: gcd(a,b) = d, a/d = 1 and b/d = 1
'''

encoding = frameClass1.Compose(pid, transition)
frameClass1.solver.add(encoding)
print(frameClass1.solver)


frameClass1.DoReachability()
