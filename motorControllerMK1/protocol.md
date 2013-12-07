protocol specification
======================

the protocol consists of packets of 7 bytes:

$ <instruction byte> <speed byte> <direction byte> <distance int, high byte> <distance int, low byte>

byte description
================

instruction byte
----------------

-bit 7: always 1
-bit 6: always 1
-bit 5: always 0
-bit 4: always 1
-bit 3: always 1
-bit 2: forward/reverse
-bit 1: turn (do a in-place turn)
-bit 0: brake

brake bit can brake single motors, f/r bit is left motor, turn bit is right motor, if f/r=turn both motors brake

speed byte
----------

unsigned, sets the base speed of both motors

direction byte
--------------

signed, range -100 - 100, gives the direction the robot will drive

distance high/low byte
----------------------

unsigned int, high byte first, distance in centimeters to drive, if turn bit = 1 sets turn degrees, if dist = 0 drives infinitely until next brake/speed = 0 command
