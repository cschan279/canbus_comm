import tkinter as tk

class App(tk.Tk):
    def __init__(self, title="NXR", delay=500):
        super().__init__()
        self.title(title)
        self.headtitle=title
        self.mod = {}

        self.mod['addr_lb'] = tk.Label(self, text="Addr")
        self.mod['addr_lb'].pack(side='left')
        self.mod['addr_in'] = tk.Spinbox(self, from_=0, to=63)
        self.mod['addr_in'].pack(side='left')
        
