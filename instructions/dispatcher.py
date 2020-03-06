from .loadstore import *
from .fixedpointarithmetic import *
from .comparison import *
from .special import * 
from .branching import *
from .logical import * 

instructions = {
10: CompareLogicalImmediate,
11: CompareImmediate,
14: AddImmediate,
15: AddImmediateShifted,
16: BranchConditional,
18: Branch,
24: ORImmediate,
25: ORImmediateShifted,
26: XORImmediate,
27: XORImmediateShifted,
28: ANDImmediate,
29: ANDImmediateShifted,
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
instructions_x = {
    0: Compare,
    19: MoveFromCR,
    26: CountLeadingZerosWord,
    28: AND,
    60: AndWithComplement,
    124: NOR,
    
    144: MoveToCRFields,
    284: Equivalent,
    316: XOR,
    
    339: MoveFromSPR,
    412: ORWithComplement,
    444: OR,
    467: MoveToSPR
    476: NAND,
    922: ExtendSignHalfword,
    954: ExtendSignByte,
    
}

instructions_xo = {
    266: Add,
    40: SubtractFrom
}

instructions_xl = {
    16: BranchConditionalToLR
}

def parse_instruction(val):
    opcode = get_bits(val, 0, 5)
   
    if opcode in instructions:
        # Do Main Instructions
        instruction = instructions[opcode](val)
    elif opcode == 19:
        opcode2 = get_bits(val, 21, 30)
        if opcode2 in instructions_xl:
            instruction = instructions_xl[opcode2](val)
        else:
            raise RuntimeError("Unknown opcode2 xl {0}".format(opcode2))
        
    elif opcode == 31:
        opcode2 = get_bits(val, 21, 30)
        
        if opcode2 in instructions_x:
            # Do X Form Instructions 
            instruction = instructions_x[opcode2](val)
        else:
            opcode2 = get_bits(val, 22, 30)
            
            if opcode2 in instructions_xo:
                # do XO Form Instructions
                instruction = instructions_xo[opcode2](val)
            else:
                raise RuntimeError("Unknown opcode2 {0} or {1}".format( get_bits(val, 21, 30), get_bits(val, 22, 30)))
    else:
        raise RuntimeError("Unknown opcode {0}".format(opcode))

    return instruction

"""
def parse_x_family(val):
    opcode = get_bits(val, 0, 5)
    assert opcode == 31 
    
    opcode2 = get_bits(22, 30)
    
    if opcode2 in instructions_xo:"""
        
    
    
