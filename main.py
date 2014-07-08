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
MortarList = []
TankList = []
EnemyList = []

shootCount = 0
gravity = 2
totalFrames = 0
canShoot = True
Score = 0
Lives = 10
Money = 0

MortarIcon = pygame.image.load("images/mortar_icon.png")
LaserIcon = pygame.image.load("images/laser_icon.png")
ground = pygame.image.load("images/ground.png")

tank = pygame.image.load("images/tank.png")

laser = pygame.mixer.Sound("sounds/shoot.wav")
mortarSound = pygame.mixer.Sound("sounds/mortar.wav")
MortarDrop = pygame.mixer.Sound("sounds/mortardrop.wav")
font = pygame.font.Font(None, 36)

ActiveWeapon = 'laser'
ActiveWeaponIcon = LaserIcon


def GetMousePos():
	mPos = pygame.mouse.get_pos()
	return mPos

def GetMouseState():
	clict = pygame.mouse.get_pressed()[0]
	return clict

def Shoot():
	global Money
	if ActiveWeapon == 'laser':
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
	elif ActiveWeapon == 'mortar':

		if Money >= 5:
			mortarSound.play(loops = 0)

			mortProject = Projectile(player.xPos, player.yPos, 16, 16)

			if mortProject.xPos < mPos[0]:
				mortProject.xVel = (mPos[0]-player.xPos)/(uniform(9.5,10.5))
			elif mortProject.xPos > mPos[0]:
				mortProject.xVel = (mPos[0]-player.xPos)/(uniform(9.5,10.5))

			if mortProject.yPos < mPos[1]:
				mortProject.yVel = ((HEIGHT-(HEIGHT-player.yPos)) - mPos[1])/(uniform(9.5,10.5))
			elif mortProject.yPos > mPos[1]:
				mortProject.yVel = -((HEIGHT-(HEIGHT-player.yPos)) - mPos[1])/(uniform(9.5,10.5))

			MortarList.append(mortProject)

			Money -= 5

	elif ActiveWeapon == 'triple laser':

		laser.play(loops = 0)

		for i in [8,10,12]:

			projectile = Projectile(player.xPos, player.yPos, 8, 8)

			if projectile.xPos < mPos[0]:
				projectile.xVel = (mPos[0]-player.xPos)/i
			elif projectile.xPos > mPos[0]:
				projectile.xVel = (mPos[0]-player.xPos)/i

			if projectile.yPos < mPos[1]:
				projectile.yVel = ((HEIGHT-(HEIGHT-player.yPos)) - mPos[1])/i
			elif projectile.yPos > mPos[1]:
				projectile.yVel = -((HEIGHT-(HEIGHT-player.yPos)) - mPos[1])/i

			projectileList.append(projectile)

			y = HEIGHT-(HEIGHT-player.yPos)-mPos[1]

			x = mPos[0]-player.xPos


while True:


# Keyboard Input #

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

			elif event.key == pygame.K_1:

				ActiveWeapon = 'laser'
				ActiveWeaponIcon = LaserIcon

			elif event.key == pygame.K_2:

				ActiveWeapon = 'mortar'
				ActiveWeaponIcon = MortarIcon


		elif event.type == pygame.KEYUP:

			if event.key == pygame.K_LEFT:

				pass
				# player.xVel = 0

# End Keyboard Input #


	player.xPos += player.xVel
	player.yPos += player.yVel

	for projectile in projectileList:

		projectile.xPos += projectile.xVel
		projectile.yPos += projectile.yVel

	
	clict = GetMouseState()
	mPos = GetMousePos()

# the stuff that happens when you click

	if clict == 1:	# If the user left-clicks:
		mPos = GetMousePos()	# Retrieve the position of the cursor for processing

		if canShoot == True:
			Shoot()
			canShoot = False
			
		else:
			pass

	if clict == 0:
		canShoot = True


	# screen.fill(SKY_BLUE)

	screen.blit(ground, (0, 0))


