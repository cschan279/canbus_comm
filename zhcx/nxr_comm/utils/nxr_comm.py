from . import can_comm
from . import var

import time


class NXR_COMM:
    def __init__(self, channel=1):
        self.ch = channel
        self.running = True
        self.lockflag = 0
        self.flag_que = []

    def flag_assign(self):
        while self.running:
            if not self.lockflag and self.flag_que:
                self.lockflag = self.flag_que.pop(0)
        return

    def sendnread(self, eid, dat, flag):
        count, cmax = 0, 20
        while self.lockflag != flag:
            time.sleep(0.3)
            count += 1
            if count >= cmax:
                raise ConnectionError('Timeout for dev In use')
        try:
            print()
