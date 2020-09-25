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

        self.entry = LabelSpin(self, text='Target Voltage', width=200,
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
        #print('ui.var.can_dev', ui.var.can_dev)
        try:
            ret, volt = ui.var.can_dev.req(addr, grp, nxr_control.get_volt_id)
            if ret:
                val = f"{int(volt*100)/100}V"
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
            ret, val = ui.var.can_dev.set(addr, grp, nxr_control.set_volt_id, val, True)
            return ret
        except Exception as e:
            print(e)
            traceback.print_exc()
        return

class Curr(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.entry = LabelSpin(self, text='Target Current', width=200,
                               val=(0,1000), inc=0.1)
        self.entry.pack(side='left')

        self.set_A = LabelButton(self, width=100, text='Set_A',
                                 command=self.set_curr)
        self.set_A.pack(side='left')

        self.get_A = LabelButton(self, width=100, text='Get_A',
                                 command=self.get_curr)
        self.get_A.pack(side='left')

        self.val_A = LabelVar(self, text='0A', width=100)
        self.val_A.pack(side='left')
        return

    def get_curr(self):
        addr, grp = ui.var.eid_mod.get_id()
        val = '--A'
        #print('ui.var.can_dev', ui.var.can_dev)
        try:
            ret, curr = ui.var.can_dev.req(addr, grp, nxr_control.get_curr_id)
            if ret:
                val = f"{int(curr*100)/100}A"
        except Exception as e:
            print(e)
            traceback.print_exc()
        self.val_A.set(val)
        return

    def set_curr(self):
        addr, grp = ui.var.eid_mod.get_id()
        print('ui.var.can_dev', ui.var.can_dev)
        val = int(float(self.entry.get())*10)
        try:
            ret, val = ui.var.can_dev.set(addr, grp, nxr_control.set_curr_id,
                                    val, False)
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
            ret, val = ui.var.can_dev.set(addr, grp, nxr_control.set_onoff_id,
                                    0x000000, False)
            print("Turn ON:", ret, val)
        except Exception as e:
            print(e)
            traceback.print_exc()
        return

    def turn_off(self):
        addr, grp = ui.var.eid_mod.get_id()
        print('turn off')
        try:
            ret, val = ui.var.can_dev.set(addr, grp, nxr_control.set_onoff_id,
                                    0x010000, False)
            print("Turn OFF:", ret, val)
        except Exception as e:
            print(e)
            traceback.print_exc()
        return

class Stat(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.get_S = LabelButton(self, width=100, text='Get_Status',
                                 command=self.get_status)
        self.get_S.pack(side='left')

        self.default = ' '.join(['----']*8)

        self.val_S = LabelVar(self, text=self.default, width=400)
        self.val_S.pack(side='left')
        return

    def get_status(self):
        addr, grp = ui.var.eid_mod.get_id()
        val = self.default
        #print('ui.var.can_dev', ui.var.can_dev)
        try:
            ret, stat = ui.var.can_dev.req(addr, grp, nxr_control.get_status_id)
            if ret:
                sl = list(f"{stat:032b}")
                for i in range(32,0,-4): sl.insert(i, " ")
                val = ''.join(sl[::-1])
        except Exception as e:
            print(e)
            traceback.print_exc()
        self.val_S.set(val)
        return


class Custom(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.id_entry = LabelSpin(self, text='Target ID', width=200,
                               val=(0,100), inc=1)
        self.id_entry.pack(side='left')

        self.dat_entry = CheckSpin(self, width=200, val=(0,100000), inc=0.1)
        self.dat_entry.pack(side='left')

        self.set = LabelButton(self, width=100, text='Set_Val',
                                 command=self.set_val)
        self.set.pack(side='left')

        self.get = LabelButton(self, width=100, text='Get_Val',
                                 command=self.get_val)
        self.get.pack(side='left')

        self.num_val = LabelVar(self, text='0A', width=100)
        self.num_val.pack(side='left')
        return

    def get_val(self):
        addr, grp = ui.var.eid_mod.get_id()
        val = '--(unit)'
        #print('ui.var.can_dev', ui.var.can_dev)
        try:
            ret, val = ui.var.can_dev.req(addr, grp, int(self.id_entry.get()))
            if ret:
                val = f"{int(val*100)/100}(unit)"
        except Exception as e:
            print(e)
            traceback.print_exc()
        self.num_val.set(val)
        return

    def set_val(self):
        addr, grp = ui.var.eid_mod.get_id()
        print('ui.var.can_dev', ui.var.can_dev)
        isfloat, val = self.dat_entry.get()
        try:
            ret, val  = ui.var.can_dev.set(addr, grp, int(self.id_entry.get()), val, isfloat)
            if ret:
                val = f"{int(val*100)/100}(unit)"
            return ret
        except Exception as e:
            print(e)
            traceback.print_exc()
            val = '--(unit)'
        self.num_val.set(val)
        return
