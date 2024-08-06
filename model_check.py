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
        for nxt_var, cur_var in zip(self.nxt_var_list, self.cur_var_list):
            self.nxt_state_dict[nxt_var] = self.cur_state_dict[cur_var]
        self.frames.append(init_frame)

    def AddProperty(self, prop):
        self.property = prop

    def CheckProperty(self, cur_frame):
        #property_solver = Solver()
        if self.property == None:
            print("Error: No Property added")
            return
    
        # create a new Z3 solver instance pcheck
        # create z3 constrints from cur_frame
        # convert provided negated property to Z3 constraint
        # add these constraints to solver pcheck,
        # solve pcheck, if sat, property violate.

        pcheck = Solver()
        pcheck.push()
        # Add the current frame's constraints to the empty solver, pcheck
        for var, (min_val, max_val) in cur_frame.items():
            pcheck.add(var >= min_val, var <= max_val)

        print(cur_frame)
        # Check if the property holds within these constraints
        if pcheck.check(Not(self.property)) == sat:
            print('Property Violation')
            print(pcheck.model())
            pcheck.pop()
            return False
        else:
            print("Property Passed")
            pcheck.pop()
            return True


    def DoReachability(self):
        if self.CheckProperty(self.frames[-1]) is False:
            print('')

        step = 0
        while True:
            print("*** Reachability step = ", step)
            cur_frame = self.frames[-1]
            print(cur_frame)
            nxt_frame = self.GetNextFrame(cur_frame)
            if nxt_frame == {}:
                print("Error: Frame empty - GetNextFrame")
                exit()
            if self.CheckFrameEqual(cur_frame, nxt_frame):
                break
            cur_frame = self.RenameFrame(nxt_frame)
            if self.CheckProperty(cur_frame) is False:
                return
            self.AddFrame(cur_frame)
            print("-----------------")
            step += 1

        return


    def CheckFrameEqual(self, cur_frame, nxt_frame):
        if nxt_frame == {} or cur_frame == {}:
            print("Error: Frame empty - CheckFrameEqual")
            return
        # Compares each respective variable in cur_state_dict and nxt_state_dict. If != breaks loop and frame_eq is false
        for cur_var, nxt_var in zip(self.cur_var_list, self.nxt_var_list):
            if cur_frame[cur_var] != nxt_frame[nxt_var]:
                return False
        print("frames are equal")
        return True

    def RenameFrame(self, nxt_frame):
        if nxt_frame == {}:
            print("Error: Frame empty - RenameFrame")
            return
        new_state_dict = {}
        for cur_var, nxt_var in zip(self.cur_var_list, self.nxt_var_list):
            new_state_dict[cur_var] = nxt_frame[nxt_var]
        self.frames.append(new_state_dict)
        return new_state_dict


    def GetNextFrame(self, cur_frame):
        cur_state = True
        # cur_state is all ranges of vars
        for cur_var in self.cur_var_list:
            (cur_min_val, cur_max_val) = cur_frame[cur_var]
            cur_state = And(cur_state, cur_var >= cur_min_val, cur_var <= cur_max_val)

        # print("----------------")
        # print("Current State: ")
        # print(simplify(cur_state))
        # print("----------------")
    
        # Iteratively call solver on cur_state with nxt_state_z3 blocked until new next state can be found
        nxt_state_dict = {} # initialize it to be the same as the current frame; this function then aims to find new states that are not in the current frame
        nxt_state_z3 = False
        iterations = 0
        # print("----------------")
        # print("Next State Dict")
        # print(self.nxt_state_dict)
        # print("----------------")
        while self.solver.check(cur_state, Not(nxt_state_z3)) == sat:
            m = self.solver.model()
            print("-- model from Z3  ------")
            print(m)
            print("----------------")
        
            for nxt_var in self.nxt_var_list:
                # print(nxt_var)
                # print(self.nxt_state_dict)
                nxt_val = m[nxt_var].as_long()
                if nxt_var in self.nxt_state_dict.keys():
                    # Update min and max values
                    nxt_min_val, nxt_max_val = self.nxt_state_dict[nxt_var]
                    nxt_min_val = min(nxt_val, nxt_min_val)
                    nxt_max_val = max(nxt_val, nxt_max_val)
                    self.nxt_state_dict[nxt_var] = (nxt_min_val, nxt_max_val)
                else:
                    # Initialize min and max values
                    print('here')
                    self.nxt_state_dict[nxt_var] = (nxt_val, nxt_val)
            # print(self.nxt_state_dict)

            # generate Z3 constraint for nxt_state_dict
            nxt_state_z3 = False
            for nxt_var in self.nxt_var_list:
                nxt_min_val, nxt_max_val = self.nxt_state_dict[nxt_var]
                #print(nxt_min_val, '   ', nxt_max_val)
                if nxt_state_z3 == False:
                    nxt_state_z3 = And(nxt_var >= nxt_min_val, nxt_var <= nxt_max_val)
                nxt_state_z3 = And(nxt_state_z3, And(nxt_var >= nxt_min_val, nxt_var <= nxt_max_val))

            # print('----------------------------')
            # print('nxt_state_z3')
            # print(simplify(Not(nxt_state_z3)))
            # print('----------------------------')
        
            """ print(simplify(cur_state))
            print(self.nxt_var_list[0] <0 )
            print(self.solver)
            print(self.solver.check(cur_state, self.nxt_var_list[0] <0)) """

            iterations += 1
            #print(simplify(nxt_state_z3))
            #print('---')
            nxt_state_dict = self.nxt_state_dict
            # print('----------------------------')
            # print("next state dict")
            # print(nxt_state_dict)
            # print('----------------------------')
        return nxt_state_dict