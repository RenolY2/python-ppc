from .common import *


class AddImmediate(Instruction):
    def __init__(self, val):
        self.opcode, self.RT, self.RA, self.SI = parse_dform(val)
        self.SI = sign_extend_short(self.SI)
    
    def execute(self, machine):
        gpr = machine.context.gpr 
        
        if self.RA == 0:
            gpr[self.RT] = self.SI 
        else:
            gpr[self.RT] = add_32bit(gpr[self.RA], self.SI)
    
    def __str__(self):
        SI = to_python_int(self.SI)
        
        if self.RA == 0:
            return "li r{0}, {1}".format(self.RT, SI)
        elif SI < 0:
            return "subi r{0}, r{1}, {2}".format(self.RT, self.RA, -SI)
        else:
            return "addi r{0}, r{1}, {2}".format(self.RT, self.RA, SI)


class AddImmediateShifted(Instruction):
    def __init__(self, val):
        self.opcode, self.RT, self.RA, self.SI = parse_dform(val)
        self.SI = sign_extend_short(self.SI)
    
    def execute(self, machine):
        gpr = machine.context.gpr 
        SI = (self.SI << 16) & 0xFFFFFFFF
        
        if self.RA == 0:
            gpr[self.RT] = SI 
        else:
            gpr[self.RT] = add_32bit(gpr[self.RA], SI)
    
    def __str__(self):
        SI = to_python_int(self.SI)
        
        if self.RA == 0:
            return "lis r{0}, {1}".format(self.RT, self.SI)
        elif SI < 0:
            return "subis r{0}, r{1}, {2}".format(self.RT, self.RA, -SI)
        else:
            return "addis r{0}, r{1}, {2}".format(self.RT, self.RA, SI)


class Add(Instruction):
    def __init__(self, val):
        self.opcode, self.RT, self.RA, self.RB, self.OE, self.opcode2, self.RC = parse_xoform(val)
    
    def execute(self, machine):
        gpr = machine.context.gpr 
        
        gpr[self.RT], ovhappened = add_32bit_overflow(gpr[self.RA], gpr[self.RB])
        
        if self.OE:
            raise RuntimeError("Overflow not supported yet")
        
        if self.RC == 1:
            machine.context.cr.compare(0, to_python_int(gpr[self.RT]), 0)
        
    def __str__(self):
        instruction = "add"
        if self.OE:
            instruction += "o"
        if self.RC:
            instruction += "."
            
        return "{0} r{1}, r{2}, r{3}".format(instruction, self.RT, self.RA, self.RB)


class SubtractFrom(Instruction):
    def __init__(self, val):
        self.opcode, self.RT, self.RA, self.RB, self.OE, self.opcode2, self.RC = parse_xoform(val)
    
    def execute(self, machine):
        gpr = machine.context.gpr 
        
        gpr[self.RT], ovhappened = add_32bit_overflow(negate(gpr[self.RA]), gpr[self.RB])
        
        if self.OE:
            raise RuntimeError("Overflow not supported yet")
        
        if self.RC == 1:
            machine.context.cr.compare(0, to_python_int(gpr[self.RT]), 0)
        
    def __str__(self):
        instruction = "sub"
        if self.OE:
            instruction += "o"
        if self.RC:
            instruction += "."
            
        return "{0} r{1}, r{3}, r{2}".format(instruction, self.RT, self.RA, self.RB)