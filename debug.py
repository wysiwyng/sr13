import time

class Debug(object):
    def __init__(self):
        self.startTime = time.time()
    
    def getDeltaTime(self):
        return time.time() - self.startTime
        
    def printMsg(self, message, sender):
        print "{0:0>8.4f} -- {1}: {2}".format(self.getDeltaTime(), str(sender), message)
        
    __call__ = printMsg