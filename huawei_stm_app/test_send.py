from utils import can_comm
from utils import hwi_conv

from threading import Event

event = Event()
event.set()

can_dev = can_comm.CanComm(event, 'COM18')
print("#####_Send_#####")
rid = encode_id(dst=0x01,cmd=0xff,ms=0x1, cnt=0x0)
dt_ls = encode_data(errc=0x0, rid=0xfff, rdt=[0], rtp=[6])
print_bin_id(rid)
print_hex_ls(dt_ls)
can_dev.req_send(rid, dt_ls)
print("#####_Read_#####")
rid = None
while not rid:
    rid, dt_ls = can_dev.read()
print_bin_id(rid)
print_hex_ls(dt_ls)
