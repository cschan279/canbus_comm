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
        if read:
            a, b = var.can_dev.read(self.ch)
