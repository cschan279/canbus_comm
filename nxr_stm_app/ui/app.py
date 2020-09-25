import tkinter as tk
from ui.module import *
#from ui.lock import Lock
import ui.var

#from utils import can_comm
from utils import nxr_control
import time
from threading import Event
import traceback


class App(tk.Tk):
    def __init__(self, title="NXR", delay=500):
        super().__init__()
        self.title(title)
        self.headtitle=title
        #ui.var.lock = Lock()
        ui.var.event = Event()
        ui.var.event.set()

        self.nxr()

        self.ui()

        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.bind('<Escape>', self.on_close)
        self.update()
        return

    def ui(self):
        ui.var.eid_mod = Target(self)
        ui.var.eid_mod.pack()

        self.onoff = OnOff(self)
        self.onoff.pack()

        self.volt = Volt(self)
        self.volt.pack()

        self.curr = Curr(self)
        self.curr.pack()

        self.stat = Stat(self)
        self.stat.pack()

        self.custom = Custom(self)
        self.custom.pack()
        return

    def nxr(self):
        ui.var.can_dev = nxr_control.NXR_CONTROL(ui.var.event, dev='/dev/ttyUSB0')
        return
    
    def getup(self, ts, addr, grp, vid):
        try:
            # {"time":t, "rdt":rdt, "err":err}
            packVal = ui.var.can_dev.return_buf[grp][addr][vid]
            if packVal['err']: return False, 0
            if packVal['time']>=(ts+3): return False, 0
            return True, packVal['rdt']
        except KeyError:
            return False, 0
        except Exception as err:
            traceback.print_exc()
            return False, 0
    
    def update(self):
        try:
            t = time.time()
            addr, grp = ui.var.eid_mod.get_id()
            ret, volt = self.getup(t, addr, grp, nxr_control.get_volt_id)
            if ret:
                self.volt.val_V.set(volt)
            ret, curr = self.getup(t, addr, grp, nxr_control.get_curr_id)
            if ret:
                self.volt.val_A.set(curr)
            ret, stat = self.getup(t, addr, grp, nxr_control.get_status_id)
            if ret:
                sl = list(f"{stat:032b}")
                for i in range(32,0,-4): sl.insert(i, " ")
                val = ''.join(sl[::-1])
                self.stat.val_S.set(val)
        except Exception as err:
            traceback.print_exc()
        self.after(1, self.update)

    def on_close(self):
        ui.var.event.clear()
        self.destroy()
        return
