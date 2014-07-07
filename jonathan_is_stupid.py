class Character(object):

	def __init__(self, xPos, yPos, width, height):

		self.xPos = xPos
		self.yPos = yPos
		self.width = width
		self.height = height

	def printHi(self, msg):

		print(msg)

class Enemy(Character):

	def __init__(self, xPos, yPos, width, height):

		self.badness = 15

		Character.__init__(self, xPos, yPos, width, height)


Fred = Enemy(10,10,10,10)


Fred.printHi('hello')