# Text (Score, Lives, Money!) #
	ScoreText = font.render(str(Score), 1, (10, 10, 10))
	screen.blit(ScoreText, (10,10))

	LivesText = font.render(str(Lives), 1, (255,10,10))
	screen.blit(LivesText, (10, 40))

	MoneyText = font.render(str(Money), 1, (80,205,50))
	screen.blit(MoneyText, (920, 10))


# Weapon Icons #

	screen.blit(ActiveWeaponIcon, (10, 70))



	for cloud in CloudList:

		cloud.xPos += cloud.xVel
		cloud.render(screen)

		if cloud.xPos >= WIDTH + 128:
			CloudList.remove(cloud)

	for projectile in projectileList:
		projectile.render(screen)
		if projectile.yPos < 0 or projectile.xPos < 0 or projectile.xPos > WIDTH:
			projectileList.remove(projectile)
			print(len(projectileList))

		for enemy in EnemyList:
			if enemy.xPos > -32 and enemy.xPos < WIDTH:
				enemy.rect = pygame.Rect(enemy.xPos,enemy.yPos,enemy.width,enemy.height)
				projectile.rect = pygame.Rect(projectile.xPos,projectile.yPos,projectile.width,projectile.height)

				if projectile.rect.colliderect(enemy.rect) or enemy.rect.contains(projectile.rect):
					print('HIT')
					if enemy in EnemyList:
						EnemyList.remove(enemy)
					projectileList.remove(projectile)
					Score += 1
					Money += 5
				if enemy.xPos >= WIDTH + 64:
					EnemyList.remove(enemy)
			else:
				pass

	for mortar in MortarList:
		mortar.yPos += mortar.yVel
		mortar.xPos += mortar.xVel
		mortar.yVel += gravity
		mortar.render(screen)
		if mortar.yPos > HEIGHT:
			MortarList.remove(mortar)
			MortarDrop.play(loops = 0)


		for tank in TankList:
			tank.rect = pygame.Rect(tank.xPos,tank.yPos,tank.width,tank.height)
			mortar.rect = pygame.Rect(mortar.xPos,mortar.yPos,mortar.width,mortar.height)
			if mortar.rect.colliderect(tank.rect) or tank.rect.contains(mortar.rect):
				print('HIT')
				if tank in TankList:
					TankList.remove(tank)
				MortarList.remove(mortar)
				Score += 2
				Money += 10


	for enemy in EnemyList:
		enemy.xPos += enemy.xVel
		if enemy.xPos > WIDTH:
			EnemyList.remove(enemy)
			Lives -= 1
		enemy.render(screen)




	if totalFrames % 60 == 0:
		NCX = randint(-100, -50)
		NCY = randint(64, 128)
		NewCloud = Cloud(NCX, NCY, 128, 64)
		CloudList.append(NewCloud)

		if randint(1,2) == 1:

			NEX = randint(-100,0)
			NEY = randint(64,300)

			NewEnemy = Enemy(NEX, NEY, 32, 16,'ship')

			EnemyList.append(NewEnemy)

		if randint(1,2) == 1:

			NEX = randint(-100,0)
			NEY = HEIGHT-16

			NewEnemy = Enemy(NEX, NEY, 32, 16, 'tank')

			TankList.append(NewEnemy)


	for tank in TankList:

		tank.xPos += tank.xVel
		if tank.xPos > WIDTH/2:
			if tank in TankList:
				print('bye')
				TankList.remove(tank)
				Lives -= 1
		tank.render(screen)


	player.render(screen)

	pygame.draw.circle(screen, (200, 60, 70), (mPos[0], mPos[1]), 2)
	pygame.draw.circle(screen, (0,0,0), (mPos[0], mPos[1]),15,2)

	clock.tick(60)

	shootCount += 1
	totalFrames += 1

	pygame.display.flip()

