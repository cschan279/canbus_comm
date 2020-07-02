#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def assert_var(var, typ, max_limit):
    assert isinstance(var, typ)
    assert var >= 0 and var < max_limit
    return



def form_id(ptc=0x0d, addr=0x00, cmd=0x50, src=0x1, cnt=0x0):
    val_range = (6,7,8,1,1)
    pos = (23,16,8,7,0)
    var = (ptc, addr, cmd, src, cnt)
    res = 0
    for i in range(5):
        assert_var(var[i], int, 2**val_range[i])
        res += var[i] * 2**pos[i]
    return res

def form_data(fault=0x0, signal=0x0, content=[0x00]*6):
    assert_var(fault, int, 2**4)
    assert_var(signal, int, 2**12)
    assert isinstance(content, list)
    for i in content:
        assert_var(i, int, 2*8)
    byt_12 = signal + fault * 2**12
    b12 = [(byt_12 // 256), (byt_12 % 256)]
    res = b12 + content
    return res

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
