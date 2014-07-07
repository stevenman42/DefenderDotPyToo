import pygame
from random import randint

BLUE = ( 50, 80,220)
RED  = (230, 70, 90)

class Character(object):

	def __init__(self, xPos, yPos, width, height):

		self.xPos = xPos
		self.yPos = yPos

		self.width = width
		self.height = height

	def render(self, screen):

		pygame.draw.rect(screen, (RED), (self.xPos, self.yPos, self.width, self.height))


class Player(Character):

	def __init__(self, xPos, yPos, width, height):

		self.xVel = 0
		self.yVel = 0



		Character.__init__(self, xPos, yPos, width, height)

class Enemy(Character):

	def __init__(self, xPos, yPos, width, height):

		self.xVel = randint(2,6)
		self.yVel = 0
		yPos = randint(64,250)
		Character.__init__(self, xPos, yPos, width, height)

class Projectile(Character):

	def __init__(self, xPos, yPos, width, height):

		self.xVel = 0
		self.yVel = 0


		Character.__init__(self, xPos, yPos, width, height)

	def render(self, screen):

		pygame.draw.rect(screen, BLUE, (self.xPos, self.yPos, self.width, self.height))



class Cloud(Character):

	def __init__(self, xPos, yPos, width, height):

		cloudnum = randint(0,2)

		if cloudnum == 0:
			self.image_location = "/Users/Steven2/Desktop/Defender/images/cloud0.png"
		elif cloudnum == 1:
			self.image_location = "/Users/Steven2/Desktop/Defender/images/cloud1.png"
		elif cloudnum == 2:
			self.image_location = "/Users/Steven2/Desktop/Defender/images/cloud1.png"

		self.xVel = randint(1,4)
		self.yVel = 0

		yPos = randint(64,250)

		Character.__init__(self, xPos, yPos, width, height)

	def render(self, screen):

		image = pygame.image.load(self.image_location)

		screen.blit(image, (self.xPos, self.yPos))


		

