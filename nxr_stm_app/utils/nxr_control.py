from threading import Thread
import traceback, time
from utils import can_comm, nxr_conv

get_volt_id = 0x01
set_volt_id = 0x21
get_curr_id = 0x02
set_curr_id = 0x1b
set_onoff_id = 0x30
get_status_id = 0x40

class NXR_CONTROL:
    def __init__(self, event, dev='/dev/ttyUSB0'):
        self.can_con = can_comm.CanComm(event, dev)
        
        
        self.sendlist = []
        self.return_buf = [[{}]*256]*8
        self.event = event

        self.lastsend = 0

        self.bc_id = nxr_conv.encode_id(ptp=False, dst=0xff, src=0xf0, grp=0x3)
        self.bc_dt = nxr_conv.encode_data(func=0x10, rid=0x43, rdt=0, isfloat=False)

        self.th = Thread(target=self.loop)
        self.th.start()


        #self.sendlist.append({"fid":self.bc_id, "fdt":self.bc_dt})

        return

    def loop(self):
        print('loop thread for control')
        while self.event.is_set():
            self.send()
            self.read()
            self.keepsend()
            #print('.', end='')
        return

    def keepsend(self):
        if time.time() - self.lastsend > 3:
            self.sendlist.append({"fid":self.bc_id, "fdt":self.bc_dt})
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
            self.can_con.req_send(fid, fdt)
            self.lastsend = time.time()
            self.sendlist.pop(0)
        except Exception as e:
            traceback.print_exc()
        return

    def read(self):
        try:
            if not self.can_con.read_buf:
                return
            fid, fdt = self.can_con.read()
            if fid and fdt:
                #print("x"*10, "Read", "x"*10)
                #nxr_conv.print_bin_id(fid)
                #nxr_conv.print_hex_ls(fdt)
                pro, ptp, dst, src, grp = nxr_conv.decode_id(fid)
                err, rid, isfloat, rdt = nxr_conv.decode_data(fdt)
                #nxr_conv.print_hex_ls([grp, src, rid, err])
                #print("x"*10, "Read", "x"*10)
                if rid in [0x40, 0x43]:
                    print("*"*30)
                    nxr_conv.print_hex_ls(fdt)
                    print("*"*30)
                self.new_rec(grp, src, rid, rdt, err)
        except Exception as e:
            traceback.print_exc()
        return

    def new_rec(self, grp, src, rid, rdt, err):
        if err:
            print(f"Error Msg: {grp:x}-{src:02x}-{rid:04x}={err}+{rdt}", end='\r')
            return
        t = time.time()
        dt_pack = {"time":t, "rdt":rdt, "err":err}
        print('###_New_Record_###', dt_pack)
        #if not err: print(f">>>>>>[{t}]: {rid:04x} data from {grp:x}-{src:02x} as {rdt}")
        self.return_buf[grp][src][rid] = dt_pack
        #self.return_buf[grp][src][rid]['rdt'] = rdt
        #self.return_buf[grp][src][rid]['err'] = err
        #self.return_buf[grp][src][rid]['time'] = t
        #if not rid > 100: print(f"///{grp}-{src}:", self.return_buf[grp][src])
        return

    def set(self, dst, grp, rid, rdt, isfloat):
        t = time.time()
        fid = nxr_conv.encode_id(ptp=True, dst=dst, src=0xf0, grp=grp)
        fdt = nxr_conv.encode_data(func=0x03, rid=rid, rdt=rdt,
                                   isfloat=isfloat)
        self.sendlist.append({"fid":fid, "fdt":fdt})
        for _ in range(5):
            time.sleep(0.1)
            if rid in self.return_buf[grp][dst]:
                if self.return_buf[grp][dst][rid]["time"] > t:
                    print('got reply', self.return_buf[grp][dst][rid]["rdt"])
                return True, self.return_buf[grp][dst][rid]["rdt"]
        return False, None

    def req(self, dst, grp, rid):
        t = time.time()
        fid = nxr_conv.encode_id(ptp=True, dst=dst, src=0xf0, grp=grp)
        fdt = nxr_conv.encode_data(func=0x10, rid=rid, rdt=0, isfloat=False)
        self.sendlist.append({"fid":fid, "fdt":fdt})
        for _ in range(5):
            time.sleep(0.1)
            if rid in self.return_buf[grp][dst]:
                if self.return_buf[grp][dst][rid]["time"] > t:
                    print('got reply', self.return_buf[grp][dst][rid]["rdt"])
                return True, self.return_buf[grp][dst][rid]["rdt"]
        return False, None
