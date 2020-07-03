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
    return struct.unpack('f', bytearray(ls.reverse()))

def f2ls(var):
    return [int(i) for i in struct.pack('f',var)].reverse()

def assert_lst(lst, length):
    assert isinstance(lst, list)
    assert len(lst) == length
    for i in lst:
        assert_var(i, int, 8)
    return

def ext_id(pro=0x060, ptp=0x0, dst=0xff, src=0xf0, grp=0x0):
    val_len = (9,1,8,8,3)
    var = (pro, ptp, dst, src, grp)
    res = 0
    for i in range(5):
        assert_var(var[i], int, val_len[i])
        res += var[i]
        if (i+1) < 5:
            res << val_len[i]
    return res

def data_sect(typ=0x0, cmd=0x0043, dat=[0x00]*4):
    assert_var(typ, int, 8)
    assert_var(cmd, int, 16)
    assert_lst(dat, 4)
    cmd0 = cmd // 0x100
    cmd1 = cmd % 0x100
    res = [typ]+[cmd0]+[cmd1]+dat
    return res

def req_addr(can_dev):
    eid = ext_id()
    dat = data_sect(typ=0x10, cmd=0x0043)
    can_dev.send(1, eid, dat)
    a, b = can_dev.read(1)
    print("{:029b}".format(a), b)


def test(can1):
    id_1 = hw_frame.form_id(ptc=0x0d, addr=0x00, cmd=0x50, src=0x1, cnt=0x0)
    data_1 = hw_frame.form_data(fault=0x0, signal=0x0, content=[0x00]*6)

    can1.send(0, id_1, data_1)
    a, b = can1.read(0)
    while a:
        print("{:029b}".format(a), b)
        if not a%2:
            break
        a, b = can1.read(0)
