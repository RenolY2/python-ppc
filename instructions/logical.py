from .common import *


class ORImmediate(Instruction):
    def __init__(self, val):
        self.opcode, self.RS, self.RA, self.UI = parse_dform(val)
        
    def execute(self, machine):
        gpr = machine.context.gpr 
        gpr[self.RA] = (gpr[self.RS] | self.UI ) & 0xFFFFFFFF
        
    def __str__(self):
        if self.RS == self.RA == self.UI:
            return "nop"
        else:
            return "ori r{0}, r{1}, {2}".format(dot, self.RA, self.RS, self.UI)


class ORImmediateShifted(Instruction):
    def __init__(self, val):
        self.opcode, self.RS, self.RA, self.UI = parse_dform(val)
        
    def execute(self, machine):
        gpr = machine.context.gpr 
        gpr[self.RA] = (gpr[self.RS] | (self.UI << 16) ) & 0xFFFFFFFF
        
    def __str__(self):
        return "oris r{0}, r{1}, {2}".format(dot, self.RA, self.RS, self.UI)
            

class OR(Instruction):
    def __init__(self, val):
        self.opcode, self.RS, self.RA, self.RB, self.opcode2, self.RC = parse_xform(val)
        
    def execute(self, machine):
        gpr = machine.context.gpr 
        gpr[self.RA] = (gpr[self.RS] | gpr[self.RB]) & 0xFFFFFFFF
        
        if self.RC:
            machine.context.cr.compare(0, to_python_int(gpr[self.RA]), 0)
        
    def __str__(self):
        if self.RC:
            dot = "."
        else:
            dot = ""
        
        if self.RS == self.RB:
            return "mr{0} r{1}, r{2}".format(dot, self.RA, self.RS)
        else:
            return "or{0} r{1}, r{2}, r{3}".format(dot, self.RA, self.RS, self.RB)
            
            
class AND(Instruction):
    def __init__(self, val):
        self.opcode, self.RS, self.RA, self.RB, self.opcode2, self.RC = parse_xform(val)
        
    def execute(self, machine):
        gpr = machine.context.gpr 
        gpr[self.RA] = (gpr[self.RS] & gpr[self.RB]) & 0xFFFFFFFF
        
        if self.RC:
            machine.context.cr.compare(0, to_python_int(gpr[self.RA]), 0)
        
    def __str__(self):
        if self.RC:
            dot = "."
        else:
            dot = ""
        
        return "and{0} r{1}, r{2}, r{3}".format(dot, self.RA, self.RS, self.RB)
        
        
class ANDImmediate(Instruction):
    def __init__(self, val):
        self.opcode, self.RS, self.RA, self.UI = parse_dform(val)
        
    def execute(self, machine):
        gpr = machine.context.gpr 
        gpr[self.RA] = (gpr[self.RS] & self.UI ) & 0xFFFFFFFF
        
    def __str__(self):
        return "andi r{0}, r{1}, {2}".format(dot, self.RA, self.RS, self.UI)


class ANDImmediateShifted(Instruction):
    def __init__(self, val):
        self.opcode, self.RS, self.RA, self.UI = parse_dform(val)
        
    def execute(self, machine):
        gpr = machine.context.gpr 
        gpr[self.RA] = (gpr[self.RS] & (self.UI << 16) ) & 0xFFFFFFFF
        
    def __str__(self):
        return "andis r{0}, r{1}, {2}".format(dot, self.RA, self.RS, self.UI)
        


class XORImmediate(Instruction):
    def __init__(self, val):
        self.opcode, self.RS, self.RA, self.UI = parse_dform(val)
        
    def execute(self, machine):
        gpr = machine.context.gpr 
        gpr[self.RA] = (gpr[self.RS] ^ self.UI ) & 0xFFFFFFFF
        
    def __str__(self):
        return "xori r{0}, r{1}, {2}".format(dot, self.RA, self.RS, self.UI)


class XORImmediateShifted(Instruction):
    def __init__(self, val):
        self.opcode, self.RS, self.RA, self.UI = parse_dform(val)
        
    def execute(self, machine):
        gpr = machine.context.gpr 
        gpr[self.RA] = (gpr[self.RS] ^ (self.UI << 16) ) & 0xFFFFFFFF
        
    def __str__(self):
        return "xoris r{0}, r{1}, {2}".format(dot, self.RA, self.RS, self.UI)


