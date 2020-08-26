from threading import Thread
from utils import can_comm, nxr_conv

class NXR_CONTROL:
    def __init__(self, lib_file='./ControlCAN.dll',
                       can_dev=[0]):
        self.can_con = can_comm.CanComm(lib_file=lib_file, can_dev=can_dev)

        self.return_buf = {}
        self.loop_ret = True
        return

    def loop(self):
        while self.loop_ret:
            pass
