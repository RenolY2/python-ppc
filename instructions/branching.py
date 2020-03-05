from common import *


class Branch(Instruction):
    def __init__(self, val):
        self.opcode, self.target_addr, self.AA, self.LK = parse_iform(val)
        self.target_addr = sign_extend_24bit(self.target_addr)
        
    def execute(self, machine):
        pc = machine.context.pc 
        
        if self.AA:
            # Absolute address 
            machine.goto(self.target_addr)
        else:
            # Relative address 
            machine.goto(add_32bit(pc, self.target_addr))
        
        if self.LK:
            # Update LR register
            machine.context.lr = pc+4
    
    def __str__(self):
        opcodes = [["b", "bl"], ["ba", "bla"]]

        return "{0} {1}".format(opcodes[self.AA][self.LK], self.target_addr)
        

BO1 = 0b00001
BO2 = 0b00010
BO3 = 0b00100
BO4 = 0b01000
BO5 = 0b10000

def BranchConditional(Instruction):
    def __init__(self, val):
        self.opcode, self.BO, self.BI, self.target_addr, self.AA, self.LK = parse_bform(val)
        self.target_addr = sign_extend_short(self.target_addr)
    
    def execute(self, machine):
        pc = machine.context.pc 
        creg = (self.BI // 4)
        crbit = self.BI % 4
    
        decrement_ctr = not self.BO & BO3 
        
        if decrement_ctr:
            branch_on_zero = self.BO & BO2 
            
        if decrement_ctr:
            machine.decrement_ctr()
            
        cond_ok = self.BO & BO5 | ((self.BO & BO4) ^ not (machine.context.cr[creg] & (1 << (3-crbit)))
        ctr_ok = self.BO & BO3 | (machine.context.ctr != 0) ^ branch_on_zero
        
        if cond_ok and ctr_ok:
            if self.AA:
                # Absolute address 
                target = self.target_addr 
            else:
                # Relative address 
                target = add_32bit(pc, self.target_addr)
            
            
            machine.goto(target)
        
        if self.LK:
            # Update LR register
            machine.context.lr = pc+4
        