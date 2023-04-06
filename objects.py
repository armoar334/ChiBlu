#!/usr/bin/env python3

import random

class light:
	def __init__(self, color, brightness, x, y):
		self.color = color
		self.brightness = brightness
		self.x = x
		self.y = y

class entity:
	def __init__(self, x, y, faction, health, max_health, icon, color):
		self.x = x
		self.y = y
		self.faction = faction
		self.health = health
		self.max_health = max_health
		self.icon = icon
		self.color = color

	def move(self, xinc, yinc):
		self.x += xinc
		self.y += yinc

	def random_move(self):
		match random.randint(0, 3):
			case 0:
				self.y += 1
			case 1:
				self.x += 1
			case 2:
				self.y -= 1
			case 3:
				self.x -= 1


	def sanitise(self, xw_max, yw_max):
		if self.x <= 0:
			self.x = 0
		if self.x >= xw_max - 1:
			self.x = xw_max - 1

		if self.y <= 0:
			self.y = 0
		if self.y >= yw_max - 1:
			self.y = yw_max - 1

class item:
	def __init__(self, x, y, icon, color):
		self.x = x
		self.y = y
		self.icon = icon
		self.color = color