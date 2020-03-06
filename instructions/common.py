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


def parse_xoform(val):
    opcode = get_bits(val, 0, 5)
    a = get_bits(val, 6, 10)
    b = get_bits(val, 11, 15)
    c = get_bits(val, 16, 20)
    oe = get_bit(val, 21)
    xo = get_bits(val, 22, 30)
    rc = get_bit(val, 31)
    
    return opcode, a, b, c, oe, xo, rc 
    
    
def parse_xfxform(val):
    opcode = get_bits(val, 0, 5)
    rt = get_bits(val, 6, 10)
    spr = get_bits(val, 11, 20)
    xo = get_bits(val, 21, 30)
    
    return opcode, rt, spr, xo 
    
    
def parse_xflform(val):
    opcode = get_bits(val, 0, 5)
    flm = get_bits(val, 7, 14)
    frb = get_bits(val, 16, 20)
    xo = get_bits(val, 21, 30)
    rc = get_bit(val, 31)
    
    return opcode, flm, frb, xo, rc
    

def sign_extend_short(val):
    if val & (1 << 15):
        return 0xFFFF0000 | val 
    else:
        return val 

def sign_extend_14bit(val):
    if val & (1 << 13):
        return 0xFFFFC000 | val 
    else:
        return val 


def sign_extend_24bit(val):
    if val & (1 << 23):
        return 0xFF000000 | val 
    else:
        return val 


def add_32bit(val1, val2):
    return (val1 + val2) & 0xFFFFFFFF


def add_32bit_overflow(val1, val2):
    result = (val1 + val2)
    return (result) & 0xFFFFFFFF, (result >> 32) > 0
    

def signed(val1):
    assert -0x80000000 <= val1 <= 0x7FFFFFFF 
    if val1 >= 0:
        return val1 
    else:
        return 2**32 + val1 


def to_python_int(val):
    assert 0 <= val < (2**32) 
    if val & (1<<31):
        return val - (2**32)
    else:
        return val 


def negate(val):
    assert 0 <= val < (2**32) 
    
    return (2**32 - val) & 0xFFFFFFFF


class Instruction(object):
    pass