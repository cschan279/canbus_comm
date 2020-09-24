
#python3.8.0 64位（python 32位要用32位的DLL）
#
from ctypes import *
import os
import time
import serial




class CanComm:
    def __init__(self, dev="/dev/ttyUSB0"):
        self.dev = dev
        
        self.init_comm_dev()

        self.run_ret = True
        return



    def init_comm_dev(self):
        self.ser=serial.Serial(self.dev,115200,timeout=0.5)
        return



    def send(self, can_dev, id_sect, data_sect):
        ubyte_array8 = c_ubyte*8
        data_array = ubyte_array8(*data_sect)
        ubyte_array3 = c_ubyte*3
        reserved_array = ubyte_array3(0, 0 , 0)
        send_obj = VCI_CAN_OBJ(id_sect, 0, 0, 1, 0, 1,  8,
                               data_array, reserved_array)
        ret = self.canLIB.VCI_Transmit(VCI_USBCAN2, 0, can_dev, byref(send_obj), 1)
        if ret == STATUS_OK:
            return True
        else:
            return False

    def read(self, can_dev):
        ubyte_array8 = c_ubyte*8
        data_array = ubyte_array8(0, 0, 0, 0, 0, 0, 0, 0)
        ubyte_array3 = c_ubyte*3
        reserved_array = ubyte_array3(0, 0 , 0)
        #data_array = data_array_cls(0, 0, 0, 0, 0, 0, 0, 0)
        recv_obj = VCI_CAN_OBJ(0x0, 0, 0, 0, 0, 0,  0,
                               data_array, reserved_array)
        ret = self.canLIB.VCI_Receive(VCI_USBCAN2, 0, can_dev,
                                 byref(recv_obj), 2500, 0)
        #while self.run_ret and not ret:
        #    ret = self.canLIB.VCI_Receive(VCI_USBCAN2, 0, can_dev,
        #                                  byref(recv_obj), 2500, 0)
        if ret > 0:
            return recv_obj.ID, list(recv_obj.Data)
        else:
            return None, None

    def __del__(self):
        self.run_ret = False
        self.canLIB.VCI_CloseDevice(VCI_USBCAN2, 0)



if __name__ == "__main__":
    c = CanComm('./ControlCAN.dll', [0,1])
    c.send(0, 33, [1,3,5,7,9,2,4,6])
    print(c.read(1))
