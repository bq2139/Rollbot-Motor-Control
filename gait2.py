import time

from lx16a import LX16A, ServoError

# initialize
LX16A.initialize("/dev/ttyUSB0")


class Servo(object):
	def __init__(self, id, lower=None, upper=None):
		self.id = id
		self.servo = LX16A(id)
		self.lower = lower
		self.upper = upper

	def rotateRange(self):
		return (self.lower, self.upper)


class Leg(object):
	def __init__(self, servo1, servo2):
		self.servo1 = servo1
		self.servo2 = servo2
		self.hori_range = servo1.rotateRange
		self.vert_range = servo2.rotateRange

	def ranges(self):
		return (self.vert_range, self.hori_range)



def gaitNaive(leg, dura=500):

	servo1 = leg.servo1.servo
	servo2 = leg.servo2.servo

	# raise leg
	servo2.moveTimeWrite(leg.servo2.upper, dura)
	# spin forward
	servo1.moveTimeWrite(leg.servo1.upper, dura)

	time.sleep(dura/1000)

	# drop leg
	servo2.moveTimeWrite(leg.servo2.lower, dura)

	time.sleep(dura/1000)

	# spin backward
	servo1.moveTimeWrite(leg.servo1.lower, dura*6)
	# time.sleep(dura*9/1000)

lift_range = [55, 95]

servo_range = [
	[90, 170],
	lift_range,
	[180, 100],
	lift_range,
	[170, 90],
	lift_range,
	[100, 180],
	lift_range
]

servos = ["undefined"]
for i in range(8):
	servos.append(Servo(i+1, servo_range[i][0], servo_range[i][1]))
# servo 1
# servos.append(Servo(1, 90, 170))
# # servo 2
# servos.append(Servo(2, 55, 95))

# servos.append(Servo(3, 180, 100))

# servos.append(Servo(4, 55, 95))

# servos.append(Servo(5, 170, 90))

# servos.append(Servo(6, 55, 95))

# servos.append(Servo(7, 100, 180))

# servos.append(Servo(8, 55, 95))


legs = ["undefined"]
# for i in range(4):
#	 legs.append((servos[2*i+1], servos[2*i+2]))
legs.append(Leg(servos[1], servos[2]))
legs.append(Leg(servos[5], servos[6]))
legs.append(Leg(servos[3], servos[4]))
legs.append(Leg(servos[7], servos[8]))

# servo1Range = (55, 90)
# servo2Range = (90, 140)


while True:
	gaitNaive(legs[1])
	gaitNaive(legs[2])
	gaitNaive(legs[3])
	gaitNaive(legs[4])

gaitNaive(legs[2])