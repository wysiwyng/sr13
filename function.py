# IF YOU UNDERSTAND IT, IT'S OBSOLETE :3

import time, math

MARKER_ARENA = 0
MARKER_ROBOT = 1
MARKER_PEDESTAL = 2
MARKER_TOKEN = 3

markerTypes = ["Arena Marker", "Robot Marker", "Pedestal Marker", "Token Marker"]

class Driver(object):
    def __init__(self, robot, motor, maxSpeed = 255, distModifier = 10, distModifierBegin = 80, camRes = (800, 600), debug = None):
        self.debug = debug
        self.debugMsg("constructing driver object which is totally not the drivingFunctions object from the last story")
        self.robot = robot
        self.motor = motor
        self.maxSpeed = maxSpeed
        self.distModifier = distModifier
        self.distModifierBegin = distModifierBegin
        self.camRes = camRes

    def getMarkerAtOffset(self, markers, type, offset = -1):
        markers.sort(key = lambda x: x.dist)
        for m in markers:
            if m.info.offset == offset and m.info.marker_type == type:
                self.debugMsg("found {0} {1}, returning it".format(markerTypes[type], offset))
                return m
            elif offset == -1 and m.info.marker_type == type:
                self.debugMsg("found a {0}, returning the nearest".format(markerTypes[type]))
                return m

    def lookForMarkers(self, type, offset = -1, direction = True, degrees = 20):
        self.debugMsg("stabilizing camera")
        time.sleep(0.3)
        self.debugMsg("looking for markers")
        markers = self.robot.see(self.camRes)
        tempMarker = self.getMarkerAtOffset(markers, type, offset)
        if tempMarker != None:
            self.debugMsg("found the marker, returning")
            return tempMarker, markers
        self.debugMsg("no marker found, turning {0} degrees".format(degrees))
        if direction:
            self.motor.turnRight(self.maxSpeed - 20, degrees)
        else:
            self.motor.turnLeft(self.maxSpeed - 20, degrees)
        
        return None

    def turnToMarker(self, marker):                          #a function to determine if the robot is centerd within 5 degrees of the given marker and if not to correct the deviation
        if abs(marker.rot_y) > 5:
            self.debugMsg("centering on marker")
            if marker.rot_y > 0:
                self.debugMsg("correcting {0} deg to the right".format(marker.rot_y -2))
                self.motor.turnRight(self.maxSpeed - 20, int(marker.rot_y) - 2)
            else:
                self.debugMsg("correcting {0} deg to the left".format(marker.rot_y -2))
                self.motor.turnLeft(self.maxSpeed - 20, int(abs(marker.rot_y)) - 2)
            self.debugMsg("should now be centered, look again to verify")
            return False
        
        self.debugMsg("marker is within +- 5 degrees, continuing")
        return True    
        
    def driveToCenterAxisMk2(self, marker, distance):                                                      #a function which leads us diagonal 45 cm before the wanted marker                           
        self.debugMsg("attempting to get to markers center axis")
        _distToM = marker.dist * 100        #distance to marker
        _direction = marker.orientation.rot_y > 0                 
        _distToD = _distToM**2 + distance**2 - (2 * _distToM * distance * math.cos(math.radians(abs(marker.orientation.rot_y))))       #distance to drive square
        _distToD = math.sqrt(_distToD)                                                                                              #getting rid of the square
        _beta = math.degrees(math.acos((_distToM**2 + _distToD**2 - distance**2) / (2 * _distToM * _distToD)))                #angle to turn            
        _alpha = 180 - _beta - abs(marker.orientation.rot_y)
        _gAlpha = 180 - _alpha

        if _distToD > self.distModifierBegin:
            _distToD -= self.distModifier

        if _distToD < 10 or _beta < 2 or _gAlpha < 2 or _distToM < distance:
            self.debugMsg("exiting: distToD: {0}, beta: {1}, gAlpha: {2}, distToM: {3}, distance: {4}".format(_distToD, _beta, _gAlpha, _distToM, distance))
            return True
            
        if _direction:
            self.debugMsg("now turning {0} degrees to the left".format(_beta))
            self.motor.turnLeft(self.maxSpeed - 20, int(_beta))
            time.sleep(0.3)
            
            self.debugMsg("driving {0} cm forward".format(_distToD))
            self.motor.driveForward(int(self.maxSpeed), 0, int(_distToD))
            time.sleep(0.3)
            
            self.debugMsg("turning {0} degrees to the right".format(_gAlpha))
            self.motor.turnRight(self.maxSpeed - 20, int(_gAlpha))
        else:
            self.debugMsg("now turning {0} degrees to the right".format(_beta))
            self.motor.turnRight(self.maxSpeed - 20, int(_beta))
            time.sleep(0.3)
            
            self.debugMsg("driving {0} cm forward".format(_distToD))
            self.motor.driveForward(int(self.maxSpeed), 0, int(_distToD))
            time.sleep(0.3)
            
            self.debugMsg("turning {0} degrees to the left".format(_gAlpha))
            self.motor.turnLeft(self.maxSpeed - 20, int(_gAlpha))
        
        return False    

    def driveToCenterAxis(self, marker):              #a function to test if the robot is out of the center axis of the given marker and if yes to drive to it
        _distance = marker.dist * 100                                                           #some variables & calculations to determine & store the distances and angles needed
        _mRotY = abs(marker.orientation.rot_y)
        _mCRotY = abs(marker.rot_y)
        _angleToTurn = 90 - _mRotY
        _distToDrive = math.sin(math.radians(_mRotY)) * _distance
        _direction = marker.orientation.rot_y > 0
    
        if _mRotY < 5  or _distToDrive < 10:
            self.debugMsg("already centered or too near to center axis, returning")       
            return True
    
        self.debugMsg("attempting to get on markers center axis:")
        self.debugMsg("turn angle is {0} degrees".format(_angleToTurn))
        self.debugMsg("drive distance is {0} cm".format(_distToDrive))
    
        if _direction:
            self.debugMsg("we are standing right of the marker, turning left")     
            self.motor.turnLeft(self.maxSpeed - 20, int(_angleToTurn))
        else:
            self.debugMsg("we are standing left of the marker, turning right")      
            self.motor.turnRight(self.maxSpeed - 20, int(_angleToTurn))
    
        time.sleep(0.2)
    
        self.debugMsg("driving towards center axis")
        self.motor.driveForward(int(self.maxSpeed), 0, int(_distToDrive))
    
        time.sleep(0.2)
    
        if _direction:
            self.debugMsg("started right of the marker, now turning back right")
            self.motor.turnRight(self.maxSpeed - 20, 90)
        else:
            self.debugMsg("started left of the marker, now turning back left")       
            self.motor.turnLeft(self.maxSpeed - 20, 90)
    
        self.debugMsg("should now be on markers center axis, look again to verify")  
        return False
       
    def driveTowardsMarker(self, marker, distance):                   #a function to determine if the robot is within a given distance in cm to a given marker and if not to drive towards it
        if marker.dist * 100 - distance > 10:
            self.debugMsg("driving {0} cm towards the marker".format(marker.dist*100-distance))        
            self.motor.driveForward(int(self.maxSpeed), 0, int(marker.dist * 100 - distance))
            return False
        else:
            self.debugMsg("too near to the marker, returning")      
            return True

    def lookForTokenAbove(self, wantedMarker, markers):
        for m in markers:
            if abs(m.centre.world.y - wantedMarker.centre.world.y) > 0.25 and abs(m.centre.world.y - wantedMarker.centre.world.y) < 0.35 and (abs(m.rot_y) - abs(wantedMarker.rot_y)) > -1.5 and (abs(m.rot_y) - abs(wantedMarker.rot_y)) < 1.5:
                return True
        return False
            
    def driveToMarker(self, type, offset = -1, distance = 50, direction = False, maxTries = 2, hadMarker = False, useMk1 = False):        #true = rechts, false = links
        self.debugMsg("attempting to drive to {0} {1}".format(markerTypes[type], offset))
        state = 0
        degrees = 20
        banana = 0
        tokenAbove = False
        while state != -1:
            if state == 0:
                self.debugMsg("state is 0; searching for marker")
                res = self.lookForMarkers(type, offset, direction, degrees)
                if res != None:
                    wantedMarker = res[0]
                    allMarkers = res[1]
                    self.debugMsg("found expected marker; setting state to 1")
                    hadMarker = True
                    if not tokenAbove:
                        tokenAbove = self.lookForTokenAbove(wantedMarker, allMarkers)
                    degrees = 10
                    state = 1
                elif res == None and hadMarker == True:
                    self.debugMsg("wanted marker was not found but we saw one previously, setting state to 0")
                    #degrees += 10
                    #direction = not direction
                    state = 0
                else:
                    self.debugMsg("wanted marker was not found, setting state to 0")
                    state = 0
                    
            elif state == 1:
                self.debugMsg("state is 1, turn to marker")
                if self.turnToMarker(wantedMarker):
                    self.debugMsg("facing marker directly; setting state to 2")
                    state = 2
                else:
                    self.debugMsg("not facing; correcting orientation; state is 0")
                    state = 0
            
            elif state == 2:
                self.debugMsg("state is 2, drive to markers center axis using mk2 routine")
                res = False
                if maxTries > 0:
                    self.debugMsg("we have {0} tries left, attempting mk2 routine".format(maxTries))
                    res = self.driveToCenterAxisMk2(wantedMarker, distance + 10)
                    maxTries -= 1
                    if res:
                        self.debugMsg("no correction necessary, setting state to 3")
                        state = 3
                    else:
                        self.debugMsg("corrected, looking again, setting state to 0")
                        state = 0     
                else:
                    self.debugMsg("no tries left, setting state to 3")
                    state = 3             
                    
            elif state == 3:
                if useMk1:
                    self.debugMsg("state is 3, drive to markers center axis, using mk1 routine")
                    if self.driveToCenterAxis(wantedMarker):
                        self.debugMsg("perfectly on center axis, setting state to 4")
                        state = 4
                    else:
                        self.debugMsg("not on center axis, corrected, setting state to 0")
                        state = 0
                else:
                    state = 4
                    
            elif state == 4:
                if self.driveTowardsMarker(wantedMarker, distance):
                    self.debugMsg("we are now in our wanted position; exiting main loop; state is 5")
                    state = -1
                else:
                    self.debugMsg("our distance to our marker is too damn high; driving forward; state is 0")
                    state = 0
        
            #if banana > 20:
            #    return "BANANA?!"
            
            banana += 1
        return res, tokenAbove
        
    def driveToFixpoint(self, type, offset = -1, direction = False):
        state = 0
        degrees = 10
        while state != -1:
            if state == 0:
                res = self.lookForMarkers(type, offset, direction, degrees)
                if res != None:
                    wantedMarker = res[0]
                    allMarkers = res[1]
                    state = 1
                    degrees = 10
                else:
                    state = 0
                    degrees += 10
                    direction = not direction
            
            elif state == 1:
                if self.turnToMarker(wantedMarker):
                    state = 2
                else: 
                    state = 0
            
            elif state == 2:
                if self.driveToCenterAxis(wantedMarker):
                    state = -1
                else:
                    state = 0                   
        return res
        
    def debugMsg(self, message):
        if self.debug != None:
            self.debug.printMsg(message, self)
            
    def __str__(self):
        return "driver"
