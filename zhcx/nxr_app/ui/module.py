import tkinter as tk
from ui.label_input import *
from ui.label_output import *

class Target(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.addr = LabelSpin(self, text='Addr', val=(0,63))
        self.addr.pack(side='left')

        self.grp = LabelSpin(self, text='Grp', val=(0,63))
        self.grp.pack(side='left')
        return

    def get_id(self):
        addr = self.addr.get()
        grp = self.grp.get()
        print(addr, grp)
        pass

class Volt(Frame):
    def __init__(self, parent, id_mod, locker):
        Frame.__init__(self, parent)
        self.id_mod = id_mod
        self.locker = locker

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
        self.id_mod.get_id()
        self.val_V.set('XV')
        pass

    def set_volt(self):
        self.id_mod.get_id()
        print(self.entry.get())
        pass

class OnOff(Frame):
    def __init__(self, parent, id_mod, locker):
        Frame.__init__(self, parent)
        self.id_mod = id_mod
        self.locker = locker

        self.onbtn = LabelButton(self, width=100, text='Turn On',
                                 command=self.turn_on)
        self.onbtn.pack(side='left')
        self.offbtn = LabelButton(self, width=100, text='Turn Off',
                                 command=self.turn_off)
        self.offbtn.pack(side='left')

    def turn_on(self):
        self.id_mod.get_id()
        print('turn on')
        pass

    def turn_off(self):
        self.id_mod.get_id()
        print('turn off')
        pass
