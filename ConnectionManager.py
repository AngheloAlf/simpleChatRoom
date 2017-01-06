import socket


class ConnectionManager:
    NETBUFFER = 1024
    ERROR = "\x00"

    def __init__(self, showLogs=False):
        # type: (bool) -> None
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.showLogs = showLogs
        self.connected = False
        self.host = ""
        self.ip = ""
        self.port = 0
        self.timeout = None
        self.clients = []

    def __connect(self):
        self.sock.connect((self.ip, self.port))
        self.connected = True
        if self.showLogs:
            print "Conexion correcta\n\tIP:" + self.ip + "\n\tPort:" + str(self.port)

    def connect(self, ip, port):
        # type: (str, int) -> ConnectionManager
        try:
            self.ip = ip
            self.port = port
            self.__connect()
        except socket.timeout:
            try:
                self.ip = ip
                self.port = port
                self.sock = ConnectionManager().sock
                self.__connect()
            except socket.timeout:
                self.connected = False
                print "Ha ocurrido un error al intentar conectar"
        return self

    def bindServer(self, host, port):
        # type: (str, int) -> ConnectionManager
        self.host = host
        self.port = port
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        if self.showLogs:
            print "Servidor creado satisfactoriamente\n\tHost: " + self.host + "\n\tPort: " + str(self.port)
        return self

    def listen(self, backlog=5):
        # type: (int) -> ConnectionManager
        self.sock.listen(backlog)
        return self

    def acceptClient(self, timeout=None):
        # type: (float) -> ConnectionManager
        client, address = self.sock.accept()
        if timeout:
            client.settimeout(timeout)
        username = client.recv(self.NETBUFFER)
        if self.showLogs:
            print "Client connected:\n\tAddress:", address, "\n\tUsername:", username
        self.clients.append((client, address, username))
        return self

    def getLastClient(self):
        return self.clients[-1]

    def sendAllClients(self, msg):
        # type: (str) -> list
        disconnectedClients = list()
        if self.showLogs:
            print "SendAll >>", msg
        for i in self.clients:
            try:
                i[0].send(msg)
            except socket.error:
                disconnectedClients.append(i)
        for i in disconnectedClients:
            self.clients.remove(i)
            if self.showLogs:
                print i[2] + "disconnected"
        return disconnectedClients

    def send(self, packet):
        # type: (str) -> ConnectionManager
        if not self.connected:
            if self.showLogs:
                print "No estas conectado"
            return self
        if self.showLogs:
            print "Send >>", packet
        self.sock.send(packet)
        return self

    def recv(self, netBuffer=None):
        # type: (int) -> str
        if not self.connected:
            if self.showLogs:
                print "No estas conectado"
            return ""
        if not self.sock.gettimeout() is None:
            self.sock.settimeout(None)
        if netBuffer is None:
            recived = self.sock.recv(self.NETBUFFER)
        else:
            recived = self.sock.recv(netBuffer)
        if self.showLogs:
            print "Recv <<", recived
        return recived

    def recvNB(self, timeout=None, netBuffer=None):
        # type: (float, int) -> str

        if not self.connected:
            if self.showLogs:
                print "No estas conectado"
            return self.ERROR
        if self.sock.gettimeout() is None:
            if not (timeout is None):
                self.sock.settimeout(timeout)
            else:
                self.sock.settimeout(self.timeout)

        if netBuffer is None:
            nb = self.NETBUFFER
        else:
            nb = netBuffer

        try:
            recvMsg = self.sock.recv(nb)
            if len(recvMsg) == 0:
                if self.showLogs:
                    print 'Se ha cerrado la conexion de forma inesperada'
                # sys.exit(0)
                return self.ERROR
            else:
                if self.showLogs:
                    print "Recv <<", recvMsg
                return recvMsg
        except socket.timeout, e:
            err = e.args[0]
            if err == 'timed out':
                pass
                # sleep(1)
                # continue
            else:
                if self.showLogs:
                    print e
                # sys.exit(1)
            return ""
        except socket.error, e:
            if self.showLogs:
                print e
            # sys.exit(1)
            self.close()
            return self.ERROR

    def close(self):
        # type: () -> None
        if self.showLogs:
            print "Cerrando socket"
        self.sock.close()
        self.sock = None
        self.connected = False

    def setTimeout(self, timeout):
        # type: (float) -> ConnectionManager
        self.timeout = timeout
        self.sock.settimeout(timeout)
        return self

    def isConnected(self):
        # type () -> bool
        return self.connected

    def getShowLogs(self):
        # type: () -> bool
        return self.showLogs


def recvClient(client, showLogs=False):
    # type: (socket._socketobject) -> str
    try:
        msg = client.recv(ConnectionManager.NETBUFFER)
        if msg:
            if showLogs:
                print "Recv <<", msg
            return msg
        else:
            if showLogs:
                print "Se ha perdido la conexion"
            return ConnectionManager.ERROR
    except socket.error:
        if showLogs:
            print "Se ha perdido la conexion"
        client.close()
        return ConnectionManager.ERROR
