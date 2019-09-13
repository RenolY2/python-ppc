
# Base classes 

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


class LoadValueZeroIndexed(Instruction):
    def __init__(self, val):
        self.opcode, self.RT, self.RA, self.RB, self.subopcode, _ = parse_xform(val)
        
    def _get_ea(self, machine):
        gpr = machine.context.gpr
        
        if self.RA == 0:
            b = 0 
        else:
            b = gpr[self.RA] 
        
        EA = add_32bit(b + gpr[self.RB])
        
        return EA 


class StoreValue(LoadValueZero):
    def __init__(self, val):
        self.opcode, self.RS, self.RA, self.D = parse_dform(val)
        self.D = sign_extend_short(self.D)


class StoreValueUpdate(StoreValue):
    def __init__(self, val):
        super().__init__(val)
        validate(self.RA != 0)
        
        
class StoreValueUpdateIndexed(StoreValueIndexed):
    def __init__(self, val):
        super().__init__(val)   

# Actual implementation

class LoadByteZero(LoadValueZero):
    def execute(self, machine):
        EA = self._get_ea(machine)
        machine.context.gpr[self.rt] = machine.readbyte(EA)
    
    def __str__(self):
        return "lbz r{0}, {1}(r{2})".format(self.RT, self.D, self.RA)


class LoadHalfwordZero(LoadValueZero):
    def execute(self, machine):
        EA = self._get_ea(machine)
        machine.context.gpr[self.RT] = machine.readhalfword(EA)
        self.context.gpr[self.RA] = EA 
    
    def __str__(self):
        return "lhz r{0}, {1}(r{2})".format(self.RT, self.D, self.RA)

class LoadHalfwordAlgebraic(LoadByteZero):
    def execute(self, machine):
        gpr = machine.context.gpr
        EA = add_32bit(gpr[self.RA] + self.D)
        
        gpr[self.rt] = sign_extend_short(machine.readhalfword(EA))
    
    def __str__(self):
        return "lha r{0}, {1}(r{2})".format(self.RT, self.D, self.RA)


class LoadWordZero(LoadValueZero):
    def execute(self, machine):
        EA = self._get_ea(machine)
        machine.context.gpr[self.RT] = machine.readword(EA) 
    
    def __str__(self):
        return "lwz r{0}, {1}(r{2})".format(self.RT, self.D, self.RA)

class LoadByteZeroUpdate(LoadValueZero):
    def execute(self, machine):
        gpr = machine.context.gpr
        EA = add_32bit(gpr[self.RA] + self.D)
        
        machine.context.gpr[self.RT] = machine.readbyte(EA)
        self.context.gpr[self.RA] = EA 
    
    def __str__(self):
        return "lbzu r{0}, {1}(r{2})".format(self.RT, self.D, self.RA)


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



class LoadWordZeroUpdate(LoadValueZero):
    def execute(self, machine):
        gpr = machine.context.gpr
        EA = add_32bit(gpr[self.RA] + self.D)
        
        gpr[self.RT] = machine.readword(EA)
        gpr[self.RA] = EA 
    
    def __str__(self):
        return "lwzu r{0}, {1}(r{2})".format(self.RT, self.D, self.RA)


####################


# Byte Indexed
class LoadByteZeroIndexed(LoadValueZeroIndexed):
    def execute(self, machine):
        EA = self._get_ea(machine)
        machine.context.gpr[self.RT] = machine.readbyte(EA)

    def __str__(self):
        return "lbzx r{0}, r{1}, r{2}".format(self.RT, self.RA, self.RB)


# Halfword Indexed
class LoadHalfwordZeroIndexed(LoadValueZeroIndexed):
    def execute(self, machine):
        EA = self._get_ea(machine)
        machine.context.gpr[self.RT] = machine.readhalfword(EA)

    def __str__(self):
        return "lhzx r{0}, r{1}, r{2}".format(self.RT, self.RA, self.RB)


class LoadHalfwordAlgebraicIndexed(LoadValueZeroIndexed):
    def execute(self, machine):
        EA = self._get_ea(machine)
        machine.context.gpr[self.RT] = sign_extend_short(machine.readhalfword(EA))

    def __str__(self):
        return "lhax r{0}, r{1}, r{2}".format(self.RT, self.RA, self.RB)

    
