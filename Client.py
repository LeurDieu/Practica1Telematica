from SocketHandler import SocketHandler
from SocketPacket import sPacket as SP
import glob
import sys
import os
import pathlib

class Client(SocketHandler):
    def __init__(self, h, p):
        super().__init__(h, p)
        self.sock.connect((str(self.host), int(self.port)))
        self.id = hex(id(self))
        self.dirs = []
        self.path = pathlib.Path(__file__).parent.absolute()
    
    def run(self):
        while (True):
            msg = input("-> ")
            
            if (msg == 'exit'):
                self.sock.close()
                sys.exit()
                
            if (msg == 'send_file'):
                self.loadFile()

            if (msg == 'create_bucket'):
                self.createBucket()

            if (msg == 'remove_bucket'):
                self.removeBucket()

            if (msg == 'lsb'):
                self.lsb()
            
            if (msg == 'lsf'):
                self.lsf()
            
            if (msg == 'df'):
                self.df()

            if (msg == 'rf'):
                self.rf()

            while (True):
                res = self.awaitResponse(self.sock)
                if(self.dictionary(res)):
                    break

    def dictionary(self, data:SP):
        comm = data.getComm()
        if (comm == 0):
            return True
        if (comm == 1 ):
            self.askParams(data)

        if (comm == 2 ):
            self.chooseOption(data)

        if (comm == 3 ):
            self.saveFile(data)

        if (comm == 4 ):
            self.displayOptions(data.getData(),data.getName())
        return False
        

    def createBucket(self):
        self.sendMessage(self.sock, 4)

    def removeBucket(self):
        self.sendMessage(self.sock, 5)

    def lsb(self):
        self.sendMessage(self.sock, 8)
    
    def lsf(self):
        self.sendMessage(self.sock, 7)
    
    def df(self):
        self.sendMessage(self.sock, 2)

    def rf(self):
        self.sendMessage(self.sock, 3)

    def askParams(self, data:SP):
        self.displayOptions(data.getData(),data.getName())
        self.sendMessage(self.sock, 6, input("->:"))

    def chooseOption(self, data:SP):
        self.displayOptions(data.getData(),data.getName())
        self.sendMessage(self.sock, 6, int(input("->:")))
    
    def saveFile(self, data:SP):
        self.writeFile(self.path,data)
    

    def displayOptions(self, options, q):
        i = 0
        print("-> ",q,":\n")
        for opt in options:
            print("  ", i , " - ", opt)
            i += 1

    def loadFile(self):
        self.dirs = glob.glob('*')
        i = 0
        for path in self.dirs:
            print("  ",  i, " - ", path)
            i += 1
        path = self.dirs[int(input("-> Select the file id:\n-> "))]
        data = self.readFile(path)
        self.sendMessage(self.sock, 1, data, path)
if __name__ == "__main__":
    host = "localhost"
    port = 3013
    c = Client( host, port)
    c.run()