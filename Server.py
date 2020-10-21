from SocketHandler import SocketHandler
from threading import Thread
from SocketPacket import sPacket as SP
import os
import glob

class Server(SocketHandler):
    def __init__(self, h, p, path):
        super().__init__(h, p)
        self.path = path
        self.clients = []
        self.buckets = []
        self.sock.bind((str(self.host), int(self.port)))
        self.sock.listen(10)
        self.pointer = ""
        
        if (not self.checkDirectory(self.path)):
            print("->Server path doesn't exists")
            self.existSock(self.sock)
        else :
            self.loadBuckets()
        
    def startListener(self):
        conn = Thread(target=self.connection)
        conn.daemon = True
        conn.start()

        while True :
            msg = input("")
            if (msg == 'exit'):
                self.existSock(self.sock)
            
            if (msg == 'create_bucket'):
                self.createBucket()        

    def connection(self):
        print("-> Waiting for connections...")
        while True :
            try:
                conn, addr = self.sock.accept()
                #conn.setblocking(False)
                t = Thread(target=self.process, args=(conn,))
                t.daemon = True
                t.start()
                self.clients.append([conn,t])
                print("-> Client Connected")
            except Exception as e: print(e)

    def process(self, client):
        """
        while True :
            try:
                data = self.recvHeader(client)
                if(data):
                    data = self.parseData(data)
                    self.dictionary(data, client)
                    #self.saveFile(data)
            except Exception as e: print(e)
        """
        while (True):
            data = self.awaitResponse(client)
            self.dictionary(data, client)

    def dictionary(self, data:SP, client):
        comm = data.getComm()
        if (comm == 1 ):
            self.saveFile(data, client)
        if (comm == 2 ):
            pass
        if (comm == 3 ):
            pass
        if (comm == 4 ):
            pass
        if (comm == 5 ):
            pass

    def createBucket(self):
        if (not self.checkDirectory(self.path)):
            print("->Server path doesn't exists")
        else:
            name = str(input("-> Select the bucket name:\n-> "))
            path = os.path.join(self.path, name)
            try:  
                os.mkdir(path)
                self.buckets.append([name, path])
            except:
                print("->Bucket already exists")
            
    def checkDirectory(self, path):
        return os.path.isdir(path)

    def saveFile(self, data:SP, client):
        """
        i = 0
        for buck in self.buckets:
            print("  ",  i, " - ", buck[0])
            i += 1
        ap = int(input("-> Choose the destination bucket:"))
        """
        self.sendMessage(client, 2, self.buckets, "Select the bucket")
        ap = self.awaitResponse(client)

        self.writeFile(self.buckets[ap.getData()][1], data)
        self.sendMessage(client, 0)

    def ls(self, path):
        dirs = glob.glob(path + '\*')
        i = 0
        for path in dirs:
            print("  ",  i, " - ", path)
            i += 1

    def loadBuckets(self):
        dirs = glob.glob(self.path + '\*')
        i = 0
        for path in dirs:
            name = os.path.basename(os.path.normpath(path))
            print("  ",  i, " - ", name)
            self.buckets.append([name, path])
            i += 1

if __name__ == "__main__":
    path = 'D:\Work\Eafit\\2020-2\Telematica\EntregaSockets\MainBucket'
    host = "localhost"
    port = 3013
    s = Server(host, port, path)
    s.startListener()