# Word Indexed
class LoadWordIndexed(LoadValueZeroIndexed):
    def execute(self, machine):
        gpr = machine.context.gpr
        
        EA = add_32bit(gpr[self.RA], gpr[self.RB])
        gpr[self.RT] = machine.readword(EA)
        gpr[self.RA] = EA 
        
    def __str__(self):
        return "lwzx r{0}, r{1}, r{2}".format(self.RT, self.RA, self.RB)



class LoadByteZeroUpdateIndexed(LoadValueZeroIndexed):
    def execute(self, machine):
        gpr = machine.context.gpr
        
        EA = add_32bit(gpr[self.RA] + gpr[self.RB])
        gpr[self.RT] = machine.readbyte(EA)
        gpr[self.RA] = EA 
        
    def __str__(self):
        return "lbzux r{0}, r{1}, r{2}".format(self.RT, self.RA, self.RB)

    
class LoadHalfwordZeroUpdateIndexed(LoadValueZeroIndexed):
    def execute(self, machine):
        gpr = machine.context.gpr
        
        EA = add_32bit(gpr[self.RA] + gpr[self.RB])
        gpr[self.RT] = machine.readhalfword(EA)
        gpr[self.RA] = EA 
        
    def __str__(self):
        return "lhzux r{0}, r{1}, r{2}".format(self.RT, self.RA, self.RB)

    
class LoadHalfwordAlgebraicUpdateIndexed(LoadValueZeroIndexed):
    def execute(self, machine):
        gpr = machine.context.gpr
        
        EA = add_32bit(gpr[self.RA] + gpr[self.RB])
        gpr[self.RT] = sign_extend_short(machine.readhalfword(EA))
        gpr[self.RA] = EA 
        
    def __str__(self):
        return "lhaux r{0}, r{1}, r{2}".format(self.RT, self.RA, self.RB)


class LoadWordUpdateIndexed(LoadValueZeroIndexed):
    def execute(self, machine):
        gpr = machine.context.gpr
        
        EA = add_32bit(gpr[self.RA], gpr[self.RB])
        gpr[self.RT] = machine.readword(EA)
        gpr[self.RA] = EA 
        
    def __str__(self):
        return "lwzux r{0}, r{1}, r{2}".format(self.RT, self.RA, self.RB)


# Store Value Direct 

class StoreByte(StoreValue):
    def execute(self, machine):
        EA = self._get_ea(machine)
        machine.writebyte(EA, machine.gpr[self.RS])
    
    def __str__(self):
        return "stb r{0}, {1}(r{2})".format(self.RS, self.D, self.RA)


class StoreHalfword(StoreValue):
    def execute(self, machine):
        EA = self._get_ea(machine)
        machine.writehalfword(EA, machine.gpr[self.RS])
    
    def __str__(self):
        return "sth r{0}, {1}(r{2})".format(self.RS, self.D, self.RA)


class StoreWord(StoreValue):
    def execute(self, machine):
        EA = self._get_ea(machine)
        machine.writeword(EA, machine.gpr[self.RS])
        
    def __str__(self):
        return "stw r{0}, {1}(r{2})".format(self.RS, self.D, self.RA)


# Store Value + Update variants
class StoreByteUpdate(StoreValueUpdate):
    def execute(self, machine):
        gpr = machine.context.gpr
        
        EA = add_32bit(gpr[self.RA], self.D)
        machine.writebyte(EA, gpr[self.RS])
        gpr[self.RA] = EA
    
    def __str__(self):
        return "stbu r{0}, {1}(r{2})".format(self.RS, self.D, self.RA)


class StoreHalfwordUpdate(StoreValueUpdate):
    def execute(self, machine):
        gpr = machine.context.gpr
        
        EA = add_32bit(gpr[self.RA], self.D)
        machine.writehalfword(EA, gpr[self.RS])
        gpr[self.RA] = EA
    
    def __str__(self):
        return "sthu r{0}, {1}(r{2})".format(self.RS, self.D, self.RA)


