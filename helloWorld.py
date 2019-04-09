from lx16a import *
from math import sin, cos
import time

# This is the port that the controller board is connected to
# This will be different for different computers
# On Windows, try the ports COM1, COM2, COM3, etc...
# On Raspbian, try each port in /dev/
LX16A.initialize("/dev/ttyUSB0")

# There should two servos connected, with IDs 1 and 2
servo1 = LX16A(1)
servo2 = LX16A(2)
servo3 = LX16A(3)
servo4 = LX16A(4)
servo5 = LX16A(5)
servo6 = LX16A(6)
servo7 = LX16A(7)
servo8 = LX16A(8)

t = 0
dura = 2500 #in milliseconds
servo1.moveTimeWrite(sin(0.2*t) * 60 + 60, dura)
servo2.moveTimeWrite(cos(0.2*t) * 60 + 60, dura)
time.sleep(2)
servo3.moveTimeWrite(sin(0.2*t) * 60 + 60, dura)
servo4.moveTimeWrite(cos(0.2*t) * 60 + 60, dura)
time.sleep(2)
servo5.moveTimeWrite(sin(0.2*t) * 60 + 60, dura)
servo6.moveTimeWrite(cos(0.2*t) * 60 + 60, dura)
time.sleep(2)
servo7.moveTimeWrite(sin(0.2*t) * 60 + 60, dura)
servo8.moveTimeWrite(cos(0.2*t) * 60 + 60, dura)

while True:
	# Two sine waves out of phase
	# The servos can rotate between 0 and 240 degrees,
	# So we adjust the waves to be in that range

	servo1.moveTimeWrite(sin(0.2*t) * 60 + 60)
	servo2.moveTimeWrite(cos(0.2*t) * 60 + 60)
	servo3.moveTimeWrite(sin(0.2*t) * 60 + 60)
	servo4.moveTimeWrite(cos(0.2*t) * 60 + 60)
	servo5.moveTimeWrite(sin(0.2*t) * 60 + 60)
	servo6.moveTimeWrite(cos(0.2*t) * 60 + 60)
	servo7.moveTimeWrite(sin(0.2*t) * 60 + 60)
	servo8.moveTimeWrite(cos(0.2*t) * 60 + 60)
	
	t += 0.01
