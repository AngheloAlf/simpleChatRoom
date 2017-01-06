

import sys
import socket
import threading
from time import sleep
import Tkinter
import ttk
from functools import partial


def sendCommand(entry, sock):
    sock.send(entry.get())


def recvCommand(s):
    try:
        msg = s.recv(4096)
    except socket.timeout, e:
        err = e.args[0]
        # this next if/else is a bit redundant, but illustrates how the
        # timeout exception is setup
        if err == 'timed out':
            sleep(1)
            print 'recv timed out, retry later'

        else:
            print e
            sys.exit(1)
    except socket.error, e:
        # Something else happened, handle error, exit, etc.
        print e
        sys.exit(1)
    else:
        if len(msg) == 0:
            print 'orderly shutdown on server end'
            sys.exit(0)
        else:
            print msg

def recvWhile(s):
    while True:
        try:
            msg = s.recv(4096)
        except socket.timeout, e:
            err = e.args[0]
            if err == 'timed out':
                sleep(1)
                continue
            else:
                print e
                sys.exit(1)
        except socket.error, e:
            print e
            sys.exit(1)
        else:
            if len(msg) == 0:
                print 'orderly shutdown on server end'
                sys.exit(0)
            else:
                print msg
                # got a message do something :)
        sleep(1)

def logear(socketSession, ip, port, user):
    socketSession.connect((ip.get(), int(port.get())))
    socketSession.send(user.get())
    threading.Thread(target=recvWhile, args=[s]).start()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.connect(('127.0.0.1', 443))
s.settimeout(0.05)

programa = Tkinter.Tk()
programa.minsize(210 * 2, 200)

labelframe = ttk.LabelFrame(programa, text="Inicio de sesion")
labelframe.pack(fill="both", expand="yes", side=Tkinter.LEFT)

L1 = ttk.Label(labelframe, text="IP: ")
E1 = ttk.Entry(labelframe)
E1.insert(0, "127.0.0.1")
L1.place(x=0, y=0)
E1.place(x=75, y=0)

L2 = ttk.Label(labelframe, text="Port: ")
E2 = ttk.Entry(labelframe)
E2.insert(0, "444")
L2.place(x=0, y=25)
E2.place(x=75, y=25)

L4 = ttk.Label(labelframe, text="Usuario: ")
E4 = ttk.Entry(labelframe)
E4.insert(0, "")
L4.place(x=0, y=50)
E4.place(x=75, y=50)

B1 = ttk.Button(labelframe, text="Logear", command=partial(logear, s, E1, E2, E4))
B1.place(x=100, y=100)

labelframeComandos = ttk.LabelFrame(programa, text="Mensajes")
labelframeComandos.pack(fill="both", expand="yes", side=Tkinter.LEFT)

L6 = ttk.Label(labelframeComandos, text="Mensaje: ")
E6 = ttk.Entry(labelframeComandos)
L6.place(x=0, y=0)
E6.place(x=75, y=0)

B2 = ttk.Button(labelframeComandos, text="Enviar", command=partial(sendCommand, E6, s))
B2.place(x=10, y=50)
#recvButton = ttk.Button(labelframeComandos, text="Recv", command=partial(recvCommand, s))
#recvButton.place(x=125, y=50)

programa.mainloop()
