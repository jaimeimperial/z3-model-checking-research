from z3 import *

class frameClass:
    def __init__(self, cur_var_list, nxt_var_list):
        self.frames = []
        self.cur_var_list = cur_var_list
        self.cur_state_dict = {}
        self.nxt_var_list = nxt_var_list
        self.nxt_state_dict = {}
        self.solver = Solver()
    
    # Function that compares if cur_state_dict is equivalent to nxt_state_dict and merges if not and does nothing if eq
    def frameCompare(self, frames, cur_var_list, cur_state_dict, nxt_var_list, nxt_state_dict):
    #TODO: check if cur_state_dict is equivalent to nxt_state_dict for each variable
    #TODO: if equivalent, break
    #TODO: otherwise, convert nxt_state_dict to cur_state_dict, add cur_state_dict into the frame list and repeat.
        while True:
            frame_eq = True
            new_state_dict = {}
            
            # Compares each respective variable in cur_state_dict and nxt_state_dict. If != breaks loop and frame_eq is false
            for cur_var, nxt_var in zip(cur_var_list, nxt_var_list):
                if cur_state_dict[cur_var] != nxt_state_dict[nxt_var]:
                    frame_eq = False
                    break
            
            # Breaks if cur_state_dict and nxt_state_dict are equal
            if frame_eq:
                break
            
            # Makes makes cur_state_dict eq to new_state_dict and adds cur_state_dict to frames list
            new_state_dict[cur_var] = self.nxt_state_dict[nxt_var]
            cur_state_dict = new_state_dict
            frames.append(cur_state_dict)

        
    def getNextFrame(self, solver, cur_var_list, cur_state_dict, nxt_var_list, nxt_state_dict):
        cur_state = True
        for cur_var in cur_var_list:
            (cur_min_val, cur_max_val) = cur_state_dict[cur_var]
            cur_state = And(cur_state, cur_var >= cur_min_val, cur_var <= cur_max_val)

        if solver.check(cur_state) == sat:
            m = solver.model()

            for cur_var, nxt_var in zip(cur_var_list, nxt_var_list):
                nxt_val = m[nxt_var].as_long()
                cur_min_val, cur_max_val = self.cur_state_dict[cur_var]
                
                self.nxt_state_dict[nxt_var] = (min(nxt_val, cur_min_val), max(cur_max_val, nxt_val))

        return self.nxt_state_dict