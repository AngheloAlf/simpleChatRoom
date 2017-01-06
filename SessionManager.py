from ConnectionManager import ConnectionManager


class SessionManager(ConnectionManager):
    def __init__(self, showLogs=False):
        # type: (bool) -> None
        ConnectionManager.__init__(self, showLogs)
        self.ip = ""
        self.port = 0
        self.user = ""

    def connectServer(self, ip, port, userName):
        # type: (str, int, str) -> SessionManager
        if self.connected:
            if self.showLogs:
                print "Ya estas conectado"
            return self
        self.user = userName
        self.connect(ip, port)
        self.send(self.user)
        return self
