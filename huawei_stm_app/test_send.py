from utils import can_comm
from utils import hwi_conv

from threading import Event

event = Event()
event.set()

can_dev = can_comm.CanComm(event, 'COM18')
print("#####_Send_#####")
rid = hwi_conv.encode_id(dst=0xff,cmd=0x81,ms=0x1, cnt=0x0)
dt_ls = hwi_conv.encode_data(errc=0x0, rid=0x13a, rdt=[1], rtp=[1,">H",4])
hwi_conv.print_bin_id(rid)
hwi_conv.print_hex_ls(dt_ls)
can_dev.req_send(rid, dt_ls)
print("#####_Read_#####")
count = 0
rid, cnt = 0, 0
rid, dt_ls = can_dev.read()
if rid:
    pro, src, cmd, ms, cnt = hwi_conv.decode_id(rid)
while cnt or not rid:
    rid, dt_ls = can_dev.read()
    if rid: 
        pro, src, cmd, ms, cnt = hwi_conv.decode_id(rid)
        hwi_conv.print_bin_id(rid)
        hwi_conv.print_hex_ls(dt_ls)
        count += 1
        if count >5:
            print("too much break")
            break

event.clear()
print("#####_End_#####")

exit()