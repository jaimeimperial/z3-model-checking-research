from z3 import *
from model_check import FrameClass

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
    pid == 1,
    pc2_nxt==pc2,
    pc3_nxt==pc3,
    Or(
        And(pc1 == 0, x < 200, x_nxt == x, pc1_nxt == 1),
        And(pc1 == 1, x_nxt == x+1,  pc1_nxt == 0),
        And(pc1 == 0, x >= 200, x_nxt == x,  pc1_nxt == pc1)),
    )

# Decrement conditions
dec_transition = And(
    pid == 2,
    pc1_nxt==pc1,
    pc3_nxt==pc3,
    Or(
        And(pc2 == 0, x > 0, x_nxt == x, pc2_nxt == 1),
        And(pc2 == 1, x_nxt == x-1, pc2_nxt == 0),
        And(pc2 == 0, x <= 0, x_nxt == x, pc2_nxt == pc2)),
    )

# Reset conditions
reset_transition = And(
    pid == 3,
    pc1_nxt==pc1,
    pc2_nxt==pc2,
    Or(
        And(pc3 == 0, x == 200, x_nxt == x, pc3_nxt == 1),
        And(pc3 == 1, x_nxt == 0, pc3_nxt == 0),
    )
)


# Creating class called frameClass1 and inserting variables into cur_var_list and nxt_var_list
frameClass1 = FrameClass([x, pid, pc1, pc2, pc3],[x_nxt, pid, pc1_nxt, pc2_nxt, pc3_nxt])


# Define initial state constraints
frameClass1.solver.add(pc1 == 0)
frameClass1.solver.add(pc2 == 0)
frameClass1.solver.add(pc3 == 0)
frameClass1.solver.add(And(x >= -10, x <= 210))
frameClass1.solver.add(And(x_nxt >= -10, x_nxt <= 210))
frameClass1.solver.add(1 <= pid, 3 >= pid)


# Adding state transitions to the solver
frameClass1.solver.add(Or(inc_transition, dec_transition, reset_transition))

cur_frame = {x : (0, 0),
            pid: (1, 3),
            pc1 : (0, 0),
            pc2 : (0, 0),
            pc3: (0, 0),
            }

frameClass1.AddFrame(cur_frame)
frameClass1.AddProperty(And(x >= 0, x <= 200))
frameClass1.DoReachability()


