import tkinter as tk
import traceback
from ui.label_input import *
from ui.label_output import *
import ui.var
from utils import nxr_control

class Target(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.addr = LabelSpin(self, text='Addr', val=(0,63))
        self.addr.pack(side='left')

        self.grp = LabelSpin(self, text='Grp', val=(0,63))
        self.grp.pack(side='left')
        return

    def get_id(self):
        addr = int(self.addr.get())
        grp = int(self.grp.get())
        print(addr, grp)
        return addr, grp

class Volt(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.entry = LabelSpin(self, text='Output Voltage', width=200,
                               val=(0,1000), inc=0.1)
        self.entry.pack(side='left')

        self.set_V = LabelButton(self, width=100, text='Set_V',
                                 command=self.set_volt)
        self.set_V.pack(side='left')

        self.get_V = LabelButton(self, width=100, text='Get_V',
                                 command=self.get_volt)
        self.get_V.pack(side='left')

        self.val_V = LabelVar(self, text='0V', width=100)
        self.val_V.pack(side='left')
        return

    def get_volt(self):
        addr, grp = ui.var.eid_mod.get_id()
        val = '--V'
        print('ui.var.can_dev', ui.var.can_dev)
        #flag = ui.var.lock.getlock()
        try:
            ret, volt = ui.var.can_dev.req(addr, grp, nxr_control.volt_id)
            if ret:
                val = f"{volt}V"
        except Exception as e:
            print(e)
            traceback.print_exc()
        self.val_V.set(val)
        return

    def set_volt(self):
        addr, grp = ui.var.eid_mod.get_id()
        print('ui.var.can_dev', ui.var.can_dev)
        val = float(self.entry.get())
        try:
            ret= ui.var.can_dev.set(addr, grp, nxr_control.volt_id, val, True)
            return ret
        except Exception as e:
            print(e)
            traceback.print_exc()
        return

class OnOff(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.onbtn = LabelButton(self, width=100, text='Turn On',
                                 command=self.turn_on)
        self.onbtn.pack(side='left')
        self.offbtn = LabelButton(self, width=100, text='Turn Off',
                                 command=self.turn_off)
        self.offbtn.pack(side='left')

    def turn_on(self):
        addr, grp = ui.var.eid_mod.get_id()
        print('turn on')
        try:
            ret= ui.var.can_dev.set(addr, grp, nxr_control.onoff_id, 0, False)
        except Exception as e:
            print(e)
            traceback.print_exc()
        return

    def turn_off(self):
        addr, grp = ui.var.eid_mod.get_id()
        print('turn off')
        try:
            ret= ui.var.can_dev.set(addr, grp, nxr_control.onoff_id, 0x10000, False)
        except Exception as e:
            print(e)
            traceback.print_exc()
        return
