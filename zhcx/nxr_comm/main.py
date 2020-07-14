from utils import can_comm
from utils import nxr_comm
from utils import var

var.can_dev = can_comm.CanComm(lib_file='./utils/ControlCAN.dll',
                               can_dev=[0,1])
                               
var.nxr_port = nxr_comm.NXR_COMM(channel=1)
