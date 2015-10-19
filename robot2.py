#    Copyright (C) 2105  wysiwyng
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from sr import *
import serial, time, function, motor, lift, voltaged, debug, anticollisiond, configReader

d = debug.Debug()
ser = serial.Serial("/dev/ttyUSB0", 115200)
m = motor.Motor(ser)
m.init()

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
[7, 8],
[5, 2],
[1, 0]]

homeMarker = [0, 21, 14, 7]

c = configReader.ConfigReader(R.usbkey, d)
v = voltaged.Voltaged(R, d)
l = lift.Lift(R)
f = function.Driver(R, motor, c.getMaxSpeed(), c.getDistModifier(), c.getDistModifierBegin(), (c.getCamResX(), c.getCamResY()))
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
    f.driveToMarker(MARKER_TOKEN, tokens[R.zone][tOffset])
    m.driveForward(maxSpeed, 0, a.getUsDistance())
    d("found token {0}, grabbing it".format(tOffset), "main")
    l.grabToken(3)
    m.driveBackward(maxSpeed, 0, 60)
    time.sleep(0.2)
    m.turnRight(maxSpeed - 20, 160)
    d("taking the token to pedestal {0}".format(nearPedestals[R.zone]), "main")
    f.driveToMarker(MARKER_PEDESTAL, nearPedestals[R.zone], direction = True)
    m.driveForward(maxSpeed - 20, 0, a.getUsDistance() - 5)
    d("planting token", "main")
    time.sleep(0.5)
    l.releaseToken()
    time.sleep(0.5)
    l.tokenHeightAsync()
    m.driveBackward(maxSpeed, 0, 84)
    time.sleep(0.2)
    m.turnRight(maxSpeed - 20, 160)
    nextToken = int(b.pop())
    return nextToken

def capMiddleLeftPedestal(tOffset):
    d("capturing middleleft Pedestal", "main")
    nextToken = int(b.pop(0))
    f.driveToMarker(MARKER_TOKEN, tokens[R.zone][tOffset])
    m.driveForward(maxSpeed, 0, a.getUsDistance())
    l.grabToken(3)
    m.driveBackward(maxSpeed, 0, 60)
    time.sleep(0.2)
    if tOffset == 4:
        m.driveForward(maxSpeed, 0, 10)
    if tOffset == 5:
        m.driveForward(maxSpeed, 0, 45)
    if tOffset < 4:
        m.driveBackward(maxSpeed, 0,155 - (40 * tOffset))
    m.turnLeft(maxSpeed - 20, 120)
    time.sleep(0.2)
    res = f.driveToMarker(MARKER_PEDESTAL, leftPedestals[R.zone][0])
    if f.lookForTokenAbove(res[0], res[1]):
        l.top()
        m.driveForward(maxSpeed - 20, a.getUsDistance() - 15)
    else:
        m.driveForward(maxSpeed - 20, a.getUsDistance() - 5)
    d("planting token", "main")
    time.sleep(0.5)
    l.releaseToken()
    time.sleep(0.5)
    l.tokenHeightAsync()
    m.driveBackward(maxSpeed, 0, 84)
    time.sleep(0.2)
    f.driveToFixpoint(MARKER_PEDESTAL, leftPedestals[R.zone][0])
    m.turnLeft(maxSpeed - 20, 90)
    m.driveForward(maxSpeed, 0, 100)
    if nextToken < 4:
        m.turnLeft(maxSpeed - 20, 90)
        m.driveForward(maxSpeed, 0, 155 - (40 * nextToken))
        m.turnRight(maxSpeed - 20, 90)
    elif nextToken == 5:
        m.turnRight(maxSpeed - 20, 90)
        m.driveForward(maxSpeed, 0, 45)
        m.turnLeft(maxSpeed - 20, 90)
    return nextToken
        
def capFarLeftPedestal(tOffset):
    d("capturing farleft pedestal", "main")
    nextToken = int(b.pop(0))
    f.driveToMarker(MARKER_TOKEN, tokens[R.zone][tOffset])
    m.driveForward(maxSpeed, 0, a.getUsDistance())
    l.grabToken(3)
    m.driveBackward(maxSpeed, 0, 60)
    time.sleep(0.2)
    arenaMarker = f.driveToFixpoint(MARKER_ARENA, homeMarker[R.zone])[0]
    m.turnLeft(maxSpeed - 20, 180)
    time.sleep(0.2)
    m.driveForward(maxSpeed, 0, int(400 - arenaMarker.dist * 100))
    time.sleep(0.2)
    m.turnRight(maxSpeed - 20, 45)
    res = f.driveToMarker(MARKER_PEDESTAL, leftPedestals[R.zone][1])
    if f.lookForTokenAbove(res[0], res[1]):
        l.top()
        m.driveForward(maxSpeed - 20, a.getUsDistance() - 15)
    else:
        m.driveForward(maxSpeed - 20, a.getUsDistance() - 5)
    d("planting token", "main")
    time.sleep(0.5)
    l.releaseToken()
    time.sleep(0.5)
    l.tokenHeightAsync()
    m.driveBackward(maxSpeed, 0, 84)
    f.driveToFixpoint(MARKER_PEDESTAL, leftPedestals[R.zone][1])
    time.sleep(0.2)
    m.turnLeft(maxSpeed - 20, 90)
    m.driveForward(maxSpeed, 0, 100)
    m.turnLeft(maxSpeed - 20, 90)
    m.driveForward(maxSpeed, 0, 355 - (40 * (tOffset + 1)))
    m.turnLeft(maxSpeed - 20, 44)
    return nextToken
        
