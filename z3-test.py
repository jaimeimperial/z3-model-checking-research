from z3 import *

def getStateSpace(s, x, x2):
    # List to track all found values of x2 to ensure new states are explored
    found_values = []

    # Main loop to dynamically adjust search based on found values
    iterations = 0
    max_iterations = 1000  # Limit to prevent infinite loops
    
    while iterations < max_iterations:
        if iterations > 0:  # From the second iteration onwards, avoid previous x2 values
            s.push()  # Create a new scope for the temporary constraint
            # Ensure x2 is not equal to any previously found value
            s.add(Not(x2 in found_values))

        result = s.check()
        if result == sat:
            m = s.model()
            x2_val = m[x2].as_long()
            found_values.append(x2_val)  # Track the found x2 value
            
            # Display found value
            print(f"Iteration {iterations}: Model found with x2 = {x2_val}")
            
            if iterations > 0:  # Pop the temporary constraints after processing
                s.pop()

            iterations += 1
        else:
            if iterations > 0:  # Ensure to pop if the last check added a constraint
                s.pop()
            print("No further solutions found within the defined constraints.")
            break

    if iterations == max_iterations:
        print("Reached maximum iterations.")

s = Solver()
x = Int('x')
x2 = Int('x2')

# Define initial state constraints and add them to the solver
s.add(And(x >= 0, x <= 200))

# Define transition relations and add to solver
inc = And((x < 200), (x2 == x + 1))
dec = And((x > 0), (x2 == x - 1))
reset = And((x == 200), (x2 == 0))

s.add(Or(inc, dec, reset))

getStateSpace(s, x, x2)
