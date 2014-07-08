import pygame
from random import randint
from random import uniform

BLUE = 	( 50, 80,220)
RED  = 	(230, 70, 90)
BLACK =	(  0,  0,  0)

class Character(object):

	def __init__(self, xPos, yPos, width, height):

		self.xPos = xPos
		self.yPos = yPos

		self.width = width
		self.height = height

		self.rect = pygame.Rect(self.xPos,self.yPos,self.width,self.height)

	def render(self, screen):

		pygame.draw.rect(screen, (RED), (self.xPos, self.yPos, self.width, self.height))

	# def detectCollisions(self,x1,y1,w1,h1,x2,y2,w2,h2):

	# 	self.x1 = x1
	# 	self.y1 = y1
	# 	self.w1 = w1
	# 	self.h1 = h1
	# 	self.x2 = x2
	# 	self.y2 = y2
	# 	self.w2 = w2	
	# 	self.h2 = h2

	# 	if self.x2 + self.w2 >= self.x1 >= self.x2 and self.y2 + self.h2 >= self.y1 >= self.y2:
	# 		return True

	# 	elif self.x2 + self.w2 >= self.x1 + self.w1 >= self.x2 and self.y2 + self.h2 >= self.y1 >= self.y2:
	# 		return True

	# 	elif self.x2 + self.w2 >= self.x1 >= self.x2 and self.y2 + self.h2 >= self.y1 + self.h1 >= self.y2:
	# 		return True

	# 	elif self.x2 + self.w2 >= self.x1 + self.w1 >= self.x2 and self.y2 + self.h2 >= self.y1 + self.h1 >= self.y2:
	# 		return True

	# 	else:
	# 		return False


class Player(Character):

	def __init__(self, xPos, yPos, width, height):

		self.xVel = 0
		self.yVel = 0

		Character.__init__(self, xPos, yPos, width, height)

class Enemy(Character):

	def __init__(self, xPos, yPos, width, height, type):

		self.xVel = uniform(2,3)
		self.yVel = 0
		self.type = type
		if self.type == 'tank':
			self.xVel = 1
			self.image_location = "images/tank.png"
			self.tank_img = pygame.image.load(self.image_location)
		elif self.type == 'helicopter':
			self.image_location = "images/helicopter.png"
			self.heli_img = pygame.image.load(self.image_location)
		# yPos = randint(64,250)
		Character.__init__(self, xPos, yPos, width, height)


	def render(self, screen):

		if self.type == 'tank':

			screen.blit(self.tank_img, (self.xPos, self.yPos))

		elif self.type == 'helicopter':

			screen.blit(self.heli_img, (self.xPos, self.yPos))

		else:

			pygame.draw.rect(screen, BLACK, (self.xPos, self.yPos, self.width, self.height))



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
			self.image_location = "images/cloud0.png"
		elif cloudnum == 1:
			self.image_location = "images/cloud1.png"
		elif cloudnum == 2:
			self.image_location = "images/cloud1.png"

		self.xVel = randint(1,4)
		self.yVel = 0

		yPos = randint(64,250)

		Character.__init__(self, xPos, yPos, width, height)

	def render(self, screen):

		image = pygame.image.load(self.image_location)

		screen.blit(image, (self.xPos, self.yPos))

class Heart(Character):

	def __init__(self, xPos, yPos, width, height):

		self.xVel = 0
		self.yVel = 5


		Character.__init__(self, xPos, yPos, width, height)

	def render(self, screen):

		pygame.draw.rect(screen, RED, (self.xPos, self.yPos, self.width, self.height))



