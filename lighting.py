import board
import neopixel
import time
import math
import random
from enum import Enum

currentTime = lambda: time.time() * 1000

HOUSE_COLORS = [
	(255, 0, 0),	# GRYIFFINDOR
	(0, 0, 255),	# RAVENCLAW
	(0, 255, 0),	# SLYTHERINE
	(255, 255, 0)	# HUFFLEPUFF
]

SPIN_DURATION = 7 * 1000
DWELL_DURATION = 30 * 1000
FADE_DURATION = 3 * 1000

def inOutCirc(p):
	if(p < 0.5):
		return 0.5 * (1 - math.sqrt(1 - 4 * (p * p)))
	else:
		return 0.5 * (math.sqrt(-((2 * p) - 3) * ((2 * p) - 1)) + 1)

class LightingState(Enum):
	IDLE = 1
	SPIN = 2
	ACTIVE = 3

class ActiveState(Enum):
	DWELL = 1
	FADE_OUT = 2
	FADE_IN = 3

class Lighting:

	def __init__(self):
		print("NeoPixel lighting active.")
		self.__pixels = neopixel.NeoPixel(board.D18, 3, brightness=1)
		self.__state = LightingState.IDLE
		self.__activeState = ActiveState.DWELL
		self.__currentHouse = 0

		self.__seed = 0
		self.__spinStart = 0
		self.__activeStart = 0

	def setActive(self, active):
		self.__seed = random.randrange(4)

		if active:
			print("Starting spin!")
			self.__spinStart = currentTime()
			self.__state = LightingState.SPIN
		else:
			print("Going idle.")
			self.__state = LightingState.IDLE
			self.__pixels.fill(HOUSE_COLORS[0])

	def update(self):
		if self.__state == LightingState.SPIN:
			elapsed = currentTime() - self.__spinStart
			if (elapsed < SPIN_DURATION):
				index = math.floor(self.__calculateSpin(elapsed))
				self.__currentHouse = index
				self.__setHouseColor(index)
				return
			
			print("Spin done. Setting Active.")
			self.__activeStart = currentTime()
			self.__state = LightingState.ACTIVE

		elif self.__state == LightingState.ACTIVE:
			elapsed = currentTime() - self.__activeStart

			if self.__activeState == ActiveState.DWELL:
				if (elapsed > DWELL_DURATION):
					print("Dwell done. Fading out")
					self.__activeStart = currentTime()
					self.__activeState = ActiveState.FADE_OUT

			elif self.__activeState == ActiveState.FADE_OUT:
				if (elapsed < FADE_DURATION):
					self.__setHouseColor(self.__currentHouse, 1 - self.__calculateFade(elapsed))
					return

				print("Fade out done. Fading in.")
				self.__currentHouse = (self.__currentHouse + 1) % len(HOUSE_COLORS)
				self.__activeStart = currentTime()
				self.__activeState = ActiveState.FADE_IN

			elif self.__activeState == ActiveState.FADE_IN:
				if (elapsed < FADE_DURATION):
					self.__setHouseColor(self.__currentHouse, self.__calculateFade(elapsed))
					return

				print("Fade in done. Dwell.")
				self.__activeStart = currentTime()
				self.__activeState = ActiveState.DWELL

	def clear(self):
		self.__pixels.fill((0, 0, 0))

	def __setHouseColor(self, index, brightness=1):
		color = HOUSE_COLORS[index]
		if brightness < 1:
			color = (
				int(color[0] * brightness), 
				int(color[1] * brightness), 
				int(color[2] * brightness))
		self.__pixels.fill(color)

	def __calculateSpin(self, time):
		progress = 1 - (SPIN_DURATION - time) / SPIN_DURATION
		return ((inOutCirc(progress) * 40) + self.__seed) % len(HOUSE_COLORS)

	def __calculateFade(self, time):
		progress = 1 - (FADE_DURATION - time) / FADE_DURATION
		return progress