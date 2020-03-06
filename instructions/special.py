from .common import *

class MoveToSPR(Instruction):
    def __init__(self, val):
        self.opcode, self.RS, self.SPR, self.opcode2 = parse_dform(val)
        print(self.SPR)
        #half = self.SPR & 0b11111
        #self.SPR = self.SPR >> 5 | (half << 5)
        
    def execute(self, machine):
        gpr = machine.context.gpr 
        
        if self.SPR == 1:
            machine.context.xer.from_value(gpr[self.RS])
        elif self.SPR == 8:
            machine.context.lr = gpr[self.RS]
        elif self.SPR == 9:
            machine.context.ctr = gpr[self.RS]
        else:
            raise RuntimeError("Invalid SPR {0}".format(self.SPR))
    
    def __str__(self):
        if self.SPR == 1:
            return "mtxer r{0}".format(self.RS)
        elif self.SPR == 8:
            return "mtlr r{0}".format(self.RS)
        elif self.SPR == 9:
            return "mtctr r{0}".format(self.RS)
        else:
            return "mtspr {0}, r{1}".format(self.SPR, self.RS)


class MoveFromSPR(Instruction):
    def __init__(self, val):
        self.opcode, self.RT, self.SPR, self.opcode2 = parse_dform(val)
        #half = spr & 0b11111
        #self.SPR = self.SPR >> 5 | (half << 5)
        
    def execute(self, machine):
        gpr = machine.context.gpr 
        
        if self.SPR == 1:
            gpr[self.RT] = machine.context.xer.to_value()
        elif self.SPR == 8:
            gpr[self.RT] = machine.context.lr
        elif self.SPR == 9:
            gpr[self.RT] = machine.context.ctr
        else:
            raise RuntimeError("Invalid SPR {0}".format(self.SPR))
    
    def __str__(self):
        if self.SPR == 1:
            return "mfxer r{0}".format(self.RT)
        elif self.SPR == 8:
            return "mflr r{0}".format(self.RT)
        elif self.SPR == 9:
            return "mfctr r{0}".format(self.RT)
        else:
            return "mfspr {0}, r{1}".format(self.SPR, self.RT)
            
            
class MoveFromCR(Instruction):
    def __init__(self, val):
        self.opcode, self.RT, self.SPR, self.opcode2 = parse_dform(val)
        
    def execute(self, machine):
        gpr = machine.context.gpr 
        gpr[self.RT] = machine.context.cr.to_value()
    
    def __str__(self):
        return "mfcr r{0}".format(self.RT)
        

class MoveToCRFields(Instruction):
    def __init__(self, val):
        self.opcode, self.RS, self.FXM, self.opcode2 = parse_dform(val)
        
    def execute(self, machine):
        gpr = machine.context.gpr 
        machine.context.cr.from_value(gpr[self.RS], self.FXM)
    
    def __str__(self):
        if self.FXM == 0xFF:
            return "mtcr r{0}".format(self.RS)
        else:
            return "mtcrf r{0}".format(self.RS)