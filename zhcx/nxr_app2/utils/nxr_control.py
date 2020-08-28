from threading import Thread
import traceback, time
from utils import can_comm, nxr_conv

volt_id = 0x21
curr_id = 0x1b
onoff_id = 0x30

class NXR_CONTROL:
    def __init__(self, lib_file='./ControlCAN.dll',
                       can_dev=[1]):
        self.can_con = can_comm.CanComm(lib_file=lib_file, can_dev=can_dev)
        self.can_ch = can_dev[0]

        self.sendlist = []
        self.return_buf = [[{}]*256]*8
        self.loop_ret = True
        self.th = Thread(target=self.loop)
        self.th.start()

        fid = nxr_conv.encode_id(ptp=False, dst=0xff, src=0xf0, grp=0x3)
        fdt = nxr_conv.encode_data(func=0x10, rid=0x43, rdt=0, isfloat=False)
        self.sendlist.append({"fid":fid, "fdt":fdt})

        return

    def loop(self):
        print('loop thread for control')
        while self.loop_ret:
            self.send()
            self.read()
            print('.', end='')
        return

    def send(self):
        if not self.sendlist:
            return
        try:
            fid = self.sendlist[0]['fid']
            fdt = self.sendlist[0]['fdt']
            print("x"*10, "Send", "x"*10)
            nxr_conv.print_bin_id(fid)
            nxr_conv.print_hex_ls(fdt)
            print("x"*10, "Send", "x"*10)
            self.can_con.send(self.can_ch, fid, fdt)
            self.sendlist.pop(0)
        except Exception as e:
            traceback.print_exc()
        return

    def read(self):
        try:
            fid, fdt = self.can_con.read(self.can_ch)
            if fid and fdt:
                print("x"*10, "Read", "x"*10)
                nxr_conv.print_bin_id(fid)
                nxr_conv.print_hex_ls(fdt)
                pro, ptp, dst, src, grp = nxr_conv.decode_id(fid)
                err, rid, isfloat, rdt = nxr_conv.decode_data(fdt)
                nxr_conv.print_hex_ls([grp, src, rid, rdt, err])
                print("x"*10, "Read", "x"*10)
                self.new_rec(grp, src, rid, rdt, err)
        except Exception as e:
            traceback.print_exc()
        return

    def new_rec(self, grp, src, rid, rdt, err):
        t = time.time()
        dt_pack = {"time":t, "rid":rid, "rdt":rdt, "err":err}
        print(f"[{t}]: {rid} data from {grp}-{src} as {rdt}")
        self.return_buf[grp][src] = dt_pack
        return

    def set(self, dst, grp, rid, rdt, isfloat):
        t = time.time()
        fid = nxr_conv.encode_id(ptp=True, dst=dst, src=0xf0, grp=grp)
        fdt = nxr_conv.encode_data(func=0x03, rid=rid, rdt=rdt,
                                   isfloat=isfloat)
        self.sendlist.append({"fid":fid, "fdt":fdt})
        for _ in range(20):
            time.sleep(0.2)
            if self.return_buf[grp][dst]:
                if self.return_buf[grp][dst]["time"] > t: return True
        return False

    def req(self, dst, grp, rid):
        t = time.time()
        fid = nxr_conv.encode_id(ptp=True, dst=dst, src=0xf0, grp=grp)
        fdt = nxr_conv.encode_data(func=0x10, rid=rid, rdt=0, isfloat=False)
        self.sendlist.append({"fid":fid, "fdt":fdt})
        for _ in range(20):
            time.sleep(0.2)
            if self.return_buf[grp][dst]:
                if self.return_buf[grp][dst]["time"] > t:
                    return True, self.return_buf[grp][src]["rdt"]
        return False, None
