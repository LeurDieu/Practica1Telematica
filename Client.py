from SocketHandler import SocketHandler
from SocketPacket import sPacket as SP
import glob
import sys
import os

class Client(SocketHandler):
    def __init__(self, h, p):
        super().__init__(h, p)
        self.sock.connect((str(self.host), int(self.port)))
        self.id = hex(id(self))
        self.dirs = []
    
    def run(self):
        while (True):
            msg = input("-> ")
            
            if (msg == 'exit'):
                self.sock.close()
                sys.exit()
                
            if (msg == 'send_file'):
                self.loadFile()

            while (True):
                res = self.awaitResponse(self.sock)
                if(self.dictionary(res)):
                    break

    def dictionary(self, data:SP):
        comm = data.getComm()
        if (comm == 0):
            return True
        if (comm == 1 ):
            pass
        if (comm == 2 ):
            self.chooseOption(data)

        if (comm == 3 ):
            pass
        if (comm == 4 ):
            pass
        if (comm == 5 ):
            pass
        return False
    def chooseOption(self, data:SP):
        options = data.getData()
        i = 0
        print("-> ",data.getName(),":\n")
        for opt in options:
            print("  ", i , " - ", opt)
            i += 1
        self.sendMessage(self.sock, 6, int(input("->:")))
    
    
    def loadFile(self):
        self.dirs = glob.glob('*')
        i = 0
        for path in self.dirs:
            print("  ",  i, " - ", path)
            i += 1

        #path = self.dirs[int(input("-> Select the file id:\n-> "))]
        path = self.dirs[int(input("-> Select the file id:\n-> "))]
        data = self.readFile(path)
        self.sendMessage(self.sock, 1, data, path)
if __name__ == "__main__":
    host = "localhost"
    port = 3013
    c = Client( host, port)
    c.run()