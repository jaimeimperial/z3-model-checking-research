from z3 import *

class FrameClass:
    def __init__(self, cur_var_list, nxt_var_list):
        self.frames = []
        self.cur_var_list = cur_var_list
        self.cur_state_dict = {}
        self.nxt_var_list = nxt_var_list
        self.nxt_state_dict = {}
        self.property = None
        self.solver = Solver()

    def AddZ3constr(self, constr):
        self.solver.add(constr)

    def AddFrame(self, init_frame):
        self.cur_state_dict = init_frame
        self.frames.append(init_frame)

    def AddProperty(self, prop):
        self.property = prop

    def CheckProperty(self, cur_frame):
        #TODO: check if self.property holds true in cur_frame. If not, return false
        # Add constraints for cur_frame to the solver
        self.solver.push()
        try:
            # Add the current frame's constraints to the solver 
            for var, (min_val, max_val) in cur_frame.items():
                self.solver.add(var >= min_val, var <= max_val)

            # Check if the property holds within these constraints
            if self.solver.check(self.property) == sat:
                return False 
            else:
                return True
        finally:
            self.solver.pop()

    def DoReachability(self):
        if self.CheckProperty(self.frames[-1]) is False:
            return
        while True:
            cur_frame = self.frames[-1]
            nxt_frame = self.GetNextFrame(cur_frame)
            if self.CheckFrameEqual(cur_frame, nxt_frame):
                return

            cur_frame = self.rename_frame(nxt_frame)
            if self.CheckProperty( self.frames[-1]) is False:
                return
            self.AddFrame(cur_frame)
        return


    def CheckFrameEqual(self, cur_frame, nxt_frame):
        frame_eq = True
        # Compares each respective variable in cur_state_dict and nxt_state_dict. If != breaks loop and frame_eq is false
        for cur_var, nxt_var in zip(self.cur_var_list, self.nxt_var_list):
            if cur_frame[cur_var] != nxt_frame[nxt_var]:
                return False
        return True

    def RenameFrame(self, nxt_frame):
        new_state_dict = {}
        for cur_var, nxt_var in zip(self.cur_var_list, self.nxt_var_list):
            new_state_dict[cur_var] = nxt_frame[nxt_var]
        self.frames.append(new_state_dict)
        return new_state_dict


    def GetNextFrame(self, cur_frame):
        cur_state = True
        for cur_var in self.cur_var_list:
            (cur_min_val, cur_max_val) = cur_frame[cur_var]
            cur_state = And(cur_state, cur_var >= cur_min_val, cur_var <= cur_max_val)

        if self.solver.check(cur_state) == sat:
            m = self.solver.model()

            for cur_var, nxt_var in zip(self.cur_var_list, self.nxt_var_list):
                nxt_val = m[nxt_var].as_long()
                cur_min_val, cur_max_val = cur_frame[cur_var]

                self.nxt_state_dict[nxt_var] = (min(nxt_val, cur_min_val), max(cur_max_val, nxt_val))

        return self.nxt_state_dict