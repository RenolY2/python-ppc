def validate(assertion):
    if not assertion:
        raise RuntimeError("Invalid Instruction Form")


def get_bits(val, start, end):
    size = end-start + 1
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


def sign_extend_24bit(val):
    if val & (1 << 24):
        return 0xFF000000 | val 
    else:
        return val 


def add_32bit(val1, val2):
    return (val1 + val2) & 0xFFFFFFFF
    

def signed(val1):
    assert -0x80000000 <= val1 <= 0x7FFFFFFF 
    if val1 >= 0:
        return val1 
    else:
        return 2**32 + val1 


class Instruction(object):
    pass
