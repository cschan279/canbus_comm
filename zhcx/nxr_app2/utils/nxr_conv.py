#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import struct
#[int(i) for i in struct.pack('f',1.2)].reverse()
#struct.unpack('f', bytearray(x.reverse()))


def encode_id(prono=0x060, ptp=True,dst=0x01,src=0xf0,grp=0x03):
    fid = (prono & 0x1ff)
    fid = (fid << 1) + (ptp & 0x1)
    fid = (fid << 8) + (dst & 0xFF)
    fid = (fid << 8) + (src & 0xFF)
    fid = (fid << 3) + (src & 0x7)
    return fid

def decode_id(fid):
    rest, grp = divmod(id_num, 2**3)
    rest, src = divmod(rest, 2**8)
    rest, dst = divmod(rest, 2**8)
    pro, ptp = divmod(rest, 2**1)
    return pro, ptp, dst, src, grp

def print_hex_ls(*args):
    for i in args: print(hex(i), end=" ")
    print(' ')
    return

def print_bin_id(fid):
    x = list("{:029b}".format(fid & 0x1fffffff))
    for i in [-20,-19,-11,-3]: x.insert(i, " ")
    print(''.join(x))
    return

def encode_data(func=0x03, errc=0x00, rid=0x00, rdt=0, isfloat=False):
    dat = [func, errc]
    dat.extend(list(struct.pack(">H",cmd)))
    if isfloat:
        dat.extend(list(struct.pack('>f',rdt)))
    else:
        dat.extend(list(struct.pack(">I",rdt)))
    dat = [(dat[i]&0xFF) for i in range(8)]
    return dat

def decode_data(data_ls):
    func = data_ls[0]
    isfloat = (func == 0x41)
    errc = (data_ls[1] != 0xF0) or (func != 0x41 and func != 0x42)
    rid = struct.unpack(">H", bytearray(data_ls[2:4]))[0]
    if isfloat:
        rdt = struct.unpack(">f", bytearray(data_ls[4:]))[0]
    else:
        rdt = struct.unpack(">I", bytearray(data_ls[4:]))[0]
    return errc, rid, isfloat, rdt
