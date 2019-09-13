class PPCContext(object):
    def __init__(self):
        self.gpr = [0 for x in range(32)]
        self.fpr = [0.0 for x in range(32)]


class Machine(object):
    def __init__(self):
        pass
        