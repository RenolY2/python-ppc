from .common import *

class CompareImmediate(Instruction):
    def __init__(self, val):
        self.opcode, self.BF, self.RA, self.SI = parse_dform(val)
        self.SI = sign_extend_short(self.SI)
        self.BF = self.BF >> 2
        
    def execute(self, machine):
        gpr = machine.context.gpr 
        assert self.BF < 8
        
        machine.context.cr.compare(self.BF, to_python_int(gpr[self.RA]), to_python_int(self.SI))
    
    def __str__(self):
        SI = to_python_int(self.SI)
        if self.BF > 0:
            return "cmpwi cr{0}, r{1}, {2}".format(self.BF, self.RA, self.SI)
        else:
            return "cmpwi r{1}, {2}".format(self.BF, self.RA, self.SI)


class CompareLogicalImmediate(Instruction):
    def __init__(self, val):
        self.opcode, self.BF, self.RA, self.SI = parse_dform(val)
        self.SI = sign_extend_short(self.SI)
        self.BF = self.BF >> 2
        
    def execute(self, machine):
        gpr = machine.context.gpr 
        assert self.BF < 8
        
        machine.context.cr.compare(self.BF, gpr[self.RA], self.SI)
    
    def __str__(self):
        SI = to_python_int(self.SI)
        if self.BF > 0:
            return "cmplwi cr{0}, r{1}, {2}".format(self.BF, self.RA, self.SI)
        else:
            return "cmplwi r{1}, {2}".format(self.BF, self.RA, self.SI)


class Compare(Instruction):
    def __init__(self, val):
        self.opcode, self.BF, self.RA, self.RB, self.opcode2, _ = parse_xform(val)
        self.BF = self.BF >> 2
        
    def execute(self, machine):
        gpr = machine.context.gpr 
        assert self.BF < 8
        
        machine.context.cr.compare(self.BF, to_python_int(gpr[self.RA]), to_python_int(gpr[self.RB]))
    
    def __str__(self):
        SI = to_python_int(self.SI)
        if self.BF > 0:
            return "cmpw cr{0}, r{1}, r{2}".format(self.BF, self.RA, self.RB)
        else:
            return "cmpw r{1}, r{2}".format(self.BF, self.RA, self.RB)
            

class CompareLogical(Instruction):
    def __init__(self, val):
        self.opcode, self.BF, self.RA, self.RB, self.opcode2, _ = parse_xform(val)
        self.BF = self.BF >> 2
        
    def execute(self, machine):
        gpr = machine.context.gpr 
        assert self.BF < 8
        
        machine.context.cr.compare(self.BF, gpr[self.RA], gpr[self.RB])
    
    def __str__(self):
        SI = to_python_int(self.SI)
        if self.BF > 0:
            return "cmpw cr{0}, r{1}, r{2}".format(self.BF, self.RA, self.RB)
        else:
            return "cmpw r{1}, r{2}".format(self.BF, self.RA, self.RB)