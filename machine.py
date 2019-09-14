import os 
from io import BytesIO
from struct import pack, unpack 
from instructions.dispatcher import parse_instruction

class PPCContext(object):
    def __init__(self):
        self.gpr = [0 for x in range(32)] # 32 General Purpose Registers
        self.fpr = [0.0 for x in range(32)] # 32 Floating Point Registers 
        self.cr = ConditionalRegister() # Conditional register
        self.xer = XerRegister()
        self.pc = 0 
        self.lr = 0
        
    def __str__(self):
        out = ""
        out += ", ".join(["r{0}: {1:x}".format(i, self.gpr[i]) for i in range(32)]) + "\n"
        out += ", ".join(["r{0}: {1}".format(i, self.fpr[i]) for i in range(32)]) + "\n" 
        out += str(self.cr) + "\n"
        out += str(self.xer) + "\n"
        out += "PC: {0:x}".format(self.pc) + "\n"
        out += "LR: {0:x}".format(self.lr) 
        
        return out 
        
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
            elif compare_result == 0:
                out += "CR{0}: -, ".format(i)
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
    def __init__(self, memory_sections):
        print(memory_sections)
        self.context = PPCContext()
        
        self.memory_sections = []
        for cached_start, uncached_start, size in memory_sections:
            self.memory_sections.append((cached_start, uncached_start, size, BytesIO(b"\x00"*size)))
    
    def load_binary(self, address, f):
        self.write_data(address, f.read())
    
    def dump_memory(self, dirpath):
        for cached_start, _, size, data in self.memory_sections:
            name = "memdump_{0:x}.bin".format(cached_start)
            with open(os.path.join(dirpath, name), "wb") as f:
                data.seek(0)
                f.write(data.read())
    
    def write_data(self, address, data):
        for cached_start, uncached_start, size, mem in self.memory_sections:
            cached_end = cached_start + size 
            uncached_end = uncached_start + size 
            
            if cached_start <= address < cached_end:
                if address+len(data) >= cached_end:
                    raise RuntimeError("Data to be written exceeds end of memory section") 
                    
                relative = address - cached_start 
                mem.seek(relative)
                mem.write(data)
                return 
                
            elif uncached_start <= address < uncached_end:
                if address+len(data) >= uncached_end:
                    raise RuntimeError("Data to be written exceeds end of memory section") 
                    
                relative = address - uncached_start 
                mem.seek(relative)
                mem.write(data)
                return 
                
        raise RuntimeError("Reading from unmapped memory: {0:x}".format(address))
    
    def read_data(self, address, len):
        for cached_start, uncached_start, size, mem in self.memory_sections:
            
            cached_end = cached_start + size 
            uncached_end = uncached_start + size 
            
            if cached_start <= address < cached_end:
                if address+len >= cached_end:
                    raise RuntimeError("Data to be read exceeds end of memory section") 
                    
                relative = address - cached_start 
                mem.seek(relative)
                return mem.read(len)
                
            elif uncached_start <= address < uncached_end:
                if address+len >= uncached_end:
                    raise RuntimeError("Data to be read exceeds end of memory section") 
                    
                relative = address - uncached_start 
                mem.seek(relative)
                return mem.read(len)
        
        raise RuntimeError("Writing to unmapped memory: {0:x}".format(address))
    
    def read_byte(self, address):
        return unpack("B", self.read_data(address, 1))[0]
    
    def read_halfword(self, address):
        return unpack(">H", self.read_data(address, 2))[0]
    
    def read_word(self, address):
        return unpack(">I", self.read_data(address, 4))[0]
    
    def write_byte(self, address, value):
        self.write_data(address, pack("B", value&0xFF))
    
    def write_halfword(self, address, value):
        self.write_data(address, pack(">H", value&0xFFFF))
    
    def write_word(self, address, value):
        self.write_data(address, pack(">I", value&0xFFFFFFFF))
    
    def goto(self, address):
        self.context.pc = address 
    
    def execute_next(self):
        assert self.context.pc % 4 == 0
        val = self.read_word(self.context.pc)
        instruction = parse_instruction(val)
        print(instruction)
        instruction.execute(self)
        
        self.context.pc += 4
    
    def run(self):
        while True:
            self.execute_next()
        
class GCMachine(Machine):
    def __init__(self, memsize=0x01800000):
        super().__init__([(0x80000000, 0xC0000000, memsize)])


    
    
if __name__ == "__main__":
    gc = GCMachine()
    with open("data.bin", "rb") as f:
        gc.load_binary(0x80000000, f)
    gc.goto(0x80000000)
    
    print(gc.context)
    print("hm", hex(gc.read_word(gc.context.pc)))
    gc.context.gpr[3] = 0x80000000
    gc.execute_next()
    gc.execute_next()
    gc.context.gpr[0] = 0xABCDEFAA
    gc.execute_next()
    gc.execute_next()
    gc.dump_memory(".")
    