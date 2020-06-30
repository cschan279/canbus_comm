import can_comm
import hw_frame

can1 = can_comm.CanComm(lib_file='./ControlCAN.dll', can_dev=[0,1])

id_1 = hw_frame.form_id(ptc=0x0d, addr=0x00, cmd=0x50, src=0x1, cnt=0x0)
data_1 = hw_frame.form_data(fault=0x0, signal=0x0, content=[0x00]*6)

can1.send(0, id_1, data_1)
print(can1.read(0))


#>>> a = 117395581
#>>> b = [0,1,0,0,16,40,42,36]
