class Debug_cp:
    """
    controled debugger logging module better
    """

    def __init__(self, name):
        self.name = name
        self.var = 1

    def run(self):
        print(self.name, "*** entered cp", self.var)
        self.var += 1
