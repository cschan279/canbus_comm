#from utils import can_port
from utils import dum_port
from utils import nxr_ctr
from utils import var
import traceback
import sys, time

var.can_dev = dum_port.CanComm(lib_file='./utils/ControlCAN.dll',
                               can_dev=[0,1])

var.nxr_port = nxr_ctr.N_CTR(channel=1, addrs=[(1,3)])

def countdown(t):
    for i in range(t):
        print(t-i, '...')
        time.sleep(1)
    return

try:
    print("volt sect start")
    v = var.nxr_port.get_volt(addr_id=0)
    print(v)

    var.nxr_port.set_volt(addr_id=0, val=250)

    time.sleep(1)

    v = var.nxr_port.get_volt(addr_id=0)
    print(v)

    print("volt sect end\n", "#"*20)

    countdown(5)

    print("volt sect start")
    v = var.nxr_port.get_volt(addr_id=0)
    print(v)

    var.nxr_port.set_volt(addr_id=0, val=150)

    time.sleep(1)

    v = var.nxr_port.get_volt(addr_id=0)
    print(v)

    print("volt sect end\n", "#"*20)
    #print("curr sect start")
    #c = var.nxr_port.get_curr(addr_id=0)
    #print(c)

    #print("curr sect stop\n", "#"*20)

    var.nxr_port.set_onoff(0, True)
except Exception as e:
    print(e)
    traceback.print_exc()


del var.nxr_port
print('end')
sys.exit()
