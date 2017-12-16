from P2P_FileSharingSystem.Peer_Files.PeerListener import *


class Peer_Server:  # Connect Peer with Centeral-Server
    def __init__(self):
        print("WELCOME TO PEER TO PEER SHARING FILE SYSTEM\n")
        while True:
            # Getting Choice From Peer
            Choice = input("TYPE :(1)REGISTER (2) SEARCH (3) DOWNLOAD (4) LIST_ALL (5)EXIT\n")

            if Choice == REGISTER:
                Peer_id = input("Enter PEER ID 4 digit: ")  # Getting PEER_ID
                self.file_name = input("Enter File name: ")  # Getting file_name will be shared
                self.Peer_port = int(Peer_id)  # Convert Peer_port to int and store as attribute
                self.registerInServer()  # connect with server and send command to register the file
                Start_PeerListener(self.Peer_port,
                                   HOST)  # After Register The File Listen to PEER_ID Port for sharing files
            elif Choice == SEARCH:
                self.SearchInServer()  # Connect with server and send command to search for file name


            elif Choice == DOWNLOAD:
                Peer_id = input("Enter PEER ID 4 digit: ")  # Taking PEER_ID and file_name i want to Download file from
                file_name = input("Enter File name: ")
                self.Download(int(Peer_id), file_name)


            elif Choice == LIST_ALL:  # SHOW ALL Sharing files that registered in Server
                self.List_all()

            elif Choice == EXIT:
                break
            else:
                continue

    def registerInServer(self):  # Connect and Send command to Register
        s = socket()
        s.connect((HOST, PORT))
        data = pickle.dumps(self.Regiserdata(self.Peer_port, self.file_name))
        s.send(data)
        state = s.recv(1024)
        print(state.decode('utf-8'))  # Receive Confirmation of Registration
        s.close()

    def SearchInServer(self):  # Connect and Send command  to Server for Specific File_name
        s = socket()
        s.connect((HOST, PORT))
        file_name = input("Enter File Name : ")
        data = pickle.dumps(self.SearchData(file_name))
        s.send(data)
        ret_data = pickle.loads(s.recv(1024))
        self.print_list(ret_data[0], ret_data[1])  # Return List of Files contain that name
        s.close()

    def List_all(self):  # Connect and Send command to Server to Show all Exiting Files
        s = socket()
        s.connect((HOST, PORT))
        data = pickle.dumps(str(LIST_ALL))
        s.send(data)
        ret_data = pickle.loads(s.recv(1024))
        self.print_list(ret_data[0], ret_data[1])  # Return all exiting files
        s.close()

    def Regiserdata(self, Peer_port, file_name):  # for formatting the return to pickle
        return [REGISTER, Peer_port, file_name]

    def print_list(self, Files, keys):  # print all List
        if len(Files) > 0:
            print("Peer_Id  |     File_name    |  Date_added :\n")
            for item in Files:
                print("  ", item[keys[0]], "       ", item[keys[1]], "   ", item[keys[2]])
        else:
            print("There is no file has this name Or There is no file At all\n")

    def SearchData(self, file_name):  # Command for Search contains file_name, SEARCH indicator command
        return [SEARCH, file_name]

    def Download(self, Peer_id, file_name):  # Connect and Send request for downloading from specific PEER_PORT
        s = socket()
        s.connect((HOST, Peer_id))
        data = pickle.dumps([DOWNLOAD, str(file_name)])
        s.send(data)
        ret_data = pickle.loads(s.recv(1024))  # Organizing the path to download files
        file_path = os.path.join(os.getcwd(), '..')
        file_path = os.path.join(file_path, 'SharingFiles')
        file_path = os.path.join(file_path, "downloads")
        with open(os.path.join(file_path, file_name),    # writing to file
                  'wt') as myfile:
            for x in range(0, len(ret_data)):
                myfile.write(ret_data[x])
            myfile.close()
        s.close()
        print('File Downloaded Successfully')


def Start_Peer():
    peer = Peer_Server()  # Start New Peer


if __name__ == '__main__':
    Start_Peer()
