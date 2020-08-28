import tkinter as tk
from ui.module import *
#from ui.lock import Lock
import ui.var

#from utils import can_comm
from utils import nxr_control
import time


class App(tk.Tk):
    def __init__(self, title="NXR", delay=500):
        super().__init__()
        self.title(title)
        self.headtitle=title
        #ui.var.lock = Lock()

        self.nxr()

        self.ui()


        return

    def ui(self):
        ui.var.eid_mod = Target(self)
        ui.var.eid_mod.pack()

        self.onoff = OnOff(self)
        self.onoff.pack()

        self.volt = Volt(self)
        self.volt.pack()
        return

    def nxr(self):
        ui.var.can_dev = nxr_control.NXR_CONTROL(lib_file='./utils/ControlCAN.dll',
                                        can_dev=[1])
        return