class XOR(Instruction):
    def __init__(self, val):
        self.opcode, self.RS, self.RA, self.RB, self.opcode2, self.RC = parse_xform(val)
        
    def execute(self, machine):
        gpr = machine.context.gpr 
        gpr[self.RA] = (gpr[self.RS] ^ gpr[self.RB]) & 0xFFFFFFFF
        
        if self.RC:
            machine.context.cr.compare(0, to_python_int(gpr[self.RA]), 0)
        
    def __str__(self):
        if self.RC:
            dot = "."
        else:
            dot = ""
        
        return "xor{0} r{1}, r{2}, r{3}".format(dot, self.RA, self.RS, self.RB)
        

class NAND(Instruction):
    def __init__(self, val):
        self.opcode, self.RS, self.RA, self.RB, self.opcode2, self.RC = parse_xform(val)
        
    def execute(self, machine):
        gpr = machine.context.gpr 
        gpr[self.RA] = negate((gpr[self.RS] & gpr[self.RB]) & 0xFFFFFFFF)
        
        if self.RC:
            machine.context.cr.compare(0, to_python_int(gpr[self.RA]), 0)
        
    def __str__(self):
        if self.RC:
            dot = "."
        else:
            dot = ""
        
        return "nand{0} r{1}, r{2}, r{3}".format(dot, self.RA, self.RS, self.RB)
        

class NOR(Instruction):
    def __init__(self, val):
        self.opcode, self.RS, self.RA, self.RB, self.opcode2, self.RC = parse_xform(val)
        
    def execute(self, machine):
        gpr = machine.context.gpr 
        gpr[self.RA] = negate((gpr[self.RS] | gpr[self.RB]) & 0xFFFFFFFF)
        
        if self.RC:
            machine.context.cr.compare(0, to_python_int(gpr[self.RA]), 0)
        
    def __str__(self):
        if self.RC:
            dot = "."
        else:
            dot = ""
        
        return "nor{0} r{1}, r{2}, r{3}".format(dot, self.RA, self.RS, self.RB)
        

class Equivalent(Instruction):
    def __init__(self, val):
        self.opcode, self.RS, self.RA, self.RB, self.opcode2, self.RC = parse_xform(val)
        
    def execute(self, machine):
        gpr = machine.context.gpr 
        gpr[self.RA] = negate((gpr[self.RS] ^ gpr[self.RB]) & 0xFFFFFFFF)
        
        if self.RC:
            machine.context.cr.compare(0, to_python_int(gpr[self.RA]), 0)
        
    def __str__(self):
        if self.RC:
            dot = "."
        else:
            dot = ""
        
        return "eqv{0} r{1}, r{2}, r{3}".format(dot, self.RA, self.RS, self.RB)
        
        
class ANDWithComplement(Instruction):
    def __init__(self, val):
        self.opcode, self.RS, self.RA, self.RB, self.opcode2, self.RC = parse_xform(val)
        
    def execute(self, machine):
        gpr = machine.context.gpr 
        gpr[self.RA] = (gpr[self.RS] & negate(gpr[self.RB])) & 0xFFFFFFFF
        
        if self.RC:
            machine.context.cr.compare(0, to_python_int(gpr[self.RA]), 0)
        
    def __str__(self):
        if self.RC:
            dot = "."
        else:
            dot = ""
        
        return "andc{0} r{1}, r{2}, r{3}".format(dot, self.RA, self.RS, self.RB)
        
        
class ORWithComplement(Instruction):
    def __init__(self, val):
        self.opcode, self.RS, self.RA, self.RB, self.opcode2, self.RC = parse_xform(val)
        
    def execute(self, machine):
        gpr = machine.context.gpr 
        gpr[self.RA] = (gpr[self.RS] | negate(gpr[self.RB])) & 0xFFFFFFFF
        
        if self.RC:
            machine.context.cr.compare(0, to_python_int(gpr[self.RA]), 0)
        
    def __str__(self):
        if self.RC:
            dot = "."
        else:
            dot = ""
        
        return "orc{0} r{1}, r{2}, r{3}".format(dot, self.RA, self.RS, self.RB)
        

