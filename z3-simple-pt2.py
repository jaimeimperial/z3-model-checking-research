from z3 import *


# return constraints defined on next state variables
def get_next_state(m, cur_var_list, nxt_var_list):
    print("Model: ", m)
    next_state = {}
    for var in nxt_var_list:
        next_state[var] = m[var]
    return next_state


# declare current state variables
cur_var_list = []
x = Int('x')
cur_var_list.append(x)


# declare next state variables
nxt_var_list = []
x2 = Int('x2')
nxt_var_list.append(x2)


s = Solver()


# create initial state constraints
s.add(x <= 200, 0 <= x)


# create transition relations
inc = And((x < 200), (x2 == x + 1))
dec = And((x > 0), (x2 == x - 1))
res = And((x == 200), (x2 == 0))
s.add(Or(inc, dec, res))




next_state_set = None
count = 0 # For keeping track of index


while s.check() == sat:
    m = s.model()

    # create dict nxt_st using get_next_state
    nxt_st = get_next_state(m, cur_var_list, nxt_var_list)
    nxt_st_z3 = (nxt_var_list[count] == nxt_st[nxt_var_list[count]])

    s.add(Not(nxt_st_z3))

    if next_state_set is None:
        next_state_set = nxt_st_z3
    else:
        next_state_set = Or(next_state_set, nxt_st_z3)