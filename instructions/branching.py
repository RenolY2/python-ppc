from .common import *


class Branch(Instruction):
    def __init__(self, val):
        self.opcode, self.target_addr, self.AA, self.LK = parse_iform(val)
        self.target_addr = (sign_extend_24bit(self.target_addr) * 4) & 0xFFFFFFFF
        
    def execute(self, machine):
        pc = machine.context.pc 
        
        if self.AA:
            # Absolute address 
            machine.goto(self.target_addr)
        else:
            # Relative address 
            machine.goto(add_32bit(pc-4, self.target_addr))
        
        if self.LK:
            # Update LR register
            machine.context.lr = pc+4
    
    def __str__(self):
        opcodes = [["b", "bl"], ["ba", "bla"]]

        return "{0} {1}".format(opcodes[self.AA][self.LK], self.target_addr)
        

BO0 = 0b00001
BO1 = 0b00010
BO2 = 0b00100 # Decrement counter 
BO3 = 0b01000
BO4 = 0b10000

class BranchConditional(Instruction):
    def __init__(self, val):
        self.opcode, self.BO, self.BI, self.target_addr, self.AA, self.LK = parse_bform(val)
        self.target_addr = to_python_int(sign_extend_14bit(self.target_addr))*4
    
    def execute(self, machine):
        pc = machine.context.pc 
        creg = (self.BI // 4)
        crbit = self.BI % 4
        #print(creg, crbit, (machine.context.cr[creg] >> (3-crbit)) & 1)
        #print(self.BO & BO4, self.BO & BO3, self.BO & BO2, self.BO & BO1, self.BO & BO0)
        
        decrement_ctr = not self.BO & BO2 
        branch_on_zero = 0
        
        if not self.BO & BO2: # decrement counter
            machine.decrement_ctr()
        
        cr_bit = (machine.context.cr[creg] >> (3-crbit)) & 1
        
        ctr_ok = (self.BO & BO2) | ((machine.context.ctr != 0) ^ (self.BO & BO3))
        cond_ok = (self.BO & BO0) | ((self.BO & BO1) == cr_bit)
        
        
        if cond_ok and ctr_ok:
            if self.AA:
                # Absolute address 
                target = self.target_addr 
            else:
                # Relative address 
                target = add_32bit(pc-4, self.target_addr)
            
            print("yes we did jump")
            machine.goto(target)
        
        if self.LK:
            # Update LR register
            machine.context.lr = pc+4
    
    def __str__(self):
        instruction = "bc"
        if self.LK:
            instruction += "l"
        if self.AA:
            instruction += "a"
        
        return "{0} {1}, {2}, {3}".format(instruction, self.BO, self.BI, self.target_addr)
        
        
class BranchConditionalToLR(Instruction):
    def __init__(self, val):
        self.opcode, self.BO, self.BI, self.BH, self.opcode2, self.LK = parse_bform(val)
        self.BH = self.BH & 0b11
    
    def execute(self, machine):
        pc = machine.context.pc 
        creg = (self.BI // 4)
        crbit = self.BI % 4
        #print(creg, crbit, (machine.context.cr[creg] >> (3-crbit)) & 1)
        #print(self.BO & BO4, self.BO & BO3, self.BO & BO2, self.BO & BO1, self.BO & BO0)
        
        decrement_ctr = not self.BO & BO2 
        branch_on_zero = 0
        
        if not self.BO & BO2: # decrement counter
            machine.decrement_ctr()
        
        cr_bit = (machine.context.cr[creg] >> (3-crbit)) & 1
        
        ctr_ok = (self.BO & BO2) | ((machine.context.ctr != 0) ^ (self.BO & BO3))
        cond_ok = (self.BO & BO0) | ((self.BO & BO1) == cr_bit)
        
        
        if cond_ok and ctr_ok:
            target = machine.context.lr
            

            machine.goto(target)
        
        if self.LK:
            # Update LR register
            machine.context.lr = pc+4
    
    def __str__(self):
        instruction = "bclr"
        if self.LK:
            instruction += "l"
        
        return "{0} {1}, {2}, {3}".format(instruction, self.BO, self.BI, self.BH)