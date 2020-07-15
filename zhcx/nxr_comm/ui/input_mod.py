from tkinter import Frame, Label, Spinbox, StringVar, OptionMenu


class LabelSpin(Frame):
    def __init__(self, parent, width=400, height=50,
                 text='spinbox', val=(0,100),
                 font=('Times', 12), ratio=0.5):
        Frame.__init__(self, parent, width=width, height=height)
        self.pack_propagate(0)

        self.f1 = Frame(self, width=int(width*ratio), height=height)
        self.f1.pack_propagate(0)
        self.f1.pack(side='left')

        self.f2 = Frame(self, width=int(width*(1-ratio)), height=height)
        self.f2.pack_propagate(0)
        self.f2.pack(side='left')

        self.lb = Label(self.f1, text=text, font=font)
        self.lb.pack(fill='both',  expand=True)

        self.sp = Spinbox(self.f2, from_=val[0], to=val[1], font=font)
        self.sp.pack(fill='both',  expand=True)

    def get(self):
        return self.sp.get()

class LabelMenu(Frame):
    def __init__(self, parent, width=400, height=50,
                 text="Menu", val={"item#1":1, "item#2":2},
                 font=('Times', 12), ratio=0.5):
        Frame.__init__(self, parent, width=width, height=height)
        self.pack_propagate(0)

        self.f1 = Frame(self, width=int(width*ratio), height=height)
        self.f1.pack_propagate(0)
        self.f1.pack(side='left')

        self.f2 = Frame(self, width=int(width*(1-ratio)), height=height)
        self.f2.pack_propagate(0)
        self.f2.pack(side='left')

        self.lb = Label(self.f1, text=text, font=font)
        self.lb.pack(fill='both',  expand=True)

        self.dic = {str(i):val[i] for i in val}
        self.opt = [i for i in self.dic]
        self.var = StringVar(self)
        self.var.set(self.opt[0])

        print(self.opt)
        self.mn = OptionMenu(self.f2, self.var, *self.opt)
        self.mn.pack(fill='both',  expand=True)

    def get(self):
        return self.dic[self.var.get()]
