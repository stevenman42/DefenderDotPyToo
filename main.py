import pygame, sys

from classes import *
from math import *

pygame.init()
pygame.mixer.init()
pygame.font.init()



WIDTH = 960
HEIGHT = 640

BLUE =		( 50, 80,220)
RED  =		(230, 70, 90)
SKY_BLUE =	(191,244,255)

screen = pygame.display.set_mode((WIDTH,HEIGHT))

pygame.display.set_caption("Defender")

clock = pygame.time.Clock()
# pygame.event.set_grab(1)
pygame.mouse.set_visible(0)


player = Player((960/2),(640-32),16,32)
projectileList = []
CloudList = []
shootCount = 0
gravity = 0 # (default: 1.25)
totalFrames = 0
canShoot = True
EnemyList = []
Score = 0

laser = pygame.mixer.Sound("sounds/shoot.wav")
ground = pygame.image.load("images/ground.png")
font = pygame.font.Font(None, 36)








def GetMousePos():
	mPos = pygame.mouse.get_pos()
	return mPos

def GetMouseState():
	clict = pygame.mouse.get_pressed()[0]
	return clict

def Shoot():
	laser.play(loops = 0)

	projectile = Projectile(player.xPos, player.yPos, 8, 8)

	if projectile.xPos < mPos[0]:
		projectile.xVel = (mPos[0]-player.xPos)/(uniform(9.5,10.5))
	elif projectile.xPos > mPos[0]:
		projectile.xVel = (mPos[0]-player.xPos)/(uniform(9.5,10.5))

	if projectile.yPos < mPos[1]:
		projectile.yVel = ((HEIGHT-(HEIGHT-player.yPos)) - mPos[1])/(uniform(9.5,10.5))
	elif projectile.yPos > mPos[1]:
		projectile.yVel = -((HEIGHT-(HEIGHT-player.yPos)) - mPos[1])/(uniform(9.5,10.5))

	projectileList.append(projectile)

	y = HEIGHT-(HEIGHT-player.yPos)-mPos[1]

	x = mPos[0]-player.xPos

while True:

	for event in pygame.event.get():

		if event.type == pygame.QUIT:

			pygame.quit()
			sys.exit()

		elif event.type == pygame.KEYDOWN:

			if event.key == pygame.K_LEFT:

				player.xVel = -10

			elif event.key == pygame.K_RIGHT:

				pass

			elif event.key == pygame.K_ESCAPE:

				pygame.quit()
				sys.exit()

		elif event.type == pygame.KEYUP:

			if event.key == pygame.K_LEFT:

				player.xVel = 0


	player.xPos += player.xVel
	player.yPos += player.yVel

	for projectile in projectileList:

		projectile.xPos += projectile.xVel
		projectile.yPos += projectile.yVel
		projectile.yVel += gravity

	
	clict = GetMouseState()
	mPos = GetMousePos()

	if clict == 1:	# If the user left-clicks:
		mPos = GetMousePos()	# Retrieve the position of the cursor for processing

		if canShoot == True:
			Shoot()
			canShoot = False
			
		else:
			pass

	if clict == 0:
		canShoot = True


	screen.fill(SKY_BLUE)

	screen.blit(ground, (0, 0))

	text = font.render(str(Score), 1, (10, 10, 10))
	screen.blit(text, (10,10))


	for cloud in CloudList:

		cloud.xPos += cloud.xVel
		cloud.render(screen)

		if cloud.xPos >= WIDTH + 128:
			CloudList.remove(cloud)

	for i in projectileList:
		i.render(screen)
		if i.yPos < 0 or i.xPos < 0 or i.xPos > WIDTH:
			projectileList.remove(i)
			print(len(projectileList))

	for enemy in EnemyList:
		enemy.xPos += enemy.xVel
		if enemy.xPos > WIDTH:
			EnemyList.remove(enemy)
			Score -= 1

		for projectile in projectileList:
			collide = enemy.detectCollisions(projectile.xPos, projectile.yPos, projectile.width, projectile.height, enemy.xPos, enemy.yPos, enemy.width, enemy.height)
			if collide:
				print('HIT')
				EnemyList.remove(enemy)
				projectileList.remove(projectile)
				Score += 1
			if enemy.xPos >= WIDTH + 64:
				EnemyList.remove(enemy)


		enemy.render(screen)




	if totalFrames % 60 == 0:
		NCX = randint(-100, 0)
		NCY = randint(64, 128)

		NewCloud = Cloud(NCX, NCY, 128, 64)

		CloudList.append(NewCloud)

		NEX = randint(-2000,0)
		NEY = randint(64,128)

		NewEnemy = Enemy(NEX, NEY, 32, 16)

		EnemyList.append(NewEnemy)

	player.render(screen)

	pygame.draw.circle(screen, (200, 60, 70), (mPos[0], mPos[1]), 2)
	pygame.draw.circle(screen, (0,0,0), (mPos[0], mPos[1]),15,2)

	clock.tick(60)

	shootCount += 1
	totalFrames += 1

	pygame.display.flip()

