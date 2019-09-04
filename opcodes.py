def validate(assertion):
    if not assertion:
        raise RuntimeError("Invalid Instruction Form")


def get_bits(val, start, end):
    size = end-start 
    
    return (val >> (31-end)) & (2**size -1)


def get_bit(val, pos):
    return (val >> (31-pos)) & 1 


def parse_iform(val):
    opcode = get_bits(val, 0, 5)
    li = get_bits(val, 6, 29)
    aa = get_bit(val, 30)
    lk = get_bit(val, 30)
    
    return opcode, li, aa, lk 


def parse_bform(val):
    opcode = get_bits(val, 0, 5)
    bo = get_bits(val, 6, 10)
    bi = get_bits(val, 11, 15)
    bd = get_bits(val, 16, 29)
    aa = get_bit(val, 30)
    lk = get_bit(val, 31)
    
    return opcode, bo, bi, bd, aa, lk
    
    
def parse_dform(val):
    opcode = get_bits(val, 0, 5)
    a = get_bits(val, 6, 10)
    b = get_bits(val, 11, 15)
    c = get_bits(val, 16, 31)
    
    return opcode, a, b, c 


def parse_dsform(val):
    opcode = get_bits(val, 0, 5)
    a = get_bits(val, 6, 10)
    b = get_bits(val, 11, 15)
    c = get_bits(val, 16, 29)
    xo = get_bits(val, 30, 31)
    
    return opcode, a, b, c, xo 
    

def parse_xform(val):
    opcode = get_bits(val, 0, 5)
    a = get_bits(val, 6, 10)
    b = get_bits(val, 11, 15)
    c = get_bits(val, 16, 20)
    xo = get_bits(val, 21, 30)
    rc = get_bit(val, 31)
    
    return opcode, a, b, c, xo, rc 


def sign_extend_short(val):
    if val & (1 << 16):
        return 0xFFFF0000 | val 
    else:
        return val 


def add_32bit(val1, val2):
    return (val1 + val2) & 0xFFFFFFFF
    
    
class PPCContext(object):
    def __init__(self):
        self.gpr = [0 for x in range(32)]
        self.fpr = [0.0 for x in range(32)]


class Instruction(object):
    pass


class LoadValueZero(Instruction):
    def __init__(self, val):
        self.opcode, self.RT, self.RA, self.D = parse_dform(val)
        self.D = sign_extend_short(self.D)
        
    def _get_ea(self, machine):
        gpr = machine.context.gpr
        
        if self.RA == 0:
            b = 0 
        else:
            b = gpr[self.RA] 
        
        EA = add_32bit(b + self.D)
        
        return EA 
        
        gpr[self.rt] = machine.readbyte(EA)


class LoadByteZero(LoadValueZero):
    def execute(self, machine):
        EA = self._get_ea(machine)
        machine.context.gpr[self.rt] = machine.readbyte(EA)
    
    def __str__(self):
        return "lbz r{0}, {1}(r{2})".format(self.RT, self.D, self.RA)


class LoadByteZeroUpdate(LoadValueZero):
    def execute(self, machine):
        gpr = machine.context.gpr
        EA = add_32bit(gpr[self.RA] + self.D)
        
        machine.context.gpr[self.RT] = machine.readbyte(EA)
        self.context.gpr[self.RA] = EA 
    
    def __str__(self):
        return "lbzu r{0}, {1}(r{2})".format(self.RT, self.D, self.RA)


class LoadHalfwordZero(LoadValueZero):
    def execute(self, machine):
        EA = self._get_ea(machine)
        machine.context.gpr[self.RT] = machine.readhalfword(EA)
        self.context.gpr[self.RA] = EA 
    
    def __str__(self):
        return "lhz r{0}, {1}(r{2})".format(self.RT, self.D, self.RA)


class LoadHalfwordZeroUpdate(LoadValueZero):
    def __init__(self, val):
        super().__init__(val)
        validate(self.RA != 0 and self.RA != self.RT)
        
    def execute(self, machine):
        gpr = machine.context.gpr
        EA = add_32bit(gpr[self.RA] + self.D)
        
        machine.context.gpr[self.RT] = machine.readhalfword(EA)
        self.context.gpr[self.RA] = EA 
    
    def __str__(self):
        return "lhzu r{0}, {1}(r{2})".format(self.RT, self.D, self.RA)


class LoadHalfwordAlgebraic(LoadByteZero):
    def execute(self, machine):
        gpr = machine.context.gpr
        EA = add_32bit(gpr[self.RA] + self.D)
        
        gpr[self.rt] = sign_extend_short(machine.readhalfword(EA))
    
    def __str__(self):
        return "lha r{0}, {1}(r{2})".format(self.RT, self.D, self.RA)


class LoadHalfwordAlgebraicUpdate(LoadByteZero):
    def __init__(self, val):
        super().__init__(val)
        validate(self.RA != 0 and self.RA != self.RT) 
        
    def execute(self, machine):
        gpr = machine.context.gpr
        EA = add_32bit(gpr[self.RA] + self.D)
        
        gpr[self.rt] = sign_extend_short(machine.readhalfword(EA))
        self.context.gpr[self.RA] = EA
        
    def __str__(self):
        return "lhau r{0}, {1}(r{2})".format(self.RT, self.D, self.RA)


class LoadWordZero(LoadValueZero):
    def execute(self, machine):
        EA = self._get_ea(machine)
        machine.context.gpr[self.RT] = machine.readword(EA) 
    
    def __str__(self):
        return "lwz r{0}, {1}(r{2})".format(self.RT, self.D, self.RA)


class LoadWordZeroUpdate(LoadValueZero):
    def execute(self, machine):
        gpr = machine.context.gpr
        EA = add_32bit(gpr[self.RA] + self.D)
        
        machine.context.gpr[self.RT] = machine.readword(EA)
        self.context.gpr[self.RA] = EA 
    
    def __str__(self):
        return "lwzu r{0}, {1}(r{2})".format(self.RT, self.D, self.RA)

if __name__ == "__main__":
    lbz = LoadByteZero(0x80a400d8)
    print(lbz)