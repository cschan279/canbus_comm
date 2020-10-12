#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import struct
#[int(i) for i in struct.pack('f',1.2)].reverse()
#struct.unpack('f', bytearray(x.reverse()))


def encode_id(prono=0x0d, dst=0x01,cmd=0xff,ms=0x1, cnt=0x0):
    fid = (prono & 0x3f)
    fid = (fid << 7) + (dst & 0x7f)
    fid = (fid << 8) + (cmd & 0xFF)
    fid = (fid << 1) + bool(ms)
    fid = (fid << 6) + 0x3f
    fid = (fid << 1) + bool(cnt)
    return fid

def decode_id(fid):
    rest, cnt = divmod(fid, 2**1)
    rest = rest >> 6
    rest, ms = divmod(rest, 2**1)
    rest, cmd = divmod(rest, 2**7)
    pro, src = divmod(rest, 2**8)
    return pro, src, cmd, ms, cnt

def print_hex_ls(ls):
    #print(args)
    for i in ls: print(hex(i), end=" ")
    print(' ')
    return

def print_bin_id(fid):
    x = list("{:029b}".format(fid & 0x1fffffff))
    for i in [-23,-16,-8,-7, -1]: x.insert(i, " ")
    print(''.join(x))
    return

######
'''
1,1,4
2,2,2
2,4
6

'''
######

def encode_data(errc=0x0, rid=0xfff, rdt=[0], rtp=[6]):
    d0, d1 = divmod(rid & 0xfff, 2**8)
    d0 += (errc << 4)
    dat = [d0, d1]
    for i in rtp:
        rest_len = 8-len(dat)
        if isinstance(i, int):
            dat.extend([0]*i)
        elif i in ["B", ">H", ">I"]:
            dt = list(struct.pack(i, rdt.pop(0)))
            dat.extend(dt)
        else:
            dat.extend([0]*rest_len)
            break
        if rest_len <= 0:
            dat = dat[8]
            break
    print_hex_ls(dat)
    return dat

def decode_data(data_ls):
    errc, m1 = divmod(data_ls[0], 2**4)
    rid = (m1<<8)+data_ls[1]
    print(errc, rid, end=' ')
    for i in range(2,8): print(bin(data_ls[i]), end=' ')
    print()
    #print_hex_ls(data_ls)
    return errc, rid, rdt
