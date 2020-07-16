from . import var

import struct
import time
from threading import Thread


def assert_var(var, typ, len_limit):
    wn = "Wrong type: {} {}".format(type(var), str(typ))
    assert isinstance(var, typ), wn
    wn = "Out of range: 0<{}<{}".format(var, 2**len_limit)
    assert var >= 0 and var < 2**len_limit, wn
    return

def ls2f(ls):
    ls.reverse()
    return struct.unpack('f', bytearray(ls))[0]

def ls2int(ls):
    val = 0
    for i in ls:
        val *= 256
        val += i
    return val

def f2ls(var):
    res = list(struct.pack('!f',var))
    return res

def i2ls(var):
    return list(int(var).to_bytes(4, 'big'))

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
    out_ls = [ls[0], ls[1], ls2int(ls[2:4])]
    if out_ls[0] == 0x41:
        out_ls.append(ls2f(ls[4:]))
    elif out_ls[0] == 0x42:
        out_ls.append(ls2int(ls[4:]))
    else:
        out_ls.append(ls[4:])
    return out_ls

def get_volt():
    return data_sect(typ=0x10, cmd=0x0001)

def set_volt(val=100):
    return data_sect(typ=0x10, cmd=0x0021, dat=f2ls(val))

def get_watt():
    return data_sect(typ=0x10, cmd=0x0048)

def get_curr():
    return data_sect(typ=0x10, cmd=0x0002)

def set_curr(val):
    return data_sect(typ=0x10, cmd=0x0021, dat=i2ls(val*1024))

def get_temp():
    return data_sect(typ=0x10, cmd=0x0004)

def set_onoff(onoff):
    if onoff:
        return data_sect(typ=0x10, cmd=0x0030, dat=[0,0,0,0])
    else:
        return data_sect(typ=0x10, cmd=0x0030, dat=[0,1,0,0])
