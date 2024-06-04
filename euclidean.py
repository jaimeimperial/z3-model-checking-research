from z3 import *
from model_check import FrameClass

# Euclidean Algorithm for finding the gcd(a, b)

a = Int('a')
a_next = Int('a_next')
b = Int('b')
b_next = Int('b_next')
pc = Int('pc')
pc_next = Int('pc_next')

# Transition Relation
'''
Algorithm is gcd(a,b) 
'''
transition = Or(
    And(pc == 0, a != 0, a_next == a, b_next == b, pc_next == 1),
    And(pc == 1, a_next == b % a, b_next == a, b == b, pc_next == 0),
    And(pc == 0, a == 0, a_next == a, b_next == b, b == b, pc_next == pc)
)

frameClass1 = FrameClass([a, b, pc],[a_next, b_next, pc_next])

frameClass1.solver.add(And(a >= -1, a <= 15))
frameClass1.solver.add(And(a_next >= -1, a_next <= 15))
frameClass1.solver.add(And(b >= -1, b <= 15))
frameClass1.solver.add(And(b_next >= -1, b_next <= 15))

frameClass1.solver.add(transition)

cur_frame = {a : (0,0),
            b : (0,0),
            pc : (0,0),
            }

frameClass1.AddFrame(cur_frame)
frameClass1.AddProperty(And(a >= 0))
frameClass1.DoReachability()