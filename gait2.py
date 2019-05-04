from lx16a import LX16A, ServoError
import time

# initialize
LX16A.initialize("/dev/ttyUSB0")

servos = ["undefined"]
for i in range(9):
	servos.append(LX16A(i+1))


def gaitNaive(servo1, servo2, dura=1000):

    # raise leg
	servo2.moveTimeWrite(90, dura)
	time.sleep(dura/1000)
    
    # spin forward
	servo1.moveTimeWrite(90, dura)
	time.sleep(dura/1000)

    # drop leg
	servo2.moveTimeWrite(55, dura)

	# spin backward
	servo1.moveTimeWrite(140, dura*9)

gaitNaive(servos[1], servos[2])
