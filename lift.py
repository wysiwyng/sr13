import time, threading

class Lift(threading.Thread):
    def __init__(self, robot, debug = None):
        threading.Thread.__init__(self)
        self.debug = debug
        self.debugMsg("constructing lift thread")
        self.R = robot
        self.newCommand = threading.Event()
        self.actionFinished = threading.Event()
        self.actionFinished.set()
        if self.getState() == 5:
            self.command = 1
            self.newCommand.set()
            self.actionFinished.clear()
        self.debugMsg("lift thread ready")
        
    def run(self):
        self.debugMsg("running lift thread")
        
        while(True):
            self.debugMsg("waiting for new commands")
            self.newCommand.wait()
            self.actionFinished.clear()
            self.debugMsg("new commands available, evaluating command variable")
            state = self.getState()
            
            if self.command < state:
                self.R.motors[0].target = 100
                self.waitForState(self.command)
                self.R.motors[0].target = 0
            
            if self.command > state:
                self.R.motors[0].target = -100
                self.waitForState(self.command)
                self.R.motors[0].target = 0
            
            if self.command == state:
                self.debugMsg("command executed, setting actionFinished flag and resetting command")
                self.command = 0
                self.newCommand.clear()
                self.actionFinished.set()

    def grabToken(self, height = 2):
        self.debugMsg("grabbing token, activating pump and moving downwards")
        self.R.io[0].output[0].d = 1    #pumpe an
        self.R.motors[0].target = 40
        self.debugMsg("waiting for pressure to fall")
        
        while self.R.io[0].input[4].d == 0:
            if self.getState() == 1:
                self.debugMsg("reached bottom position and no token, aborting")
                self.releaseToken()
                self.R.motors[0].target = 0
                self.tokenHeightAsync()
                return False
                
        self.debugMsg("moving arm to token height")
        self.R.motors[0].target = -100
        self.waitForState(height)
        self.R.motors[0].target = 0
        self.debugMsg("arrived at token height, returning")
        return True

    def releaseToken(self):
        self.debugMsg("releasing token")
        self.R.io[0].output[0].d = 0

    def hasToken(self):
        if self.R.io[0].input[4].d == 1:
            self.debugMsg("token is present")
            return True
        else:
            self.debugMsg("no token present")
            return False
    
    def bottom(self):
        self.bottomAsync()
        self.debugMsg("waiting for command to finish")
        self.actionFinished.wait()
    
    def tokenHeight(self):
        self.tokenHeightAsync()
        self.debugMsg("waiting for command to finish")
        self.actionFinished.wait() 

    def pedestalHeight(self):
        self.pedestalHeightAsync()
        self.debugMsg("waiting for command to finish")
        self.actionFinished.wait()
        
    def top(self):
        self.topAsync()
        self.debugMsg("waiting for command to finish")
        self.actionFinished.wait()

    def bottomAsync(self):
        self.debugMsg("signalling main thread to move to bottom position")
        self.command = 1
        self.newCommand.set()
        self.debugMsg("signal sent, should be processed immediatly")
    
    def tokenHeightAsync(self):
        self.debugMsg("signalling main thread to move to token height")
        self.command = 2
        self.newCommand.set()
        self.debugMsg("signal sent, should be processed immediatly")    
        
    def pedestalHeightAsync(self):
        self.debugMsg("signalling main thread to move to pedestal height")
        self.command = 3
        self.newCommand.set()
        self.debugMsg("signal sent, should be processed immediatly")  
        
    def topAsync(self):
        self.debugMsg("signalling main thread to move to top position")
        self.command = 4
        self.newCommand.set()
        self.debugMsg("signal sent, should be processed immediatly")
        
    def getState(self):
        with self.R.io[0].dev.lock:
            ports = self.R.io[0]._inputs_read_d()
        
        if ports[5] == 1:
            return 5
        
        elif ports[6] == 0 and ports[7] == 0:
            return 1
        
        elif ports[6] == 1 and ports[7] == 0:
            return 2

        elif ports[6] == 0 and ports[7] == 1:
            return 3
            
        elif ports[6] == 1 and ports[7] == 1:
            return 4
            
        else:
            self.debugMsg("something is wrong with the lift ports, setting state to 0")
            return 0

    def debugMsg(self, text):
        if self.debug != None:
            self.debug.printMsg(text, self)
    
    def waitForState(self, state):
        self.debugMsg("waiting for state to become {0}".format(state))
        while self.getState() != 5:
            pass
        self.debugMsg("in movement now waiting")
        temp = self.getState()
        while True:
            if temp == state:
                self.debugMsg("reached state {0}".format(state))
                return True
            elif temp == 1 or temp == 4:
                self.debugMsg("something went wrong, we're at state {0}".format(temp))
                return False
            temp = self.getState()
        
    def __str__(self):
        return "lift"
