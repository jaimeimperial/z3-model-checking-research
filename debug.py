from z3 import *
from model_check import FrameClass

x = Int('x')
x_nxt = Int('x_nxt')


pc1 = Int('pc1')
pc1_nxt = Int('pc1_next')

# Creating class called frameClass1 and inserting variables into cur_var_list and nxt_var_list
frameClass1 = FrameClass([x, pc1],[x_nxt, pc1_nxt])

inc_transition = Or(
        And(pc1 == 0, x < 10, x_nxt == x + 1, pc1_nxt == 1),
    )


# Define initial state constraints
frameClass1.solver.add(And(x >= 0, x <= 10))
frameClass1.solver.add(And(x_nxt >= 0, x_nxt <= 10))


# Adding state transitions to the solver
frameClass1.solver.add(inc_transition)

cur_frame = {x : (0, 0),
            pc1 : (0, 0),
            }

frameClass1.AddFrame(cur_frame)
frameClass1.AddProperty(And(x >= 0, x <= 10))
frameClass1.DoReachability()


