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
        if value == SO:
            # SO bit is independent of comparison bits
            self.cr[index] = value | SO 
        else:
            # SO bit can only be cleared by MTSPR/MCRXR
            self.cr[index] = value | (self.cr[index] & SO)
        
    def from_value(self, val):
        for i in range(8):
            bitfield = (val >> (7-i)*4) & 0b1111 
            self.cr[i] = bitfield 
    
    def to_value(self):
        val = 0
        for i in range(8):
            val = val | (self.cr[i] << (7-i)*4)
    
    def clear(self, index):
        self.cr[index] = 0
    
    def is_equal(self, index):
        return self.cr[index] == EQ 
    
    def is_lesser(self, index):
        return self.cr[index] == LT 
    
    def is_bigger(self, index):
        return self.cr[index] == GT
    
    def __str__(self):
        out = ""
        for i in range(8):
            compare_result = self.cr[i] & ~SO 
            so_bit = self.cr[i] & SO 
            
            if compare_result == LT:
                out += "CR{0}: LT, ".format(i)
            elif compare_result == GT:
                out += "CR{0}: GT, ".format(i)
            elif compare_result == EQ:
                out += "CR{0}: EQ, ".format(i)
            else:
                raise RuntimeError("Invalid compare result: {0}".format(compare_result))
                
            if so_bit:
                out += "SO, "
        
        return out 


class XerRegister(object):
    def __init__(self):
        self.SO = 0 # summary overflow when instruction sets OV and remains until cleared 
        self.OV = 0 # overflow, indicate that overflow occured during execution of an instruction 
        self.CA = 0 # carry, set if there is a carry out of the msb 
        self.reserved = 0
        self.bytes_transfered = 0
        
    def from_value(self, val):
        self.bytes_transfered = val & 0b1111111 # 7 bits 
        self.reserved = (val >> 7) & 0b1111111111111111111111 # 22 bits 
        self.CA = (val >> 29) & 1 
        self.OV = (val >> 30) & 1 
        self.SO = (val >> 31) & 1 
    
    def to_value(self):
        val = 0
        val = val | (self.bytes_transfered & 0b1111111)
        val = val | (self.reserved & 0b1111111111111111111111) << 7 
        val = val | (self.CA & 1) << 29 
        val = val | (self.OV & 1) << 30
        val = val | (self.SO & 1) << 31 
        
        return val 
        
    
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
    