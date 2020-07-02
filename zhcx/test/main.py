import can_comm
import hw_frame

can1 = can_comm.CanComm(lib_file='./ControlCAN.dll', can_dev=[0,1])





#>>> a = 117395581 -> 001101 1111111 01010000 0 111110 1
#>>> b = [0,1],[0,0,16,40,42,36]
