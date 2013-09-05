from sr import *
import serial, time, function, motor, lift, voltaged, debug, anticollisiond, configReader, random

d = debug.Debug()
d("opening serial port", "main")
ser = serial.Serial("/dev/ttyUSB0", 115200)
d("initing motor controller", "main")
m = motor.Motor(ser)
m.init()
d("init complete, creating robot", "main")
R = Robot()

d("declaring objects", "main")

tokens = [[0, 1, 2, 3, 4, 5],
[6, 7, 8, 9, 10, 11],
[12, 13, 14, 15, 16, 17],
[18, 19, 20, 21, 22, 23]]

nearPedestals = [0, 2, 8, 6]

leftPedestals = [[1, 2],
[5, 8],
[7, 6],
[3, 0]]

rightPedestals = [[3, 6],
[1, 0],
[5, 2],
[7, 8]]

homeMarker = [0, 21, 14, 7]

c = configReader.ConfigReader(R.usbkey, d)
v = voltaged.Voltaged(R, d)
l = lift.Lift(R)
if c.getDebug():
    f = function.Driver(R, m, c.getMaxSpeed(), c.getDistModifier(), c.getDistModifierBegin(), (c.getCamResX(), c.getCamResY()), d)
else:
    f = function.Driver(R, m, c.getMaxSpeed(), c.getDistModifier(), c.getDistModifierBegin(), (c.getCamResX(), c.getCamResY()))
    
a = anticollisiond.AntiCollisiond(R)
l.daemon = True
m.daemon = True
a.daemon = True
v.daemon = True

b = c.getTokenOrder()
command = c.getCommands()

maxSpeed = c.getMaxSpeed()

def capNearestPedestal(tOffset):
    d("capturing nearest pedestal", "main")
    d("driving to token {0}".format(tOffset), "main")
    f.driveToMarker(MARKER_TOKEN, tokens[R.zone][tOffset], useMk1 = True, hadMarker = True)
    grabToken(MARKER_TOKEN, tokens[R.zone][tOffset])
    d("found token {0}, grabbing it".format(tOffset), "main")
    time.sleep(0.2)
    m.turnRight(maxSpeed - 20, 90)
    time.sleep(0.2)
    m.driveForward(maxSpeed, 0, 155)
    time.sleep(0.2)
    m.turnRight(maxSpeed - 20, 110)
    d("taking the token to pedestal {0}".format(nearPedestals[R.zone]), "main")
    tokenAbove = f.driveToMarker(MARKER_PEDESTAL, nearPedestals[R.zone], direction = True, distance = 40, useMk1 = True)[1]
    if tokenAbove == True:
        l.top()
        m.driveForward(maxSpeed - 20, 0, a.getUsDistance() - 15)
    else:
        m.driveForward(maxSpeed - 20, 0, a.getUsDistance() - 5)
    d("planting token", "main")
    time.sleep(0.5)
    l.releaseToken()
    time.sleep(2)
    m.driveBackward(maxSpeed, 0, 70)
    l.tokenHeightAsync()
    time.sleep(0.2)
    m.turnRight(maxSpeed - 20, 90)
    nextToken = int(b.pop(0))
    l.actionFinished.wait()
    return nextToken