def capMiddleRightPedestal(tOffset):
    d("capturing middle right pedestal", "main")
    nextToken = int(b.pop(0))
    f.driveToMarker(MARKER_TOKEN, tokens[R.zone][tOffset])
    m.driveForward(maxSpeed, 0, a.getUsDistance())
    l.grabToken(3)
    m.driveBackward(maxSpeed, 0, 60)
    m.turnLeft(maxSpeed - 20, 90)
    arenaMarker = f.driveToFixpoint(MARKER_ARENA, homeMarker[R.zone])[0]
    m.driveForward(maxSpeed, arenaMarker.dist * 100 - 100)
    f.driveToFixpoint(MARKER_ARENA, homeMarker[R.zone])
    m.turnLeft(maxSpeed - 20, 90)
    m.driveForward(maxSpeed, 0, 100)
    m.turnLeft(maxSpeed - 20, 45)
    res = f.driveToMarker(MARKER_PEDESTAL, rightPedestals[R.zone][0], direction = "right")
    if f.lookForTokenAbove(res[0], res[1]):
        l.top()
        m.driveForward(maxSpeed - 20, a.getUsDistance() - 15)
    else:
        m.driveForward(maxSpeed - 20, a.getUsDistance() - 5)
    d("planting token", "main")
    time.sleep(0.5)
    l.releaseToken()
    time.sleep(0.5)
    m.driveBackward(maxSpeed, 0, 84)
    l.tokenHeightAsync()
    f.driveToFixpoint(MARKER_PEDESTAL, rightPedestals[R.zone][0])
    m.turnRight(maxSpeed - 20, 90)
    m.driveForward(maxSpeed, 0, 100)
    m.turnRight(maxSpeed - 20, 90)
    m.driveForward(maxSpeed, 0, 200)
    m.turnRight(maxSpeed - 20, 90)
    m.driveForward(maxSpeed, 0, 45 + (nextToken * 40))
    m.turnLeft(maxSpeed - 20, 90)
    return nextToken

def capFarRightPedestal(tOffset):
    d("capturing far right pedestal", "main")
    nextToken = int(b.pop(0))
    f.driveToMarker(MARKER_TOKEN, tokens[R.zone][tOffset])
    m.driveForward(maxSpeed, 0, a.getUsDistance())
    l.grabToken(3)
    m.driveBackward(maxSpeed, 0, 60)
    m.turnLeft(maxSpeed - 20, 90)
    arenaMarker = f.driveToFixpoint(MARKER_ARENA, homeMarker[R.zone])[0]
    m.driveForward(maxSpeed, 0, arenaMarker.dist * 100 - 100)
    f.driveToFixpoint(MARKER_ARENA, homeMarker[R.zone])
    m.turnLeft(maxSpeed - 20, 90)
    m.driveForward(maxSpeed, 0, 300)
    m.turnLeft(maxSpeed - 20, 45)
    res = f.driveToMarker(MARKER_PEDESTAL, rightPedestals[R.zone][0], direction = "right")
    if f.lookForTokenAbove(res[0], res[1]):
        l.top()
        m.driveForward(maxSpeed - 20, a.getUsDistance() - 15)
    else:
        m.driveForward(maxSpeed - 20, a.getUsDistance() - 5)
    d("planting token", "main")
    time.sleep(0.5)
    l.releaseToken()
    time.sleep(0.5)
    m.driveBackward(maxSpeed, 0, 84)
    l.tokenHeightAsync()
    f.driveToFixpoint(MARKER_PEDESTAL, rightPedestals[R.zone][1])
    m.turnRight(maxSpeed - 20, 90)
    m.driveForward(maxSpeed, 0, 100)
    m.turnRight(maxSpeed - 20, 90)
    m.driveForward(maxSpeed, 0, 400)
    m.turnRight(maxSpeed - 20, 90)
    m.driveForward(maxSpeed, 0, 45 + (nextToken * 40))
    m.turnLeft(maxSpeed - 20, 90)
    return nextToken
    
def capCenterPedestal(tOffset):
    d("capturing center pedestal", "main")
    return 99999

def run():
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
        
d("starting threads", "main")
#voltaged.start()
l.start()
#motor.start()
#anticollisiond.start()

l.actionFinished.wait()

d.__init__()

d("starting action", "main")

run()
