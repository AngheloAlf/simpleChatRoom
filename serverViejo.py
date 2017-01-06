import socket
import threading


def listenToClient(client, address, user, clientList):
    size = 1024
    conectedMsg = user + " is connected"
    print address
    print conectedMsg
    for i in clientList:
        try:
            i.send(conectedMsg)
        except socket.error:
            clientList.remove(i)
            print i, "disconnected"
    while True:
        try:
            data = client.recv(size)
            if data:
                # Set the response to echo back the recieved data
                response = data
                # client.send(response)
                msg = user + ": " + response
                print msg
                for i in clientList:
                    try:
                        i.send(msg)
                    except socket.error:
                        clientList.remove(i)
                        print i, "disconnected"
            else:
                print user, "disconnected"
        except socket.timeout:
            client.close()
            return False


class ThreadedServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        self.sock.listen(5)
        clientList = []
        while True:
            client, address = self.sock.accept()
            # client.settimeout(60)
            user = client.recv(1024)
            clientList.append(client)
            threading.Thread(target=listenToClient, args=(client, address, user, clientList)).start()


if __name__ == "__main__":
    port_num = input("Port? ")
    print "opening on port:", port_num
    ThreadedServer('', port_num).listen()
