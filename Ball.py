import pygame
from Constants import *

class Ball():
	def __init__(self, p_pos, p_radius, p_vel=pygame.math.Vector2()):
		self.pos = p_pos
		self.radius = p_radius
		self.vel = p_vel
		self.mass = self.radius*10

	def move(self):
		self.pos += self.vel

		#keep it on screen
		if self.pos.x < 0:
			self.pos.x = DISPLAY_WIDTH
		if self.pos.x > DISPLAY_WIDTH:
			self.pos.x = 0
		if self.pos.y < 0:
			self.pos.y = DISPLAY_HEIGHT
		if self.pos.y > DISPLAY_HEIGHT:
			self.pos.y = 0


		#friction
		self.vel *= 0.995
		if (abs(self.vel.x) < 0.001):
			self.vel.x = 0
		if (abs(self.vel.y) < 0.001):
			self.vel.y = 0
