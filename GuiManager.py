import Tkinter
import ttk


class GuiManager:
    def __init__(self):  # , xOffset, yOffSet):
        # type: (int, int) -> None
        self.gui = Tkinter.Tk()
        # self.gui.minsize(xOffset, yOffSet)
        # self.xOffset = xOffset
        # self.yOffset = yOffSet
        self.entries = dict()
        self.panelsAmmount = 0
        self.height = 0
        self.width = 210

    def addPanel(self, frameName, labels, inputs, button):
        # type: (str, list, list, list) -> GuiManager
        frame = ttk.LabelFrame(self.gui, text=frameName)
        frame.pack(fill="both", expand="yes", side=Tkinter.LEFT)

        yPos = []

        # inputs = [("Entry", "DefaultText")]
        x = 75
        y = 0
        for i in range(len(inputs)):
            # print inputs[i]
            yPos.append(y)
            if inputs[i][0] == "Entry":
                en = ttk.Entry(frame)
                en.insert(0, inputs[i][1])
                en.place(x=x, y=y)
                self.entries[labels[i]] = en
                y += 25
            elif inputs[i][0] == "Text":
                # sc = Tkinter.Scrollbar(frame)
                # sc.place(x=x, y=y)

                te = Tkinter.Text(frame, state="normal", width="38", height="12")  # , yscrollcommand = sc.set)
                te.insert(Tkinter.INSERT, inputs[i][1])
                te.place(x=x, y=y)
                # te.pack(side = Tkinter.LEFT, fill = Tkinter.BOTH)
                self.entries[labels[i]] = te

                # sc.config(command = te.yview)
                te["state"] = "disabled"

                y += 200
                if self.width < 400:
                    self.width = 400

        # labels = ["ip", "port", "usuario"]
        x = 0
        for l in range(len(labels)):
            la = ttk.Label(frame, text=labels[l])
            la.place(x=x, y=yPos[l])
            # print la.winfo_width()
            # print la.winfo_height()
            # print la['width']

        yMax = yPos[-1] + 25

        # button = ["logear"]
        bu = ttk.Button(frame, text=button[0], command=button[1])
        bu.place(x=75, y=yMax+25)

        if yMax + 25 > self.height:
            self.height = yMax + 50

        self.panelsAmmount += 1

        return self
    
    def getEntries(self):
        # type: () -> dict
        return self.entries

    def start(self):
        self.gui.minsize(self.width * self.panelsAmmount, self.height + 20 + 25)
        self.gui.mainloop()

    def stop(self):
        self.gui.destroy()
        del self.gui
        self.entries = dict()
        self.panelsAmmount = 0
        self.height = 0
        self.gui = Tkinter.Tk()

    def isClose(self):
        # () -> bool
        return False


def addMsgToText(txtWid, msg):
    # (Tkinter.Text, str) -> None
    txtWid["state"] = "normal"
    txtWid.insert(Tkinter.END, msg + "\n")
    txtWid.see(Tkinter.END)
    txtWid["state"] = "disabled"
