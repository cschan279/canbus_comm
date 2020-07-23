import time

class Lock:
    def __init__(self, interval=0.1, countmax=50):
        self.true = True
        self.lock0 = None
        self.lock1 = None
        self.countmax = countmax
        self.interval = interval
        return

    def getlock(self):
        t = time.time()
        count = 0
        while self.true:
            while self.lock0 or self.lock1:
                time.sleep(0.1)
                count += 1
                if count >= 50:
                    return False
            self.lock0 = t
            time.sleep(0.1)
            if self.lock0 == t:
                break
            else:
                self.lock0 = None
        self.lock1 = t
        return t

    def unlock(self, t, force=False):
        if force or self.lock0 == t:
            self.lock0 = None
        else:
            print('mismatch lock0 to release', self.lock0, t)
        if force or self.lock1 == t:
            self.lock1 = None
        else:
            print('mismatch lock1 to release', self.lock1, t)
        return