def capMiddleLeftPedestal(tOffset):
    d("capturing middleleft Pedestal", "main")
    d("searching nexttoken {0}".format(tOffset), "main")
    f.driveToMarker(MARKER_TOKEN, tokens[R.zone][tOffset], useMk1 = True, hadMarker = True)
    grabToken(MARKER_TOKEN, tokens[R.zone][tOffset])
    time.sleep(0.2)
    if tOffset == 4:
        m.driveBackward(maxSpeed, 0, 90)
        time.sleep(0.2)
        m.turnRight(maxSpeed - 20, 105)
    if tOffset == 5:
        m.turnRight(maxSpeed - 20, 90)
        time.sleep(0.2)
        m.driveBackward(maxSpeed, 0, 45)
        time.sleep(0.2)
        m.turnRight(maxSpeed - 20, 70)
    if tOffset < 4:
        m.turnRight(maxSpeed - 20, 140)

    time.sleep(0.2)
    tokenAbove = f.driveToMarker(MARKER_PEDESTAL, leftPedestals[R.zone][0], useMk1 = True)[1]
    if tokenAbove == True:
        l.top()
        m.driveForward(maxSpeed - 20, 0, a.getUsDistance() - 15)
    else:
        m.driveForward(maxSpeed - 20, 0, a.getUsDistance() - 5)
    d("planting token", "main")
    time.sleep(0.5)
    l.releaseToken()
    time.sleep(2)
    m.driveBackward(maxSpeed, 0, 70)
    l.tokenHeightAsync()
    time.sleep(0.2)
    f.driveToFixpoint(MARKER_PEDESTAL, leftPedestals[R.zone][0])
    m.turnLeft(maxSpeed - 20, 85)
    time.sleep(0.2)
    m.driveForward(maxSpeed, 0, 90)
    time.sleep(0.2)
    nextToken = int(b.pop(0))
    if nextToken < 4:
        m.turnLeft(maxSpeed - 20, 85)
        time.sleep(0.2)
        m.driveForward(maxSpeed, 0, 155 - (40 * nextToken))
        time.sleep(0.2)
        m.turnRight(maxSpeed - 20, 90)
    elif nextToken == 5:
        m.turnRight(maxSpeed - 20, 70)
    l.actionFinished.wait()
    return nextToken
        
def capFarLeftPedestal(tOffset):
    d("capturing farleft pedestal", "main")
    d("searching nexttoken {0}".format(tOffset), "main")
    f.driveToMarker(MARKER_TOKEN, tokens[R.zone][tOffset], useMk1 = True, hadMarker = True)
    grabToken(MARKER_TOKEN, tokens[R.zone][tOffset])
    time.sleep(0.2)
    m.turnLeft(maxSpeed - 20, 90)
    time.sleep(0.2)
    arenaMarker = f.driveToFixpoint(MARKER_ARENA, homeMarker[R.zone])[0]
    m.turnLeft(maxSpeed - 20, 179)
    time.sleep(0.2)
    m.driveForward(maxSpeed, 0, int(400 - arenaMarker.dist * 100))
    time.sleep(0.2)
    m.turnRight(maxSpeed - 20, 45)
    time.sleep(0.2)
    tokenAbove = f.driveToMarker(MARKER_PEDESTAL, leftPedestals[R.zone][1], direction = True, useMk1 = True)[1]
    if tokenAbove == True:
        l.top()
        m.driveForward(maxSpeed - 20, 0, a.getUsDistance() - 15)
    else:
        m.driveForward(maxSpeed - 20, 0, a.getUsDistance() - 5)
    d("planting token", "main")
    time.sleep(0.5)
    l.releaseToken()
    time.sleep(2)
    m.driveBackward(maxSpeed, 0, 70)
    l.tokenHeightAsync()
    f.driveToFixpoint(MARKER_PEDESTAL, leftPedestals[R.zone][1])
    time.sleep(0.2)
    m.turnLeft(maxSpeed - 20, 90)
    time.sleep(0.2)
    m.driveForward(maxSpeed, 0, 95)
    time.sleep(0.2)
    m.turnLeft(maxSpeed - 20, 90)
    time.sleep(0.2)
    nextToken = int(b.pop(0))
    m.driveForward(maxSpeed, 0, 355 - (40 * (nextToken)))
    time.sleep(0.2)
    m.turnRight(maxSpeed - 20, 90)
    l.actionFinished.wait()
    return nextToken
        
