from threading import Thread
import traceback
from utils import can_comm, nxr_conv

class NXR_CONTROL:
    def __init__(self, lib_file='./ControlCAN.dll',
                       can_dev=[0]):
        self.can_con = can_comm.CanComm(lib_file=lib_file, can_dev=can_dev)
        self.can_ch = can_dev[0]

        self.sendlist = []
        self.return_buf = {}
        self.loop_ret = True
        return

    def loop(self):
        while self.loop_ret:
            self.send()
            self.read()

    def send(self):
        if not self.sendlist:
            return
        try:
            fid = self.sendlist[0]['fid']
            fdt = self.sendlist[0]['fdt']
            self.can_con.send(self.can_ch, fid, fdt)
            self.sendlist.pop(0)
        except Exception as e:
            traceback.print_exc()
        return

    def read(self):
        try:
            fid, fdt = self.can_con.read(self.can_ch)
            if fid and fdt:
                fm_id = nxr_conv.decode_id(fid)
                fm_dt = nxr_conv.decode_data(fdt)
        except Exception as e:
            traceback.print_exc()
