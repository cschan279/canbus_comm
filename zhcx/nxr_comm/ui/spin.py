from tkinter import Frame, Spinbox, Label


class LabelSpin(Frame):
    def __init__(self, parent, width=400, height=50,
                 text='spinbox', val=(0,100),
                 font=('Times', 12))):
        Frame.__init__(self, parent, width=width, height=height)
        self.pack_propagate(0)

        self.f1 = Frame(self, width=width//2, height=height)
        self.f1.pack_propagate(0)
        self.f1.pack(side='left')

        self.f2 = Frame(self, width=width//2, height=height)
        self.f2.pack_propagate(0)
        self.f2.pack(side='left')

        self.lb = Label(self.f1, text=text)
        self.lb.pack(fill='both',  expand=True)

        self.sp = Spinbox(self.f2, from_=val[0], to=val[1])
        self.sp.pack(fill='both',  expand=True)

    def get(self):
        return self.sp.get()
