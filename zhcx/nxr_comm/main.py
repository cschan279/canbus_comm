from utils import can_comm
from utils import nxr_comm
from utils import var
import sys

var.can_dev = can_comm.CanComm(lib_file='./utils/ControlCAN.dll',
                               can_dev=[0,1])

var.nxr_port = nxr_comm.NXR_COMM(channel=1)


try:
    print("volt sect start")
    v = var.nxr_port.get_volt(dst=0x01, grp=0x03)
    print(v)

    var.nxr_port.set_volt(dst=0x01, grp=0x03, val=200)
    
    time.sleep(1)
    
    v = var.nxr_port.get_volt(dst=0x01, grp=0x03)
    print(v)

    print("volt sect end")


    print("watt sect start")
    w = var.nxr_port.get_watt(dst=0x01, grp=0x03)
    print(w)

    print("watt sect stop")
finally:
    var.nxr_port.__del__()
    print('end')
    sys.exit()
