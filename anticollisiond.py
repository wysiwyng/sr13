import time, threading, event

class AntiCollisiond(threading.Thread):
    def __init__(self, robot, alarmDist = 0, debug = None):
            threading.Thread.__init__(self)
            self.R = robot
            self.debug = debug
            self.alarmDist = alarmDist
            self.USDist = 0
            self.rearBumper = 0
            self.frontBumper = 0
            self.rearBumper_pressed = event.Event()
            self.USSensor_tooNear = event.Event()
            self.frontBumper_pressed = event.Event()
            self.running = threading.Event()
            
    def run(self):
        while(True):
            self.running.wait()
            with self.R.io[0].dev.lock:
                ports = self.R.io[0]._inputs_read_a()

            self.USDist = int(ports[0] * (1023 / 3.3)) / 2 * 2.54

            if ports[3] > 2:
                self.rearBumper = True
                self.rearBumper_pressed(self)
            else:
                self.rearBumper = False
            
            if ports[2] > 2:
                self.frontBumper = True
                self.frontBumper_pressed(self)
            else:
                self.frontBumper = False

            if self.USDist < self.alarmDist:
                self.USSensor_tooNear([self, self.USDist])      

    def getUsDistance(self, samples = 6):
        if not self.running.isSet():
            temp = []
            for i in range(samples):
                with self.R.io[0].dev.lock:
                    ports = self.R.io[0]._inputs_read_a()
                temp.append(int(ports[0] * (1023 / 3.3)) / 2 * 2.54)
                self.debugMsg("us reads {0}".format(temp[i]))
            self.USDist = temp[int(samples / 2)]
                
        self.debugMsg("ultrasonic sensor reads a distance of {0}".format(self.USDist))
        return self.USDist

    def getFrontBumper(self):
        self.debugMsg("front bumper is reading {0}".format(self.frontBumper))
        return self.frontBumper

    def getRearBumper(self):
        self.debugMsg("rear bumper is reading {0}".format(self.rearBumper))
        return self.rearBumper

    def debugMsg(self, text):
        if self.debug != None:
            self.debug.printMsg(text, self)
    
    def on(self):
        self.running.set()
        
    def off(self):
        self.running.clear()
    
    def __str__(self):
        return "anticollisiond"
