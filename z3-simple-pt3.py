from z3 import *

def getStateSpace(s, x, x_nxt, cur_var_list, nxt_var_list, x_next_dict):
    min_val, max_val = float('inf'), float('-inf')
    iterations, max_iterations = 0, 1000

    while s.check() == sat and iterations < max_iterations:
        m = s.model()
        x_next_val = m[x_nxt].as_long()
        x_val = m[x].as_long()

        # Update lists and dictionary with current model's values
        nxt_var_list.append(x_next_val)
        cur_var_list.append(x_val)
        
        # Changes min_val and max_val depending on x_next
        min_val, max_val = min(min_val, x_next_val), max(max_val, x_next_val)
        
        # Adding x_next as keys with [lower bound, upper bound] as value
        x_next_dict[x_next_val] = f"[{min_val}, {max_val}]"

        # Display x_next, x as well as the bounds
        print(f"x = {x_val}, x_next = {x_next_val}")
        print(f"[{min_val}, {max_val}]")

        # Add bounds constraint to find a new model
        if iterations > 0:
            s.pop()  # Clear previous bounds constraint

        # Pushing new bounds to solver
        s.push()
        s.add(Or(x_nxt < min_val, x_nxt > max_val))

        iterations += 1

    if iterations > 0:  # Clean up the last push if any
        s.pop()
    print("No further states")



s = Solver()

cur_var_list = []
nxt_var_list = []

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

# Makes a dict with x_next as keys and [min, max] as values
x_next_dict = {}

# Define initial state constraints
s.add(And(x >= 0, x <= 200))
s.add(pc1 == 0)
s.add(pc2 == 0)
s.add(pc3 == 0)

# Constrains pID
s.add(1 <= pid, 3 >= pid)

# Increment conditions
inc_transition = And(
    pid == 1,
    pc2_nxt==pc2,
    pc3_nxt==pc3,
    Or(
        And(pc1 == 0, x < 200, x_nxt == x+1, pc1_nxt == pc1),
        And(pc1 == 0, x >= 200, x_nxt == x,  pc1_nxt == pc1)),
    )

# Decrement conditions
dec_transition = And(
    pid == 2,
    pc1_nxt==pc1,
    pc3_nxt==pc3,
    Or(
        And(pc2 == 0, x > 0, x_nxt == x-1, pc2_nxt == pc2),
        And(pc2 == 0, x <= 0, x_nxt == x, pc2_nxt == pc2)),
    )

# Reset conditions
reset_transition = And(
    pid == 3,
    pc1_nxt==pc1,
    pc2_nxt==pc2,
    And(pc3 == 0, x == 200, x_nxt == 0, pc3_nxt == pc3),
    )

# Adding state transitions to the solver
s.add(Or(inc_transition, dec_transition, reset_transition))

getStateSpace(s, x, x_nxt, cur_var_list, nxt_var_list, x_next_dict)
