from tkinter import Frame, Label, StringVar, Button


class LabelButton(Frame):
    def __init__(self, parent, width=200, height=50,
                 text='Button', font=('Times', 12),
                 command=None):
        Frame.__init__(self, parent, width=width, height=height)
        self.pack_propagate(0)
        self.button = Button(self, text=text, font=font, command=command)
        self.button.pack(fill='both', expand=True)
        return

class LabelVar(Frame):
    def __init__(self, parent, width=200, height=50,
                 text='Var', font=('Times', 12)):
        Frame.__init__(self, parent, width=width, height=height)
        self.pack_propagate(0)

        self.var = StringVar(self)
        self.var.set(text)

        self.label = Label(self, textvariable=self.var, font=font)
        self.label.pack(fill='both', expand=True)

    def set(self, val):
        self.var.set(str(val))
        return
