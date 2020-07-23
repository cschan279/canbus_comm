import can_comm
import hw_frame
import nxr_frame

import time


can1 = can_comm.CanComm(lib_file='./ControlCAN.dll', can_dev=[0,1])

#print('Req_Addr')
#nxr_frame.req_addr(can1)
#print('='*20)

print('Turn Off')
nxr_frame.turn_onoff(can1, 0x01, False)
print('='*20)

print('Req_Volt')
nxr_frame.req_volt(can1, 0x01)
print('='*20)

print('Set_Volt')
nxr_frame.set_volt(can1, 0x01, 350)
print('='*20)
time.sleep(1)

print('Req_Volt')
nxr_frame.req_volt(can1, 0x01)
print('='*20)
'''
print('Turn On')
nxr_frame.turn_onoff(can1, 0x01, True)
print('='*20)
time.sleep(1)
'''
#input('Status is now ON, Press Enter to turn OFF')

for i in range(5):
    print('Turn On')
    nxr_frame.turn_onoff(can1, 0x01, True)
    print('='*20)
    time.sleep(3)

print('Set_Volt')
nxr_frame.set_volt(can1, 0x01, 250)
print('='*20)
time.sleep(1)

print('Req_Volt')
nxr_frame.req_volt(can1, 0x01)
print('='*20)


for i in range(5):
    print('Turn On')
    nxr_frame.turn_onoff(can1, 0x01, True)
    print('='*20)
    time.sleep(3)

print('Set_Volt')
nxr_frame.set_volt(can1, 0x01, 300)
print('='*20)
time.sleep(1)




for i in range(5):
    print('Req_Volt')
    nxr_frame.req_volt(can1, 0x01)
    print('='*20)
    time.sleep(3)



print('Turn Off')
nxr_frame.turn_onoff(can1, 0x01, False)
print('='*20)