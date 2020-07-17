from utils import can_port
from utils import nxr_ctr
from utils import var
import sys, time

var.can_dev = can_port.CanComm(lib_file='./utils/ControlCAN.dll',
                               can_dev=[0,1])

var.nxr_port = nxr_ctr.N_CTR(channel=1, addrs=[(1,3)])


try:
    print("volt sect start")
    v = var.nxr_port.get_volt(addr_id=0)
    print(v)

    var.nxr_port.set_volt(addr_id=0, val=250)

    time.sleep(1)

    v = var.nxr_port.get_volt(addr_id=0)
    print(v)

    print("volt sect end\n", "#"*20)


    print("watt sect start")
    w = var.nxr_port.get_curr(addr_id=0)
    print(w)

    print("watt sect stop\n", "#"*20)

    print("curr sect start")
    w = var.nxr_port.get_curr(addr_id=0)
    print(w)

    print("curr sect stop\n", "#"*20)
except Exception as e:
	print(e)
finally:
    del var.nxr_port
    print('end')
    sys.exit()
