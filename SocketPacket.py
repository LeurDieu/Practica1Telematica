class sPacket():
    def __init__(self, comm, *args):
        self.command = comm
        self.name = None
        self.data = None
        
        if (len(args) > 0):
            if (len(args) > 1):
                self.name = args[1]
            self.data = args[0]
        
    def getComm(self):
        return int(self.command)

    def getName(self):
        return str(self.name)

    def getData(self):
        return self.data