class ExtendSignByte(Instruction):
    def __init__(self, val):
        self.opcode, self.RS, self.RA, self.RB, self.opcode2, self.RC = parse_xform(val)
        
    def execute(self, machine):
        gpr = machine.context.gpr
        sign = (gpr[self.RS] >> 7) & 1
        
        
        gpr[self.RA] = (0xFFFFFF00*sign | gpr[self.RB] & 0xFF) & 0xFFFFFFFF
        
        if self.RC:
            machine.context.cr.compare(0, to_python_int(gpr[self.RA]), 0)
        
    def __str__(self):
        if self.RC:
            dot = "."
        else:
            dot = ""
        
        return "extsb{0} r{1}, r{2}".format(dot, self.RA, self.RS, self.RB)


class ExtendSignHalfword(Instruction):
    def __init__(self, val):
        self.opcode, self.RS, self.RA, self.RB, self.opcode2, self.RC = parse_xform(val)
        
    def execute(self, machine):
        gpr = machine.context.gpr
        sign = (gpr[self.RS] >> 15) & 1
        
        
        gpr[self.RA] = (0xFFFF0000*sign | gpr[self.RB] & 0xFFFF) & 0xFFFFFFFF
        
        if self.RC:
            machine.context.cr.compare(0, to_python_int(gpr[self.RA]), 0)
        
    def __str__(self):
        if self.RC:
            dot = "."
        else:
            dot = ""
        
        return "extsh{0} r{1}, r{2}".format(dot, self.RA, self.RS, self.RB)
        
        
class CountLeadingZerosWord(Instruction):
    def __init__(self, val):
        self.opcode, self.RS, self.RA, self.RB, self.opcode2, self.RC = parse_xform(val)
        
    def execute(self, machine):
        gpr = machine.context.gpr
        count = 0
        for i in range(31, -1, -1):
            if not gpr[self.RB] & (1 << i):
                count += 1
            else:
                break 
                
        gpr[self.RA] = count
        
        if self.RC:
            machine.context.cr.compare(0, to_python_int(gpr[self.RA]), 0)
        
    def __str__(self):
        if self.RC:
            dot = "."
        else:
            dot = ""
        
        return "cntlzw{0} r{1}, r{2}".format(dot, self.RA, self.RS, self.RB)
        
        
def create_mask(mb, me):
    result = 0
    for i in range(mb, me+1):
        result = result | (1 << (31-i))
    
    return result 


class RotateLeftWordImmediateThenANDWithMask(Instruction):
    def __init__(self, val):
        self.opcode, self.RS, self.RA, self.SH, self.MB, self.ME, self.RC = parse_mform(val)
        
        
    def execute(self, machine):
        gpr = machine.context.gpr
        
        mask = create_mask(MB, ME)        
        result = gpr[self.RS] << self.SH 
        shifted_out = result >> 32
        result = result | shifted_out
        gpr[self.RA] = result & mask
        
        if self.RC:
            machine.context.cr.compare(0, to_python_int(gpr[self.RA]), 0)
        
    def __str__(self):
        if self.RC:
            dot = "."
        else:
            dot = ""
        
        return "rlwinm{0} r{1}, r{2}, {3}, {4}, {5}".format(
            dot, self.RA, self.RS, self.SH, self.MB, self.ME)
            
            
class RotateLeftWordThenANDWithMask(Instruction):
    def __init__(self, val):
        self.opcode, self.RS, self.RA, self.RB, self.MB, self.ME, self.RC = parse_mform(val)
        
        
    def execute(self, machine):
        gpr = machine.context.gpr
        
        mask = create_mask(MB, ME)        
        result = gpr[self.RS] << gpr[self.RB]
        shifted_out = result >> 32
        result = result | shifted_out
        gpr[self.RA] = result & mask
        
        if self.RC:
            machine.context.cr.compare(0, to_python_int(gpr[self.RA]), 0)
        
    def __str__(self):
        if self.RC:
            dot = "."
        else:
            dot = ""
        
        return "rlwnm{0} r{1}, r{2}, r{3}, {4}, {5}".format(
            dot, self.RA, self.RS, self.RB, self.MB, self.ME)
            
            
