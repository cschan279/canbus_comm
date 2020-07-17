from utils import can_port
from utils import nxr_ctr
from utils import var
import sys, time

var.can_dev = can_port.CanComm(lib_file='./utils/ControlCAN.dll',
                               can_dev=[0,1])

var.nxr_port = nxr_comm.N_CTR(channel=1, addrs=[(1,3)])


try:
    print("volt sect start")
    v = var.nxr_port.get_volt(addr_id=0)
    print(v)

    var.nxr_port.set_volt(addr_id=0, val=250)

    time.sleep(1)

    v = var.nxr_port.get_volt(addr_id=0)
    print(v)

    print("volt sect end")


    print("watt sect start")
    w = var.nxr_port.get_watt(addr_id=0)
    print(w)

    print("watt sect stop")
except Exception as e:
	print(e)
finally:
    var.nxr_port.__del__()
    print('end')
    sys.exit()
