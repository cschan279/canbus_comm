from utils import can_comm
from utils import nxr_comm
from utils import var
import sys

var.can_dev = can_comm.CanComm(lib_file='./utils/ControlCAN.dll',
                               can_dev=[0,1])

var.nxr_port = nxr_comm.NXR_COMM(channel=1)



print("volt sect start")
var.nxr_port.set_volt(dst=0x01, grp=0x03, val=200)

v = var.nxr_port.get_volt(dst=0x01, grp=0x03)
print(v)

print("volt sect end")


print("watt sect start")
w = var.nxr_port.get_watt(dst=0x01, grp=0x03)
print(w)

print("watt sect stop")

del var.nxr_port
print('end')
sys.exit() 