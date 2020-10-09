from utils import can_comm, nxr_conv
import struct


device = can_comm.CanComm(lib_file='./utils/ControlCAN.dll', can_dev=[1])

bc_id, bc_dt = None, None
while bc_id == None:
    bc_id, bc_dt = device.read(1)

print(struct.pack(">I", bc_id))
for i in bc_dt: print(hex(i), end=' ')