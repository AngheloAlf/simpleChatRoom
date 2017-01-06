import threading
import ConnectionManager


def listenClient(con):
    # type: (ConnectionManager.ConnectionManager) -> None
    client = con.getLastClient()
    connectedMsg = client[2] + " is connected"
    con.sendAllClients(connectedMsg)
    while True:
        msg = ConnectionManager.recvClient(client[0], con.getShowLogs())
        if msg == con.ERROR:
            print client[2], "disconnected"
            break
        else:
            con.sendAllClients(client[2] + ": " + msg)


def main():
    server = ConnectionManager.ConnectionManager(True)
    server.bindServer("127.0.0.1", 443)
    server.listen()
    print "Escuchando..."
    while True:
        server.acceptClient()
        threading.Thread(target=listenClient, args=[server]).start()

if __name__ == '__main__':
    main()
