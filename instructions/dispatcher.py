from .loadstore import *

def parse_indexed(val):
    pass 

instructions = {
32: LoadWordZero,
33: LoadWordZeroUpdate,
34: LoadByteZero,
35: LoadByteZeroUpdate,
36: StoreWord,
37: StoreWordUpdate,
38: StoreByte,
39: StoreByteUpdate,
40: LoadHalfwordZero,
41: LoadHalfwordZeroUpdate,
42: LoadHalfwordAlgebraic,
43: LoadHalfwordAlgebraicUpdate,
44: StoreHalfword,
45: StoreHalfwordUpdate
}

def parse_instruction(val):
    opcode = get_bits(val, 0, 5)
    
    if opcode in instructions:
        instruction = instructions[opcode](val)
    elif opcode == 31:
        instruction = parse_indexed(val)
    else:
        raise RuntimeError("Unknown opcode {0}".format(opcode))
    
    return instruction
