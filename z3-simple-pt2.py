from z3 import *

def getStateSpace(s, x, x2, cur_next_dict):
    # Variables to track the minimum and maximum values of x2 found so far
    min_val = float('inf')  # Initialize to positive infinity
    max_val = float('-inf') # Initialize to negative infinity

    # Main loop to dynamically adjust bounds based on found values
    iterations = 0
    max_iterations = 1000  # Prevent infinite loops
    while iterations < max_iterations:
        if iterations > 0:  # From the second iteration onwards, add bounds constraints
            s.push()  # Create a new scope for the temporary constraint
            s.add(Or(x2 < min_val, x2 > max_val))  # Add updated bounds constraint

        result = s.check()
        if result == sat:
            m = s.model()
            x2_val = m[x2].as_long()
            cur_next_dict[f"x: {m[x].as_long()}"] = f"x2: {m[x2].as_long()}"
            
            # Update bounds
            min_val = min(min_val, x2_val)
            max_val = max(max_val, x2_val)
            
            # Display updated bounds
            print(f"Iteration {iterations}: Model found with x2 = {x2_val}")
            print(f"Updated bounds are [{min_val}, {max_val}]")
            
            if iterations > 0:  # Pop the temporary bounds constraint after processing
                s.pop()

            iterations += 1
        else:
            if iterations > 0:  # Ensure to pop if the last check added a constraint
                s.pop()
            print("No further solutions found within the defined constraints.")
            break
        #print(s)
    if iterations == max_iterations:
        print("Reached maximum iterations.")


s = Solver()

x = Int('x')
x2 = Int('x2')

# Creates program id (pid) and program counter (pc) and program counter next (pc_next)
pid = Int('pid')
pc = Int('pc')
pc2 = Int('pc_next')

# Makes a dict with x as keys and x2 as values
cur_next_dict = {}

# Define initial state constraints
s.add(And(x >= 0, x <= 200))

# Constrains pID, pc, and pc2
s.add(2 <= pc, 4 >= pc)
s.add(1 <= pid, 3 >= pid)
s.add(2 <= pc2, 4 >= pc2)

# Increment operation conditions
inc_condition = And(pid == 1, pc == 2, x < 200)
# Decrement operation conditions
dec_condition = And(pid == 2, pc == 2, x > 0)
# Reset operation conditions
reset_condition = And(pid == 3, pc == 2, x == 200)  # Assuming reset has a condition to not be 0 for demonstration

# Applying operation using nested if statements
operation_effect = If(inc_condition, x2 == x + 1, If(dec_condition, x2 == x - 1, If(reset_condition, x2 == 0, x2 == x)))

# Ensures pc cycles through 2-4 sequentially
pc_update = If(pc == 4, pc2 == 2, pc2 == pc + 1)

# Adding operation and pc transition conditions to the solver
s.add(operation_effect, pc_update)

# Example of ensuring a specific process id and starting pc
#s.add(Or(x2 == x + 1, x2 == x - 1, And(x == 200, x2 == 0)))

# starting

getStateSpace(s, x, x2, cur_next_dict)

#print(cur_next_dict)