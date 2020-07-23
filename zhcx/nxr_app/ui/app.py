import tkinter as tk
from ui.module import *
from ui.lock import Lock

from utils import can_comm

import time


class App(tk.Tk):
    def __init__(self, title="NXR", delay=500):
        super().__init__()
        self.title(title)
        self.headtitle=title
        self.lock = Lock()

        self.nxr()

        self.ui()


        return

    def ui(self):
        self.eid = Target(self)
        self.eid.pack()

        self.onoff = OnOff(self, self.eid, self.lock)
        self.onoff.pack()

        self.volt = Volt(self, self.eid, self.lock)
        self.volt.pack()
        return

    def nxr(self):
        self.can_dev = can_comm.CanComm(lib_file='./ControlCAN.dll',
                                        can_dev=[0,1])
        return
