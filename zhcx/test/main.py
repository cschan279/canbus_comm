import can_comm
import hw_frame
import nxr_frame

can1 = can_comm.CanComm(lib_file='./ControlCAN.dll', can_dev=[0,1])

nxr_frame.req_addr(can1)

nxr_frame.req_volt(can1, 0x01)
