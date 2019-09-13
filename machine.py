class PPCContext(object):
    def __init__(self):
        self.gpr = [0 for x in range(32)] # 32 General Purpose Registers
        self.fpr = [0.0 for x in range(32)] # 32 Floating Point Registers 
        self.cr = [0 for x in range(8)] # 8 conditional registers


class Machine(object):
    def __init__(self):
        pass
        