def capMiddleRightPedestal(tOffset):
    d("capturing middle right pedestal", "main")
    f.driveToMarker(MARKER_TOKEN, tokens[R.zone][tOffset], hadMarker = True)
    grabToken(MARKER_TOKEN, tokens[R.zone][tOffset])
    time.sleep(0.2)
    m.turnLeft(maxSpeed - 20, 80)
    time.sleep(0.2)
    arenaMarker = f.driveToMarker(MARKER_ARENA, homeMarker[R.zone], distance = 110)
    time.sleep(0.2)
    f.driveToFixpoint(MARKER_ARENA, homeMarker[R.zone])
    m.turnLeft(maxSpeed - 20, 80)
    time.sleep(0.2)
    m.driveForward(maxSpeed, 0, 150)
    time.sleep(0.2)
    m.turnLeft(maxSpeed - 20, 45)
    tokenAbove = f.driveToMarker(MARKER_PEDESTAL, rightPedestals[R.zone][0], direction = True, useMk1 = True)[1]
    if tokenAbove == True:
        l.top()
        m.driveForward(maxSpeed - 20, 0, a.getUsDistance() - 15)
    else:
        m.driveForward(maxSpeed - 20, 0, a.getUsDistance() - 5)
    d("planting token", "main")
    time.sleep(0.5)
    l.releaseToken()
    time.sleep(2)
    m.driveBackward(maxSpeed, 0, 60)
    l.tokenHeightAsync()
    time.sleep(0.2)
    f.driveToFixpoint(MARKER_PEDESTAL, rightPedestals[R.zone][0])
    m.turnRight(maxSpeed - 20, 80)
    time.sleep(0.2)
    m.driveForward(maxSpeed, 0, 85)
    time.sleep(0.2)
    m.turnRight(maxSpeed - 20, 80)
    time.sleep(0.2)
    m.driveForward(maxSpeed, 0, 190)
    time.sleep(0.2)
    m.turnRight(maxSpeed - 20, 70)
    time.sleep(0.2)
    nextToken = int(b.pop(0))
    m.driveForward(maxSpeed, 0, 40 + (nextToken * 40))
    time.sleep(0.2)
    m.turnLeft(maxSpeed - 20, 80)
    l.actionFinished.wait()
    return nextToken

def capFarRightPedestal(tOffset):
    d("capturing middle right pedestal", "main")
    f.driveToMarker(MARKER_TOKEN, tokens[R.zone][tOffset], hadMarker = True)
    grabToken(MARKER_TOKEN, tokens[R.zone][tOffset])
    time.sleep(0.2)
    m.turnLeft(maxSpeed - 20, 80)
    time.sleep(0.2)
    arenaMarker = f.driveToMarker(MARKER_ARENA, homeMarker[R.zone], distance = 100)
    time.sleep(0.2)
    f.driveToFixpoint(MARKER_ARENA, homeMarker[R.zone])
    m.turnLeft(maxSpeed - 20, 80)
    time.sleep(0.2)
    m.driveForward(maxSpeed, 0, 300)
    time.sleep(0.2)
    m.turnLeft(maxSpeed - 20, 45)
    tokenAbove = f.driveToMarker(MARKER_PEDESTAL, rightPedestals[R.zone][1], direction = True, useMk1 = True)[1]
    if tokenAbove == True:
        l.top()
        m.driveForward(maxSpeed - 20, 0, a.getUsDistance() - 15)
    else:
        m.driveForward(maxSpeed - 20, 0, a.getUsDistance() - 5)
    d("planting token", "main")
    time.sleep(0.5)
    l.releaseToken()
    time.sleep(2)
    m.driveBackward(maxSpeed, 0, 60)
    l.tokenHeightAsync()
    time.sleep(0.2)
    f.driveToFixpoint(MARKER_PEDESTAL, rightPedestals[R.zone][1])
    m.turnRight(maxSpeed - 20, 80)
    time.sleep(0.2)
    m.driveForward(maxSpeed, 0, 90)
    time.sleep(0.2)
    m.turnRight(maxSpeed - 20, 80)
    time.sleep(0.2)
    m.driveForward(maxSpeed, 0, 390)
    time.sleep(0.2)
    m.turnRight(maxSpeed - 20, 80)
    time.sleep(0.2)
    nextToken = int(b.pop(0))
    m.driveForward(maxSpeed, 0, 40 + (nextToken * 40))
    time.sleep(0.2)
    m.turnLeft(maxSpeed - 20, 80)
    l.actionFinished.wait()
    return nextToken
    
