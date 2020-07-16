from . import can_comm
from . import var

import struct
import time
from threading import Thread


def assert_var(var, typ, len_limit):
    wn = "Wrong type: {}/{}".format(str(type(var)), str(typ))
    assert isinstance(var, typ), wn
    wn = "Out of range: 0<{}<{}".format(var, 2**len_limit)
    assert var >= 0 and var < 2**len_limit, wn
    return

def ls2f(ls):
    ls.reverse()
    return struct.unpack('f', bytearray(ls))

def ls2int(ls):
    val = 0
    for i in ls:
        val *= 256
        val += i
    return val

def f2ls(var):
    res = [int(i) for i in struct.pack('f',var)]
    res.reverse()
    return res

def assert_lst(lst, length):
    assert isinstance(lst, list)
    assert len(lst) == length
    for i in lst:
        assert_var(i, int, 8)
    return

def ext_id(ptp=0x0, dst=0xff, src=0xf0, grp=0x0):
    val_len = (1,8,8,3)
    var = (ptp, dst, src, grp)
    res = 0x060
    for i in range(4):
        assert_var(var[i], int, val_len[i])
        res = res << val_len[i]
        res += var[i]
    return res

def id_ext(id_num):
    rest, grp = divmod(id_num, 2**3)
    rest, src = divmod(rest, 2**8)
    rest, dst = divmod(rest, 2**8)
    pro, ptp = divmod(rest, 2**1)
    #rest, pro = divmod(rest, 2**9)
    return pro, ptp, dst, src, grp

def data_sect(typ=0x0, cmd=0x0043, dat=[0x00]*4):
    assert_var(typ, int, 8)
    assert_var(cmd, int, 16)
    assert_lst(dat, 4)
    cmd0, cmd1 = divmod(cmd, 0x100)
    res = [typ]+[0x00]+[cmd0]+[cmd1]+dat
    return res

def dat_ext(ls):
    out_ls = []
    out_ls.append(ls[0])
    out_ls.append(ls[1])
    out_ls.append(ls2int(ls[2:4]))
    if out_ls[0] == 0x41:
        out_ls.append(ls2f(ls[4:]))
    elif out_ls[0] == 0x42:
        out_ls.append(ls2int(ls[4:]))
    else:
        out_ls.append(ls[4:])
    return out_ls

class NXR_COMM:
    def __init__(self, channel=1, dev_ls=[(1,3)]):
        self.ch = channel
        self.running = True
        self.lockflag = 0
        self.dev_ls = dev_ls
        self.flag_que = []
        self.flagkeeper = Thread(target=self.flag_assign)
        self.flagkeeper.start()
        return

    def flag_assign(self):
        while self.running:
            if not self.lockflag and self.flag_que:
                self.lockflag = self.flag_que.pop(0)
            time.sleep(0.1)
        return

    def wait_flag(self):
        f = time.time()
        self.flag_que.append(f)
        count, cmax = 0, 20
        while self.lockflag != f:
            time.sleep(0.3)
            count += 1
            if count >= cmax:
                raise ConnectionError('Timeout for dev In use')
        return f

    def release_flag(self, flag):
        self.lockflag = 0
        return

    def send(self, eid, dat, read=True):
        var.can_dev.send(self.ch, eid, dat)
        if read:
            a, b = var.can_dev.read(self.ch)
            print(b)
            return (a, b)
        else:
            return None

    def get_req(self, dst=0x01, grp=0x03, reg=0x0001):
        eid = ext_id(ptp=0x1, dst=dst, grp=grp)
        dat = data_sect(typ=0x10, cmd=reg)
        f = self.wait_flag()
        count, cmax = 0, 10
        try:
            tup = self.send(eid, dat, read=True)
            while not tup and count < 20:
                time.sleep(0.3)
                tup = self.send(eid, dat)
            if not tup:
                raise ConnectionError('no response')
        finally:
            self.release_flag(f)

        a = id_ext(tup[0])
        b = dat_ext(tup[1])
        #if a[3] != dst:
        #    print(a)
        #    raise ConnectionError('Unexpected Frame Src:', a[3])
        #if b[1] != 0xf0:
        #    print(b)
        #    raise ConnectionError('Invalid Response Frame:', b[1])
        #if b[2] != reg:
        #    print(b)
        #    raise ConnectionError('Invalid Response Register:', b[1])
		print(b)
        return b[3]

    def config(self, dst=0x01, grp=0x03, reg=0x0021, flt=True, val=250):
        if flt:
            data = f2ls(val)
        else:
            data = list(val.to_bytes(4, 'big'))
        eid = ext_id(ptp=0x1, dst=dst, grp=grp)
        dat = data_sect(typ=0x03, cmd=reg, dat=data)
        f = self.wait_flag()
        try:
            self.send(eid, dat, read=False)
        finally:
            self.release_flag(f)
        return

    def get_volt(self, dst=0x01, grp=0x03):
        return self.get_req(dst=dst, grp=grp, reg=0x0001)

    def set_volt(self, dst=0x01, grp=0x03, val=250.):
        self.config(dst=0x01, grp=0x03, flt=True, val=val)
        return

    def get_watt(self, dst=0x01, grp=0x03):
        return self.get_req(dst=dst, grp=grp, reg=0x0048)
		
    def __del__(self):
        self.running = False
