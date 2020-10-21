import socket
import struct
import pickle
import sys
import os
from SocketPacket import sPacket as SP

class SocketHandler:
    def __init__(self, h, p):
        self.host = h
        self.port = p
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def recvHeader(self, sock):
        # Read message length and unpack it into an integer
        
        raw_msglen = self.recvAll(sock, 4)
        if not raw_msglen:
            return None
        msglen = struct.unpack('>I', raw_msglen)[0]
        # Read the message data
        return self.recvAll(sock, msglen)

    def recvAll(self, sock, n):
        # Helper function to recv n bytes or return None if EOF is hit
        data = bytearray()
        while len(data) < n:
            packet = sock.recv(n - len(data))
            if not packet:
                return None
            data.extend(packet)
        return data

    def parseData(self, data):
        out = pickle.loads(data)
        return out

    def readFile(self, path):
        tmpFile = open(path, 'rb')
        binary = tmpFile.read()
        tmpFile.close()
        return binary

    def sendMessage(self, sock, comm, *args):
        if (len(args) > 0):
            if (len(args) > 1):
                data = SP(comm, args[0], args[1])
            else :
                data = SP(comm, args[0])
        else :
            data = SP(comm)

        msg = pickle.dumps(data)
        lenmsg = struct.pack('>I', len(msg))

        sock.sendall(lenmsg)
        sock.sendall(msg)
        print("-> Request Sent")

    def existSock(self, sock):
        self.sock.close()
        sys.exit()
    
    def writeFile(self, path, data:SP):
        file = open(os.path.join(path,data.getName()), "wb")
        file. write(data.getData())
        file. close()

    def awaitResponse(self, sock):
        while True :
            try:
                data = self.recvHeader(sock)
                if(data):
                    data = self.parseData(data)
                    return data
            except Exception as e: print(e)


            
