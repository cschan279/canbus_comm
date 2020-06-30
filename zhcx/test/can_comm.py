
#python3.8.0 64位（python 32位要用32位的DLL）
#
from ctypes import *
import os

VCI_USBCAN2 = 4
STATUS_OK = 1
class VCI_INIT_CONFIG(Structure):
    _fields_ = [("AccCode", c_uint),
                ("AccMask", c_uint),
                ("Reserved", c_uint),
                ("Filter", c_ubyte),
                ("Timing0", c_ubyte),
                ("Timing1", c_ubyte),
                ("Mode", c_ubyte)
                ]
class VCI_CAN_OBJ(Structure):
    _fields_ = [("ID", c_uint),
                ("TimeStamp", c_uint),
                ("TimeFlag", c_ubyte),
                ("SendType", c_ubyte),
                ("RemoteFlag", c_ubyte),
                ("ExternFlag", c_ubyte),
                ("DataLen", c_ubyte),
                ("Data", c_ubyte*8),
                ("Reserved", c_ubyte*3)
                ]

data_array_cls = c_ubyte*8
reserved_array_cls = c_ubyte*3
def reserved_array():
    return reserved_array_cls(0, 0 , 0)

def verifylibfile(fname):
    f_ext = os.path.splitext(fname)[1]
    if not os.path.isfile:
        raise ValueError('File not exist')
    if f_ext == ".dll":
        return 1
    elif f_ext == ".so":
        return 2
    else:
        raise ValueError('Unexpected file extension')

class CanComm:
    def __init__(self, lib_file='./ControlCAN.dll',
                       can_dev = [0,1]):
        self.loadLIB(lib_file)
        init_comm_dev()
        self.dev_conn = []
        for i in can_dev:
            self.init_dev_conn(i)
            self.dev_conn.append(i)



    def loadLIB(self, file_dir):
        t = verifylibfile(file_dir)
        if t == 1:
            self.canLIB = windll.LoadLibrary(file_dir)
        elif t == 2:
            self.canDLL = cdll.LoadLibrary(file_dir)
        print(self.canLIB)
        return

    def init_comm_dev(self):
        ret = self.canLIB.VCI_OpenDevice(VCI_USBCAN2, 0, 0)
        if ret == STATUS_OK:
            print('call up VCI_OpenDevice success\r\n')
        if ret != STATUS_OK:
            print('call up VCI_OpenDevice fail\r\n')
        self.vci_initconfig = VCI_INIT_CONFIG(0x80000008, 0xFFFFFFFF, 0,
                                              0, 0x03, 0x1C, 0)
        #波特率125k，正常模式
        return

    def init_dev_conn(self, can_dev):
        ret = canLIB.VCI_InitCAN(VCI_USBCAN2, 0, can_dev, byref(vci_initconfig))
        if ret == STATUS_OK:
            print('connect VCI_InitCAN-{} success\r\n'.format(i))
        else:
            m = 'connect VCI_InitCAN-{} fail\r\n'.format(i)
            raise ConnectionError(m)
        ret = canLIB.VCI_StartCAN(VCI_USBCAN2, 0, can_dev)
        if ret == STATUS_OK:
            print('connect VCI_StartCAN-{} success\r\n'.format(i))
        else:
            m = 'connect VCI_StartCAN-{} fail\r\n'.format(i)
            raise ConnectionError(m)
        return

    def send(self, can_dev, id_sect, data_sect):
        data_array = data_array_cls(*data_sect)
        send_obj = VCI_CAN_OBJ(id_sect, 0, 0, 1, 0, 1,  8,
                               data_array, reserved_array())
        ret = canLIB.VCI_Transmit(VCI_USBCAN2, 0, can_dev, byref(send_obj), 1)
        if ret == STATUS_OK:
            return True
        else:
            return False

    def read(self, can_dev):
        data_array = data_array_cls(0, 0, 0, 0, 0, 0, 0, 0)
        recv_obj = VCI_CAN_OBJ(0x0, 0, 0, 0, 0, 0,  0,
                               data_array, reserved_array())
        ret = canLIB.VCI_Receive(VCI_USBCAN2, 0, 1,
                                 byref(vci_can_obj), 2500, 0)
        while ret <= 0:
            ret = canLIB.VCI_Receive(VCI_USBCAN2, 0, 1,
                                     byref(vci_can_obj), 2500, 0)
        if ret > 0:
            return recv_obj.ID, list(recv_obj.Data)

    def __del__(self):
        canLIB.VCI_CloseDevice(VCI_USBCAN2, 0)



#通道2接收数据
a = ubyte_array(0, 0, 0, 0, 0, 0, 0, 0)
vci_can_obj = VCI_CAN_OBJ(0x0, 0, 0, 0, 0, 0,  0, a, b)#复位接收缓存
ret = canDLL.VCI_Receive(VCI_USBCAN2, 0, 1, byref(vci_can_obj), 2500, 0)
#print(ret)
while ret <= 0:#如果没有接收到数据，一直循环查询接收。
        ret = canDLL.VCI_Receive(VCI_USBCAN2, 0, 1, byref(vci_can_obj), 2500, 0)
if ret > 0:#接收到一帧数据
    print('CAN2通道接收成功\r\n')
    print('ID：')
    print(vci_can_obj.ID)
    print('DataLen：')
    print(vci_can_obj.DataLen)
    print('Data：')
    print(list(vci_can_obj.Data))

#关闭
canDLL.VCI_CloseDevice(VCI_USBCAN2, 0)
