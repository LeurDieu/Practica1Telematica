from SocketHandler import SocketHandler
from threading import Thread
from SocketPacket import sPacket as SP
import os
import glob
import shutil
from pathlib import PurePath as PP

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
        while (True):
            data = self.awaitResponse(client)
            self.dictionary(data, client)

    def dictionary(self, data:SP, client):
        comm = data.getComm()
        if (comm == 1 ):
            self.saveFile(data, client)
        if (comm == 2 ):
            self.df(client)
        if (comm == 3 ):
            self.rf(client)
        if (comm == 4 ):
            self.createBucket(client)
        if (comm == 5 ):
            self.removeBucket(client)
        if (comm == 7):
            self.lsf(client)
        if (comm == 8):
            self.lsb(client)

    def createBucket(self, client):
        self.sendMessage(client, 1, self.buckets, "Select the name of the new bucket")
        data = self.awaitResponse(client)

        if (not self.checkDirectory(self.path)):
            print("->Server path doesn't exists")
        else:
            #name = str(input("-> Select the bucket name:\n-> "))
            name = data.getData()
            path = os.path.join(self.path, name)
            try:  
                os.mkdir(path)
                self.buckets.append([name, path])

                self.sendMessage(client, 0)
            except:
                print("->Bucket already exists")
    
    def removeBucket(self, client):
        self.sendMessage(client, 2, self.buckets, "Select the name of the bucket that you want to remove")
        data = self.awaitResponse(client)

        if (not self.checkDirectory(self.path)):
            print("->Server path doesn't exists")
        else:
            data = data.getData()
            try:  
                shutil.rmtree(self.buckets[data][1])
                self.buckets.pop(data)

                self.sendMessage(client, 0)
            except:
                print("->Wrong Bucket ID")
            
    def checkDirectory(self, path):
        return os.path.isdir(path)

    def saveFile(self, data:SP, client):
        self.sendMessage(client, 2, self.buckets, "Select the bucket")
        ap = self.awaitResponse(client)

        self.writeFile(self.buckets[ap.getData()][1], data)
        self.sendMessage(client, 0)

    def df(self, client):
        self.sendMessage(client, 2, self.buckets, "Select the bucket with the file")
        datab = self.awaitResponse(client)

        dirs = self.ls(self.buckets[datab.getData()][0])
        self.sendMessage(client, 2, dirs, "Select the file")
        dataf = self.awaitResponse(client)

        path = dirs[dataf.getData()]
        purepath = PP(path)
        data = self.readFile(path)
        self.sendMessage(client, 3, data, purepath.name)
        self.sendMessage(client, 0)

    def rf(self, client):
        self.sendMessage(client, 2, self.buckets, "Select the bucket with the file")
        datab = self.awaitResponse(client)

        dirs = self.ls(self.buckets[datab.getData()][0])
        self.sendMessage(client, 2, dirs, "Select the file")
        dataf = self.awaitResponse(client)
        
        path = dirs[dataf.getData()]
        os.remove(path)
        self.sendMessage(client, 0)

    def ls(self, name):
        path = os.path.join(self.path, name)
        dirs = glob.glob(path + '\*')
        return dirs
        """
        i = 0

        for path in dirs:
            print("  ",  i, " - ", path)
            i += 1
        """

    def lsb(self, client):
        self.sendMessage(client, 4, self.buckets, "Buckets")
        self.sendMessage(client, 0)

    def lsf(self, client):
        self.sendMessage(client, 2, self.buckets, "Select the bucket with the file")
        datab = self.awaitResponse(client)

        dirs = self.ls(self.buckets[datab.getData()][0])
        self.sendMessage(client, 4, dirs, "Files")
        self.sendMessage(client, 0)
        


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