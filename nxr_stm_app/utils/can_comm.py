

import os
import time
import serial
import traceback
import struct
from threading import Thread, Event


# Based on the canbus-stm32-485 board 
# with msg format:
# {0xaa [4B-id] [8B-dat] 0xCS}
# -> total:14B
class CanComm:
    def __init__(self, event, dev="/dev/ttyUSB0"):
        self.dev = dev
        self.ser=serial.Serial(self.dev,115200,
                               bytesize=serial.EIGHTBITS, 
                               parity=serial.PARITY_NONE, 
                               stopbits=serial.STOPBITS_ONE,
                               timeout=0.01)
        self.event = event
        
        self.read_buf = []
        self.write_buf = []
        self.th = Thread(target=self.rw_loop)
        self.th.start()
        return

    def rw_loop(self):
        buf = b''
        while self.event.is_set():
            if self.write_buf:
                # send if msg in write_buf
                self.ser.write(self.write_buf.pop(0))
            
            buf_temp = self.ser.read(14)
            if not buf_temp:
                #timeout break
                buf = b''
                continue
            
            buf += buf_temp
            
            if buf[0] != 0xaa:
                # invalid header
                buf = b''
                continue
            
            length = len(buf)
            if length < 14:
                # not completed msg
                continue
            
            cs = 0
            for i in range(1,14):
                cs ^= buf[i]
            if cs != 0:
                # invalid checksum
                buf = b''
                continue
            self.read_buf.append((buf[1:5],buf[5:13]))
            #print('#'*30)
            #print('Received:', (buf[1:5],buf[5:13]))
            #print('#'*30)
            buf = buf[14:]
        return

    def req_send(self, id_sect, data_sect):
        # id_sect->int, data_sect->[byte]*8
        try:
            msg = b'\xaa' + struct.pack(">I", id_sect)
            for i in range(8): 
                msg += struct.pack("B", data_sect[i])
            cs = 0
            for i in range(1,13): cs^=msg[i]
            msg += struct.pack('B',cs)
            tcs = 0
            for i in range(1,14): tcs^=msg[i]
            print('tcs', tcs)
            self.write_buf.append(msg)
            return True
        except Exception as err:
            traceback.print_exc()
            return False
        

    def read(self):
        try:
            buf = self.read_buf.pop(0)
            m_id = struct.unpack(">I",buf[0])[0]
            m_dt = list(buf[1])
            return m_id, m_dt
        except IndexError as err:
            return None, None
        except Exception as err:
            traceback.print_exc()
            return None, None

        



if __name__ == "__main__":
    e = Event()
    e.set()
    c = CanComm(e, "/dev/ttyUSB0")
    c.send(33, [1,3,5,7,9,2,4,6])
    print(c.read())
    e.clear()
