import tkinter as tk
import traceback
from ui.label_input import *
from ui.label_output import *
import ui.var
from utils import nxr_frame

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
        flag = ui.var.lock.getlock()
        try:
            volt = nxr_frame.req_volt(ui.var.can_dev, addr, grp)
            val = volt + 'V'
        except Exception as e:
            print(e)
            traceback.print_exc()
        ui.var.lock.unlock(flag)

        self.val_V.set(val)
        return

    def set_volt(self):
        addr, grp = ui.var.eid_mod.get_id()
        print('ui.var.can_dev', ui.var.can_dev)
        val = float(self.entry.get())
        flag = ui.var.lock.getlock()
        try:
            nxr_frame.set_volt(ui.var.can_dev, addr, val, grp)
        except Exception as e:
            print(e)
            traceback.print_exc()
        ui.var.lock.unlock(flag)
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


        flag = ui.var.lock.getlock()
        try:
            nxr_frame.turn_onoff(ui.var.can_dev, addr, True, grp)
        except Exception as e:
            print(e)
            traceback.print_exc()
        ui.var.lock.unlock(flag)
        return

    def turn_off(self):
        addr, grp = ui.var.eid_mod.get_id()
        print('turn off')


        flag = ui.var.lock.getlock()
        try:
            nxr_frame.turn_onoff(ui.var.can_dev, addr, False, grp)
        except Exception as e:
            print(e)
            traceback.print_exc()
        ui.var.lock.unlock(flag)
        return
