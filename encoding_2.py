from z3 import *
from model_check import FrameClass
from encoding_functions import *

x = Int('x')
x_nxt = Int('x_nxt')

# Creates program id (pid) and program counter (pc) and program counter next (pc_next)
pid = Int('pid')
pc1 = Int('pc1')
pc1_nxt = Int('pc1_next')
pc2 = Int('pc2')
pc2_nxt = Int('pc2_next')
pc3 = Int('pc3')
pc3_nxt = Int('pc3_next')

# Increment conditions
inc_transition = And(
    pc2_nxt==pc2,
    pc3_nxt==pc3,
    Or(
        And(pc1 == 0, x < 200, x_nxt == x, pc1_nxt == 1),
        And(pc1 == 1, x_nxt == x+1,  pc1_nxt == 0),
        And(pc1 == 0, x >= 200, x_nxt == x,  pc1_nxt == pc1)),
    )

# Decrement conditions
dec_transition = And(
    pc1_nxt==pc1,
    pc3_nxt==pc3,
    Or(
        And(pc2 == 0, x > 0, x_nxt == x, pc2_nxt == 1),
        And(pc2 == 1, x_nxt == x-1, pc2_nxt == 0),
        And(pc2 == 0, x <= 0, x_nxt == x, pc2_nxt == pc2)),
    )

# Reset conditions
reset_transition = And(
    pc1_nxt==pc1,
    pc2_nxt==pc2,
    Or(
        And(pc3 == 0, x == 200, x_nxt == 0, pc3_nxt == 1),
    )
)


# Creating class called frameClass1 and inserting variables into cur_var_list and nxt_var_list
frameClass1 = FrameClass([x, pid, pc1, pc2, pc3],[x_nxt, pid, pc1_nxt, pc2_nxt, pc3_nxt])

# Define initial state constraints
frameClass1.solver.add(And(x > 0, x <= 200))
frameClass1.solver.add(And(x_nxt >= -10, x_nxt <= 200))

""" if frameClass1.solver.check() == sat:
    print(frameClass1.solver.model())
exit() """

# Adding state transitions to the solver
#frameClass1.solver.add(Or(inc_transition, dec_transition, reset_transition))

cur_frame = {x : (1, 1),
            pid: (1, 3),
            pc1 : (0, 0),
            pc2 : (0, 0),
            pc3: (0, 0),
            }

transitions = [inc_transition, dec_transition, reset_transition]
encoding = Compose(pid, transitions)
frameClass1.solver.add(encoding)
print(frameClass1.solver)


frameClass1.AddFrame(cur_frame)
frameClass1.AddProperty(And(x_nxt >= 0, x_nxt <= 200))
frameClass1.DoReachability()
#print(frameClass1.solver)