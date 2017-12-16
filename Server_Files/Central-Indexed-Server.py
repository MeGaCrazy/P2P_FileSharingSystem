import pickle
import threading
from datetime import datetime
from socket import *
from threading import *

from P2P_FileSharingSystem.Constants.Constant import *


class Server(threading.Thread):
    def __init__(self, port, host, max_connection):
        threading.Thread.__init__(self)
        self.host = 'localhost'
        self.semaphore = Semaphore(max_connection)  # For Handling threads synchronization
        self.port = 5555  # this port it will listen to
        self.sock = socket()
        self.sock.bind((self.host, self.port))  # bind socket to address
        self.sock.listen(max_connection)
        self.Files = []
        self.keys = ['peer_id', 'file_name', 'Date_added']
        print("Server Start listening on", self.host, " : ", self.port)

    def run(self):
        while True:
            conn, addr = self.sock.accept()
            print("Got Connection From ", addr[0], " : ", addr[1])
            request = pickle.loads(conn.recv(1024))

            if request[0] == REGISTER:  # Register File and Send Confirmation Msg
                print("Peer ", addr[1], " ,Add New File\n")
                self.semaphore.acquire()
                self.register(request[1], request[2], str(datetime.now()))
                ret = "File Registered Successfully,"
                conn.send(bytes(ret, 'utf-8'))
                self.semaphore.release()
                conn.close()


            elif request[0] == SEARCH:  # Search for File_Name and return List of Files That Match the name
                print("Peer ", addr[1], " ,Searching For a File\n")
                self.semaphore.acquire()
                ret_data = pickle.dumps(self.Search_data(request[1]))
                conn.send(ret_data)
                self.semaphore.release()
                conn.close()



            elif request[0] == LIST_ALL:  # List All Exiting Files and return as a object with pickle
                print("Peer ", addr[1], " ,Listing all Exiting Files\n")
                self.semaphore.acquire()
                ret_data = pickle.dumps(self.all_data())
                conn.send(ret_data)
                self.semaphore.release()
                conn.close()


            else:
                continue

    def register(self, peer_id, file_name, Date):  # Store all Files in format
        entry = [str(peer_id), file_name, str(Date)]  # peer_id', 'file_name', 'Date_added'
        self.Files.insert(0, dict(zip(self.keys, entry)))

    def Search_data(self, file_name):  # Return File Match name we Search For
        ret = []
        for item in self.Files:
            if item['file_name'] == file_name:
                entry = [item['peer_id'], item['file_name'], item['Date_added']]
                ret.insert(0, dict(zip(self.keys, entry)))
        return ret, self.keys

    def all_data(self):  # Return all Exiting Files
        return self.Files, self.keys


def Start_Server():
    print("Welcome!!..CENTRAL INDEX SERVER IS UP AND RUNNING.\n")
    server = Server(HOST, PORT, 5)  # Start the Central Server
    server.start()


if __name__ == '__main__':
    Start_Server()
