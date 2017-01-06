import SessionManager
import GuiManager
import threading
from functools import partial


def mandarComando(con, gui):
    # type: (SessionManager.SessionManager, GuiManager.GuiManager) -> None
    con.send(gui.getEntries()["Mensaje"].get())


def recvHandler(con, gui):
    # type: (SessionManager.SessionManager, GuiManager.GuiManager) -> None
    while True:
        msg = con.recvNB()
        if msg == con.ERROR:
            # Se ha perdido conexion con el servidor, o algun error
            print "Se ha perdido conexion con el servidor"
            break
        elif msg == "":
            # No se recibio nada
            pass
        else:
            GuiManager.addMsgToText(gui.getEntries()["Chat"], msg)

        if gui.isClose():
            break


def logear(con, gui):
    # type: (SessionManager.SessionManager, GuiManager.GuiManager) -> None
    entries = gui.getEntries()
    ip = entries["IP"].get()
    port = int(entries["Port"].get())
    username = entries["Usuario"].get()
    con.connectServer(ip, port, username)
    if con.isConnected():
        gui.stop()
        gui.addPanel("Mensajes", ["Chat", "Mensaje"], [("Text", "\x00\n"), ("Entry", "")],
                     ["Enviar", partial(mandarComando, con, gui)])
        threading.Thread(target=recvHandler, args=[con, gui]).start()
        gui.start()


def main(showLogs=False, timeout=0.5):
    # type: (bool, float) -> None
    connection = SessionManager.SessionManager(showLogs)
    connection.setTimeout(timeout)

    gui = GuiManager.GuiManager()  # 210 * 2, 180)
    gui.addPanel("Inicio de sesion", ["IP", "Port", "Usuario"],
                 [("Entry", "127.0.0.1"), ("Entry", "443"), ("Entry", "")],
                 ["Logear", partial(logear, connection, gui)])
    gui.start()


if __name__ == '__main__':
    main(True)
