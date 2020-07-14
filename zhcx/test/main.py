import can_comm
import hw_frame
import nxr_frame

import time


can1 = can_comm.CanComm(lib_file='./ControlCAN.dll', can_dev=[0,1])

#print('Req_Addr')
#nxr_frame.req_addr(can1)
#print('='*20)

print('Turn On')
nxr_frame.turn_onoff(can1, 0x01, True)
print('='*20)

print('Req_Volt')
nxr_frame.req_volt(can1, 0x01)
print('='*20)

print('Set_Volt')
nxr_frame.set_volt(can1, 0x01, 350)
print('='*20)



input('Status is now ON, Press Enter to turn OFF')

while True:
	print('Turn OFF')
	nxr_frame.turn_onoff(can1, 0x01, False)
	print('='*20)
	time.sleep(3)

print('Status is now OFF')


