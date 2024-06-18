from z3 import *
from model_check import FrameClass
import encoding_functions

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
    pc2_nxt == pc2,
    pc3_nxt == pc3,
    encoding_functions.ITE(x < 200, [pc1, pc1_nxt], x_nxt == x+1, x_nxt == x, x_nxt == x)
)

# Decrement conditions
dec_transition = And(
    pc1_nxt==pc1,
    pc3_nxt==pc3,
    encoding_functions.ITE(x > 0, [pc2, pc2_nxt], x_nxt == x-1, x_nxt == x, x_nxt == x)
)

# Reset conditions
reset_transition = And(
    pc1_nxt==pc1,
    pc2_nxt==pc2,
    encoding_functions.ITE(And(x == 200, x_nxt == x), [pc3, pc3_nxt], x_nxt == 0, x_nxt == x, x_nxt == x)
)


# Creating class called frameClass1 and inserting variables into cur_var_list and nxt_var_list
frameClass1 = FrameClass([x, pid, pc1, pc2, pc3],[x_nxt, pid, pc1_nxt, pc2_nxt, pc3_nxt])

# Define initial state constraints
frameClass1.solver.add(And(x >= -10, x <= 210))
frameClass1.solver.add(And(x_nxt >= -10, x_nxt <= 210))

""" if frameClass1.solver.check() == sat:
    print(frameClass1.solver.model())
exit() """

# Adding state transitions to the solver
#frameClass1.solver.add(Or(inc_transition, dec_transition, reset_transition))

cur_frame = {x : (0, 0),
            pid: (1, 3),
            pc1 : (0, 0),
            pc2 : (0, 0),
            pc3: (0, 0),
            }

transitions = [inc_transition, dec_transition, reset_transition]
encoding = encoding_functions.Compose(pid, transitions)
frameClass1.solver.add(encoding)
print(frameClass1.solver)


frameClass1.AddFrame(cur_frame)
frameClass1.AddProperty(And(x >= 0, x <= 200))
frameClass1.DoReachability()
#print(frameClass1.solver)