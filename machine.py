class PPCContext(object):
    def __init__(self):
        self.gpr = [0 for x in range(32)] # 32 General Purpose Registers
        self.fpr = [0.0 for x in range(32)] # 32 Floating Point Registers 
        self.cr = ConditionalRegister() # Conditional register

LT = 0b1000 # result is negative, or less than 
GT = 0b0100 # result is positive and not zero, or bigger than  
EQ = 0b0010 # result is zero, or equal to 
SO = 0b0001 # summary overflow or floating-point unordered (frA or frB or both are NaN)

class ConditionalRegister(object):
    def __init__(self):
        self.cr = [0 for x in range(8)]
    
    def __getitem__(self, index):
        return self.cr[index]
    
    def __setitem__(self, index, value):
        assert value in (LT, GT, EQ, SO, 0)
        self.cr[index] = value 
    
    def from_value(self, val):
        for i in range(8):
            bitfield = (val >> (7-i)*4) & 0b1111 
            self.cr[i] = bitfield 
    
    def to_value(self):
        val = 0
        for i in range(8):
            val = val | (self.cr[i] << (7-i)*4)
    
    def is_equal(self, index):
        return self.cr[index] == EQ 
    
    def is_lesser(self, index):
        return self.cr[index] == LT 
    
    def is_bigger(self, index):
        return self.cr[index] == GT
    
    def __str__(self):
        out = ""
        for i in range(8):
            if self.cr[i] == LT:
                out += "CR{0}: LT, ".format(i)
            elif self.cr[i] == GT:
                out += "CR{0}: GT, ".format(i)
            elif self.cr[i] == EQ:
                out += "CR{0}: EQ, ".format(i)
            elif self.cr[i] == SO:
                out += "CR{0}: SO, ".format(i)
            else:
                out += "CR{0}: 0, ".format(i)
        
        return out 
        
        
class Machine(object):
    def __init__(self):
        pass
        
        
if __name__ == "__main__":
    cr = ConditionalRegister()
    cr.from_value(0x40000088)
    print(cr)
    cr.from_value(0x20000088)
    print(cr)
    print(cr.is_equal(0))
    