class RotateLeftWordImmediateThenMaskInsert(Instruction):
    def __init__(self, val):
        self.opcode, self.RS, self.RA, self.SH, self.MB, self.ME, self.RC = parse_mform(val)
        
        
    def execute(self, machine):
        gpr = machine.context.gpr
        
        mask = create_mask(MB, ME)        
        result = gpr[self.RS] << self.SH 
        shifted_out = result >> 32
        result = result | shifted_out
        gpr[self.RA] = (result & mask) | (gpr[self.RA] & negate(mask))
        
        if self.RC:
            machine.context.cr.compare(0, to_python_int(gpr[self.RA]), 0)
        
    def __str__(self):
        if self.RC:
            dot = "."
        else:
            dot = ""
        
        return "rlwimi{0} r{1}, r{2}, {3}, {4}, {5}".format(
            dot, self.RA, self.RS, self.SH, self.MB, self.ME)
            

class ShiftRightWord(Instruction):
    def __init__(self, val):
        self.opcode, self.RS, self.RA, self.RB, self.opcode2, self.RC = parse_xform(val)
        
    def execute(self, machine):
        gpr = machine.context.gpr 
        gpr[self.RA] = (gpr[self.RS] >> gpr[self.RB]) & 0xFFFFFFFF
        
        if self.RC:
            machine.context.cr.compare(0, to_python_int(gpr[self.RA]), 0)
        
    def __str__(self):
        if self.RC:
            dot = "."
        else:
            dot = ""
        
        return "srw{0} r{1}, r{2}, r{3}".format(dot, self.RA, self.RS, self.RB)
        
        
class ShiftLeftWord(Instruction):
    def __init__(self, val):
        self.opcode, self.RS, self.RA, self.RB, self.opcode2, self.RC = parse_xform(val)
        
    def execute(self, machine):
        gpr = machine.context.gpr 
        gpr[self.RA] = (gpr[self.RS] << gpr[self.RB]) & 0xFFFFFFFF
        
        if self.RC:
            machine.context.cr.compare(0, to_python_int(gpr[self.RA]), 0)
        
    def __str__(self):
        if self.RC:
            dot = "."
        else:
            dot = ""
        
        return "slw{0} r{1}, r{2}, r{3}".format(dot, self.RA, self.RS, self.RB)
        

class ShiftRightWordAlgebraicImmediate(Instruction):
    def __init__(self, val):
        self.opcode, self.RS, self.RA, self.SH, self.opcode2, self.RC = parse_xform(val)
        
    def execute(self, machine):
        gpr = machine.context.gpr 
        sign = (gpr[self.RS] >> 31) & 1
        mask = create_mask(0, self.SH)
        shifted_out = gpr[self.RS] & create_mask(31 - self.SH, 31)
        
        gpr[self.RA] = (gpr[self.RS] >> self.SH) & 0xFFFFFFFF
        gpr[self.RA] = gpr[self.RA] | (sign * mask)
        
        if sign and shifted_out:
            machine.context.xer.CA = 1
        else:
            machine.context.xer.CA = 0
        
        if self.RC:
            machine.context.cr.compare(0, to_python_int(gpr[self.RA]), 0)
        
    def __str__(self):
        if self.RC:
            dot = "."
        else:
            dot = ""
        
        return "srawi{0} r{1}, r{2}, {3}".format(dot, self.RA, self.RS, self.SH)
        
        
class ShiftRightWordAlgebraic(Instruction):
    def __init__(self, val):
        self.opcode, self.RS, self.RA, self.RB, self.opcode2, self.RC = parse_xform(val)
        
    def execute(self, machine):
        gpr = machine.context.gpr 
        sign = (gpr[self.RS] >> 31) & 1
        mask = create_mask(0, gpr[self.RB])
        shifted_out = gpr[self.RS] & create_mask(31 - gpr[self.RB], 31)
        
        gpr[self.RA] = (gpr[self.RS] >> gpr[self.RB]) & 0xFFFFFFFF
        gpr[self.RA] = gpr[self.RA] | (sign * mask)
        
        if sign and shifted_out:
            machine.context.xer.CA = 1
        else:
            machine.context.xer.CA = 0
        
        if self.RC:
            machine.context.cr.compare(0, to_python_int(gpr[self.RA]), 0)
        
    def __str__(self):
        if self.RC:
            dot = "."
        else:
            dot = ""
        
        return "sraw{0} r{1}, r{2}, r{3}".format(dot, self.RA, self.RS, self.RB)
        
if __name__ == "__main__":
    a = RotateLeftWordImmediateThenANDWithMask(0x54637C3E)
    print(a)