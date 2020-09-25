
#python3.8.0 64位（python 32位要用32位的DLL）
#

import os
import time


def assert_var(var, typ, len_limit):
    wn = "Wrong type: {} {}".format(type(var), str(typ))
    assert isinstance(var, typ), wn
    wn = "Out of range: 0<{}<{}".format(var, 2**len_limit)
    assert var >= 0 and var < 2**len_limit, wn
    return

def ext_id(ptp=0x0, dst=0xff, src=0xf0, grp=0x0):
    val_len = (1,8,8,3)
    var = (ptp, dst, src, grp)
    res = 0x060
    for i in range(4):
        assert_var(var[i], int, val_len[i])
        res = res << val_len[i]
        res += var[i]
        #print('id', res)
    return res




def id_ext(id_num):
    rest, grp = divmod(id_num, 2**3)
    rest, src = divmod(rest, 2**8)
    rest, dst = divmod(rest, 2**8)
    pro, ptp = divmod(rest, 2**1)
    #rest, pro = divmod(rest, 2**9)
    return pro, ptp, dst, src, grp

def printlsHex(ls, endc='\n'):
    #print(ls)
    ls_out = [hex(i) if isinstance(i, int) else i for i in ls]
    print(ls_out, end=endc)
    return

class CanComm:
    def __init__(self, lib_file='./ControlCAN.dll',
                       can_dev=[0,1]):
        self.lib_file = lib_file
        print('<{}>'.format(self.lib_file))
        self.return_msg = None

        self.dev_conn = []




    def send(self, can_dev, id_sect, data_sect):
        print('Send:', end=" ")
        printlsHex(id_ext(id_sect), endc="\t")
        printlsHex(data_sect, endc="\n")
        if data_sect[0] == 0x10:
            _, a, b, c, d = id_ext(id_sect)
            rid = ext_id(a, c, b, d)
            rdt = data_sect
            rdt[0] = 0x41
            rdt[1] = 0xf0
            self.return_msg = (rid, rdt)
        else:
            self.return_msg = None
        return True

    def read(self, can_dev):
        time.sleep(0.5)
        if self.return_msg:
            return self.return_msg
        else:
            return None, None

    def __del__(self):
        print('can_dev closed')



if __name__ == "__main__":
    c = CanComm('./ControlCAN.dll', [0,1])
    c.send(0, 33, [1,3,5,7,9,2,4,6])
    print(c.read(1))
