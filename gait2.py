import sys
import os
import time

from lx16a import LX16A, ServoError

# initialize
LX16A.initialize("/dev/ttyUSB2")

lift_range = [75, 115]

gait1_range = [
	[90, 170],
	lift_range,
	[170, 90],
	lift_range,
	[180, 100],
	lift_range,
	[100, 180],
	lift_range,
	[0, 150]
]

gait2_range = [
	[90, 170],
	lift_range,
	[90, 170],
	lift_range,
	[180, 100],
	lift_range,
	[180, 100],
	lift_range,
	[0,150]
]

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


class Robot(object):
	def __init__(self, legs, core):
		self.dura = 1000
		self.cycle = self.dura * 2 * 4
		self.legs = legs
		self.core = core

	def fold(self, dura=500):
		fold_pos = (180, 0)
		for leg in self.legs[1:]:
			servo1 = leg.servo1.servo
			servo2 = leg.servo2.servo
			servo1.moveTimeWrite(fold_pos[0], dura)
			servo2.moveTimeWrite(fold_pos[1], dura)
		time.sleep(dura/1000)
		self.core.servo.moveTimeWrite(0, dura)

	def spread(self, dura=500):
		self.core.servo.moveTimeWrite(90, dura)
		time.sleep(dura/1000)
		for i in range(4):
			leg = self.legs[i+1]
			print(2*i+1)
			spread_pos = (gait1_range[2*i][0], gait1_range[2*i+1][0])
			servo1 = leg.servo1.servo
			servo2 = leg.servo2.servo
			servo1.moveTimeWrite(spread_pos[0], dura)
			servo2.moveTimeWrite(spread_pos[1], dura)
		time.sleep(dura/1000)

	def gaitNaive(self, dura=500):
		while True:
			for leg in [self.legs[1], self.legs[3], self.legs[2], self.legs[4]]:
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


	def gaitSpin(self, dura=500):
		while True:
			for i in range(1):
				leg = self.legs[i+1]
				servo1 = leg.servo1.servo
				servo2 = leg.servo2.servo

				# raise leg
				servo2.moveTimeWrite(gait2_range[2*i+1][1], dura)
				# spin forward
				servo1.moveTimeWrite(gait2_range[2*i][1], dura)

				time.sleep(dura/1000)

				# drop leg
				servo2.moveTimeWrite(gait2_range[2*i+1][0], dura)

				time.sleep(dura/1000)

				# spin backward
				servo1.moveTimeWrite(gait2_range[2*i][0], dura*6)







if __name__ == "__main__":

	servos = ["undefined"]
	for i in range(9):
		servos.append(Servo(i+1, gait1_range[i][0], gait1_range[i][1]))

	legs = ["undefined"]
	legs.append(Leg(servos[1], servos[2]))
	legs.append(Leg(servos[3], servos[4]))
	legs.append(Leg(servos[5], servos[6]))
	legs.append(Leg(servos[7], servos[8]))
	
	Rollbot = Robot(legs, servos[9])
	Rollbot.spread(dura=1500)
	try:
		Rollbot.gaitNaive()
		# Rollbot.gaitSpin()
	except KeyboardInterrupt:
		print("Interrupted by keyboard")
		Rollbot.fold(dura=1500)
		try:
			sys.exit(0)
		except SystemExit:
			os.exit(0)