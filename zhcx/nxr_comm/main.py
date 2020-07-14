from utils import can_comm
from utils import nxr_comm
from utils import var

var.can_dev = can_comm.CanComm(lib_file='./utils/ControlCAN.dll',
                               can_dev=[0,1])

var.nxr_port = nxr_comm.NXR_COMM(channel=1)


var.nxr_port.config(dst=0x01, grp=0x03, reg=0x0021, flt=True, val=250)

while True:
    var.nxr_port.config(dst=0x01, grp=0x03, reg=0x0030, flt=False, val=0)
