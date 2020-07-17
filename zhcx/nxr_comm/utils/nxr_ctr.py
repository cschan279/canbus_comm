import var
import time
from utils import nxr_cmd

class Flag:
    def __init__(self, timeout=5, inter=0.3):
        self.running = True
        self.lockflag = 0
        self.flag_que = []
        self.inter = inter
        self.cmax = timeout // inter
        self.flagkeeper = Thread(target=self.flag_assign)
        self.flagkeeper.start()
        return

    def flag_assign(self):
        while self.running:
            if not self.lockflag and self.flag_que:
                self.lockflag = self.flag_que.pop(0)
            time.sleep(0.3)
        print('flag assign end')
        return

    def wait_flag(self):
        f = time.time()
        self.flag_que.append(f)
        count = 0
        while self.lockflag != f:
            time.sleep(self.inter)
            count += 1
            if count > self.cmax:
                raise ConnectionError('Dev In use, Timeout')
        return f

    def release_flag(self, flag, force=False):
        if force or flag == self.lockflag:
            self.lockflag = 0
            return True
        else:
            return False

class N_CTR:
    def __init__(self, channel=1, addrs=[(1,3)]):
        self.ch = channel
        self.lockflag = Flag(timeout=5)
        self.running = True
        self.addrs = addrs
        # loop send msg
        return

    def _send(self, eid, dat, read=True):
        var.can_dev.send(self.ch, eid, dat)
        time.sleep(0.3)
        if not read:
            return
        else:
            a, b = var.can_dev.read(self.ch)
            count = 0
            while count < 16:
                count += 1
                if not a or b:
                    a, b = var.can_dev.read(self.ch)
                    continue
                if b[0] == 0x41 or b[0]== 0x42:
                    break
                time.sleep(0.3)
            if b[0] == 0x41:
                c = nxr_cmd.ls2int(b[2:4])
                d = nxr_cmd.ls2f(b[4:])
                return True, (a, b), ()
            elif b[0]== 0x42:
                c = nxr_cmd.ls2int(b[2:4])
                d = nxr_cmd.ls2int(b[4:])
                return True, (a, b), ()
            else:
                print('Unk Return data type')
                nxr_cmd.print_pack(a, b)
                return False, (a, b), None

    def set_volt(self, addr_id=0, val=250):
        addr = self.addrs[addr_id]
        eid = nxr_cmd.ext_id(ptp=1, dst=addr[0], grp=addr[1])
        dat = nxr_cmd.set_volt(val=val)
        self._send(eid, dat, read=False)
        return

    def get_volt(self, addr_id=0):
        addr = self.addrs[addr_id]
        eid = nxr_cmd.ext_id(ptp=1, dst=addr[0], grp=addr[1])
        dat = nxr_cmd.get_volt()
        ret, raw, res = self._send(eid, dat, read=True)
        if ret:
            if res[0] = 0x01:
                return True, res[1]
            else:
                return False, res[1]
        else:
            return False, raw

    def set_curr(self, addr_id=0, val=10):
        addr = self.addrs[addr_id]
        eid = nxr_cmd.ext_id(ptp=1, dst=addr[0], grp=addr[1])
        dat = nxr_cmd.set_curr(val=val)
        self._send(eid, dat, read=False)
        return

    def get_curr(self, addr_id=0):
        addr = self.addrs[addr_id]
        eid = nxr_cmd.ext_id(ptp=1, dst=addr[0], grp=addr[1])
        dat = nxr_cmd.get_curr()
        ret, raw, res = self._send(eid, dat, read=True)
        if ret:
            if res[0] = 0x01:
                return True, res[1]
            else:
                return False, res[1]
        else:
            return False, raw

    def set_onoff(self, addr_id=0, onoff=False):
        addr = self.addrs[addr_id]
        eid = nxr_cmd.ext_id(ptp=1, dst=addr[0], grp=addr[1])
        dat = nxr_cmd.set_onoff(onoff)
        self._send(eid, dat, read=False)
        return