class StoreWordUpdate(StoreValueUpdate):
    def execute(self, machine):
        gpr = machine.context.gpr
        
        EA = add_32bit(gpr[self.RA], self.D)
        machine.writeword(EA, gpr[self.RS])
        gpr[self.RA] = EA
        
    def __str__(self):
        return "stwu r{0}, {1}(r{2})".format(self.RS, self.D, self.RA)
        
        
# Store Value Indexed 
class StoreValueIndexed(Instruction):
    def __init__(self, val):
        self.opcode, self.RS, self.RA, self.RB, self.subopcode, _ = parse_xform(val)


class StoreByteIndexed(StoreValueIndexed):
    def execute(self, machine):
        gpr = machine.context.gpr
        if self.RA == 0:
            b = 0
        else:
            b = gpr[self.RA] 
            
        EA = add_32bit(b, gpr[self.RB])
        machine.writebyte(EA, gpr[self.RS])
    
    def __str__(self):
        return "stbx r{0}, r{1}, r{2}".format(self.RS, self.RA, self.RB)
        
        
class StoreHalfwordIndexed(StoreValueZeroIndexed):
    def execute(self, machine):
        gpr = machine.context.gpr
        if self.RA == 0:
            b = 0
        else:
            b = gpr[self.RA] 
            
        EA = add_32bit(b, gpr[self.RB])
        machine.writehalfword(EA, gpr[self.RS])
    
    def __str__(self):
        return "sthx r{0}, r{1}, r{2}".format(self.RS, self.RA, self.RB)
        
        
class StoreWordIndexed(StoreValueZeroIndexed):
    def execute(self, machine):
        gpr = machine.context.gpr
        if self.RA == 0:
            b = 0
        else:
            b = gpr[self.RA] 
            
        EA = add_32bit(b, gpr[self.RB])
        machine.writeword(EA, gpr[self.RS])
    
    def __str__(self):
        return "stwx r{0}, r{1}, r{2}".format(self.RS, self.RA, self.RB)
        
# Store value zero indexed with update
class StoreByteUpdateIndexed(StoreValueIndexed):
    def execute(self, machine):
        gpr = machine.context.gpr
        
        EA = add_32bit(gpr[self.RA], gpr[self.RB])
        machine.writebyte(EA, gpr[self.RS])
        gpr[self.RA] = EA 
    
    def __str__(self):
        return "stbux r{0}, r{1}, r{2}".format(self.RS, self.RA, self.RB)


class StoreHalfwordUpdateIndexed(StoreValueIndexed):
    def execute(self, machine):
        gpr = machine.context.gpr
        
        EA = add_32bit(gpr[self.RA], gpr[self.RB])
        machine.writehalfword(EA, gpr[self.RS])
        gpr[self.RA] = EA 
    
    def __str__(self):
        return "sthux r{0}, r{1}, r{2}".format(self.RS, self.RA, self.RB)


class StoreWordUpdateIndexed(StoreValueIndexed):
    def execute(self, machine):
        gpr = machine.context.gpr
        
        EA = add_32bit(gpr[self.RA], gpr[self.RB])
        machine.writeword(EA, gpr[self.RS])
        gpr[self.RA] = EA 
    
    def __str__(self):
        return "stwux r{0}, r{1}, r{2}".format(self.RS, self.RA, self.RB)



class LoadMultipleWord(LoadValueZero):
    def __init__(self, val):
        super().__init__(val)
        validate(self.RA < self.RT)
        
    def execute(self, machine):
        EA = self._get_ea(machine)
        gpr = machine.context.gpr 
        
        r = self.RT 
        
        while r <= 31:
            gpr[r] = machine.readword(EA)
            r += 1 
            EA += 4 
    
    def __str__(self):
        return "lmw r{0}, {1}({2})".format(self.RT, self.D, self.RA)
        
        
class StoreMultipleWord(LoadValueZero):
    def execute(self, machine):
        EA = self._get_ea(machine)
        gpr = machine.context.gpr 
        
        r = self.RT 
        
        while r <= 31:
            machine.writeword(EA, gpr[r])
            r += 1 
            EA += 4 
    
    def __str__(self):
        return "stmw r{0}, {1}({2})".format(self.RT, self.D, self.RA)

if __name__ == "__main__":
    lbz = LoadByteZero(0x80a400d8)
    print(lbz)