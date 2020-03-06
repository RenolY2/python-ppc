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