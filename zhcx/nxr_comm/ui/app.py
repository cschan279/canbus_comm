import tkinter as tk
from ui.label_input import *
from ui.label_output import *

class App(tk.Tk):
    def __init__(self, title="NXR", delay=500):
        super().__init__()
        self.title(title)
        self.headtitle=title
        self.mod = {}

        self.mod['addr'] = LabelSpin(self, text='Addr', val=(0,63))
        self.mod['addr'].grid(row=0, column=0, columnspan=2)
        self.mod['grp'] = LabelSpin(self, text='Grp', val=(0,63))
        self.mod['grp'].grid(row=0, column=2, columnspan=2)

        self.mod['volt'] = LabelSpin(self, text='Output Voltage', width=200,
                                     val=(0,1000), inc=0.1)
        self.mod['volt'].grid(row=1, column=0)
        self.mod['setV'] = LabelButton(self, width=100, text='Set_V',
                                       command=None)
        self.mod['setV'].grid(row=1, column=1)
        self.mod['getV'] = LabelButton(self, width=100, text='Get_V',
                                       command=None)
        self.mod['getV'].grid(row=1, column=2)
        self.mod['valV'] = LabelVar(self, text='0V', width=100)
        self.mod['valV'].grid(row=1, column=3)