def capCenterPedestal(tOffset):
    d("capturing center Pedestal", "main")
    d("searching nexttoken {0}".format(tOffset), "main")
    f.driveToMarker(MARKER_TOKEN, tokens[R.zone][tOffset], useMk1 = True, hadMarker = True)
    grabToken(MARKER_TOKEN, tokens[R.zone][tOffset])
    time.sleep(0.2)
    if tOffset == 4:
        m.turnRight(maxSpeed - 20, 175)
    if tOffset == 5:
        m.turnRight(maxSpeed - 20, 80)
        time.sleep(0.2)
        m.driveBackward(maxSpeed, 0, 45)
        time.sleep(0.2)
        m.turnRight(maxSpeed - 20, 80)
    if tOffset < 4:
        m.turnRight(maxSpeed - 20, 80)
        time.sleep(0.2)
        m.driveForward(maxSpeed, 0, 30 +((3 - tOffset) * 40))
        time.sleep(0.2)
        m.turnRight(maxSpeed - 20, 80)
        time.sleep(0.2)
    m.driveForward(maxSpeed, 0, 150)
    time.sleep(0.2)
    m.turnLeft(maxSpeed - 20, 45)
    f.driveToMarker(MARKER_PEDESTAL, 4, useMk1 = True)
    time.sleep(0.2)
    m.driveForward(maxSpeed, 0, a.getUsDistance() - 5)
    l.releaseToken()
    time.sleep(2)
    m.driveBackward(maxSpeed, 0, 70)
    return "BANANA!?"
    
def grabToken (type, offset):
    m.driveForward(maxSpeed, 0, a.getUsDistance())
    if l.grabToken():
        l.pedestalHeightAsync()
        m.driveBackward(maxSpeed, 0, 55)
        return 
    else:
        m.driveBackward(maxSpeed, 0, 60)
        f.driveToFixpoint(type, offset)
        grabToken(type, offset)

def run():
    m.driveForward(maxSpeed, 0, 25)
    time.sleep(0.2)
    m.turnLeft(maxSpeed - 20, 100)
    time.sleep(0.2)
    #m.driveForward(maxSpeed, 0, 45 + (40 * int(b[0])))
    
    nextToken = int(b.pop(0))
    nextMove = command.pop(0)
    while(True):
        if nextMove == "far-right":
            nextToken = capFarRightPedestal(nextToken)
            nextMove = command.pop(0)
        elif nextMove == "middle-right":
            nextToken = capMiddleRightPedestal(nextToken)
            nextMove = command.pop(0)
        elif nextMove == "nearest":                 #center
            nextToken = capNearestPedestal(nextToken)
            nextMove = command.pop(0)
        elif nextMove == "center":
            nextToken = capCenterPedestal(nextToken)
            nextMove = command.pop(0)
        elif nextMove == "middle-left":
            nextToken = capMiddleLeftPedestal(nextToken)
            nextMove = command.pop(0)
        elif nextMove == "far-left":
            nextToken = capFarLeftPedestal(nextToken)
            nextMove = command.pop(0)

def choosePedestal():
    if random.randrange(1,3) == 1:
        return MARKER_TOKEN, 20
    else:
        return MARKER_PEDESTAL, 6

def runShowOff():
    while(True):
        nextToken = int(b.pop(0))
        markers = f.driveToMarker(MARKER_TOKEN, nextToken, useMk1 = True)[0]
        grabToken(MARKER_TOKEN, nextToken)
        m.driveBackward(maxSpeed, 0, 40)
        pedestal = choosePedestal()
        tokenAbove = f.driveToMarker(MARKER_TOKEN, 23,  direction = True, useMk1 = True)[1]
        if tokenAbove == True:
            l.top()
            m.driveForward(255, 0, a.getUsDistance() - 15)
        else:
            m.driveForward(255, 0, a.getUsDistance() - 5)
        l.releaseToken()
        time.sleep(3)
        m.driveBackward(255, 0, 50)

d("starting threads", "main")
#voltaged.start()
l.start()
#motor.start()
#anticollisiond.start()

l.actionFinished.wait()

d.__init__()

d("starting action", "main")

l.tokenHeight()

runShowOff()
#run
