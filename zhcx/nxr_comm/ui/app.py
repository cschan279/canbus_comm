import tkinter as tk
from ui.label_input import *

class App(tk.Tk):
    def __init__(self, title="NXR", delay=500):
        super().__init__()
        self.title(title)
        self.headtitle=title
        self.mod = {}

        self.mod['addr'] = LabelSpin(self, text='Addr', val=(0,63))
        self.mod['addr'].pack(side='left')
        self.mod['grp'] = LabelSpin(self, text='Grp', val=(0,63))
        self.mod['grp'].pack(side='right')
        Frame(self).pack()
        self.mod['volt'] = LabelSpin(self, text='volt', val=(0,1000), inc=0.1)
        self.mod['volt'].pack(side='left')
        
