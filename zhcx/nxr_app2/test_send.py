from utils import can_comm, nxr_conv
import struct


device = can_comm.CanComm(lib_file='./utils/ControlCAN.dll', can_dev=[1])

bc_id = nxr_conv.encode_id(ptp=False, dst=0xfe, src=0xf0, grp=0x3)
bc_dt = nxr_conv.encode_data(func=0x10, rid=0x43, rdt=0, isfloat=False)
print(struct.pack(">I", bc_id))
for i in bc_dt: print(hex(i), end=' ')
print()
device.send(1, bc_id, bc_dt)