#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import struct
#[int(i) for i in struct.pack('f',1.2)].reverse()
#struct.unpack('f', bytearray(x.reverse()))


def assert_var(var, typ, len_limit):
    assert isinstance(var, typ)
    assert var >= 0 and var < 2**len_limit
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

def sendNread(can_dev, eid, dat):
    print('Sent:')
    printlsHex(id_ext(eid))
    printlsHex(dat)
    can_dev.send(1, eid, dat)
    a, b = can_dev.read(1)
    count = 0
    while not b and count < 20:
         can_dev.send(1, eid, dat)
         a, b = can_dev.read(1)
         count += 1
    if not b:
        raise ConnectionError('No response:', b[1])
    return a, b

def send2get(can_dev, eid, dat):
    a, b = sendNread(can_dev, eid, dat)
    if b[1] !=0xf0:
        print(b)
        raise ConnectionError('Invalid Response Frame:', b[1])
    if b[0] == 0x41:
        fn = ls2f(b[4:])
    else:
        fn = ls2int(b[4:])
    id_ls = id_ext(a)
    print('Received:')
    printlsHex(id_ls)
    printlsHex(b)
    return id_ls, [b[0], b[1], ls2int(b[2:4]), fn]

def send2config(can_dev, eid, dat):
    a, b = sendNread(can_dev, eid, dat)


def printlsHex(ls):
    ls_out = [hex(i) if isinstance(i, int) else i for i in ls]
    print(ls_out)

def req_addr(can_dev):
    eid = ext_id(ptp=0x1, dst=0xfe, grp=0x03)
    dat = data_sect(typ=0x10, cmd=0x0043)
    a, b = send2get(can_dev, eid, dat)
    print("Result:")
    printlsHex(a)
    printlsHex(b)
    return

def req_volt(can_dev, addr):
    eid = ext_id(ptp=0x1, dst=addr, grp=0x03)
    dat = data_sect(0x10, 0x0001)
    a, b = send2get(can_dev, eid, dat)
    print("Result:")
    printlsHex(a)
    #printlsHex(b)
    #print(b[-1])
    return b[-1]
