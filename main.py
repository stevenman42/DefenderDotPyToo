import pygame, sys

from classes import *
from math import *

pygame.init()
pygame.mixer.init()
pygame.font.init()

#test


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

EverythingList = []		# not necessarily everything, just everything that needs to be rendered!

projectileList = []
CloudList = []
MortarList = []
TankList = []
EnemyList = []
HeartList = []

player = Player((960/2),(640-32),16,32)
EverythingList.append(player)

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
helicopter = pygame.image.load("images/helicopter.png")

laser = pygame.mixer.Sound("sounds/shoot.wav")
mortarSound = pygame.mixer.Sound("sounds/mortar.wav")
MortarDrop = pygame.mixer.Sound("sounds/mortardrop.wav")
HeliHit = pygame.mixer.Sound("sounds/helihit.wav")
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
			projectile.xVel = (mPos[0]-player.xPos)/(uniform(10.5,11.5))
		elif projectile.xPos > mPos[0]:
			projectile.xVel = (mPos[0]-player.xPos)/(uniform(10.5,11.5))

		if projectile.yPos < mPos[1]:
			projectile.yVel = ((HEIGHT-(HEIGHT-player.yPos)) - mPos[1])/(uniform(10.5,11.5))
		elif projectile.yPos > mPos[1]:
			projectile.yVel = -((HEIGHT-(HEIGHT-player.yPos)) - mPos[1])/(uniform(10.5,11.5))

		projectileList.append(projectile)
		EverythingList.append(projectile)

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
			EverythingList.append(mortProject)

			Money -= 5

	elif ActiveWeapon == 'triple laser':

		laser.play(loops = 0)

		for i in [10,12,14]:

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
			EverythingList.append(projectile)

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
				pass		# Maybe player movement sometime in the future, but probably not

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

			elif event.key == pygame.K_3:
				ActiveWeapon = 'triple laser'


		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT:
				pass

# End Keyboard Input #
	
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
		if cloud.xPos >= WIDTH + 128:
			CloudList.remove(cloud)
			EverythingList.remove(cloud)

	for projectile in projectileList:
		if projectile.yPos < 0 or projectile.xPos < 0 or projectile.xPos > WIDTH:
			projectileList.remove(projectile)
			EverythingList.remove(projectile)
			print(len(projectileList))

		for enemy in EnemyList:
			if enemy.xPos > -32 and enemy.xPos < WIDTH:
				enemy.rect = pygame.Rect(enemy.xPos,enemy.yPos,enemy.width,enemy.height)
				projectile.rect = pygame.Rect(projectile.xPos,projectile.yPos,projectile.width,projectile.height)

				if projectile.rect.colliderect(enemy.rect) or enemy.rect.contains(projectile.rect):
					if enemy in EnemyList:
						enemy.yVel = 18
						HeliHit.play(loops = 0)
						if randint(1,15) == 1:
							NewHeart = Heart(enemy.xPos, enemy.yPos, 16,16)
							HeartList.append(NewHeart)
							EverythingList.append(NewHeart)
					if projectile in projectileList:
						projectileList.remove(projectile)
					EverythingList.remove(projectile)
					Score += 1
					Money += 5
				if enemy.xPos >= WIDTH + 64:
					EnemyList.remove(enemy)
					EverythingList.remove(enemy)
				if enemy.yPos >= HEIGHT:
					EnemyList.remove(enemy)
					EverythingList.remove(enemy)
			else:
				pass

		for heart in HeartList:
			heart.rect = pygame.Rect(heart.xPos,heart.yPos,heart.width,heart.height)
			projectile.rect = pygame.Rect(projectile.xPos,projectile.yPos,projectile.width,projectile.height)

			if projectile.rect.colliderect(heart.rect):
				if heart in HeartList:
					HeartList.remove(heart)
					EverythingList.remove(heart)
					Lives += 1

	for mortar in MortarList:
		mortar.yVel += gravity
		if mortar.yPos > HEIGHT:
			MortarList.remove(mortar)
			EverythingList.remove(mortar)
			MortarDrop.play(loops = 0)

		for tank in TankList:
			tank.rect = pygame.Rect(tank.xPos,tank.yPos,tank.width,tank.height)
			mortar.rect = pygame.Rect(mortar.xPos,mortar.yPos,mortar.width,mortar.height)
			if mortar.rect.colliderect(tank.rect) or tank.rect.contains(mortar.rect):
				if tank in TankList:
					TankList.remove(tank)
					EverythingList.remove(tank)
				MortarList.remove(mortar)
				EverythingList.remove(mortar)
				Score += 2
				Money += 10

	for enemy in EnemyList:
		if enemy.xPos > WIDTH:
			EnemyList.remove(enemy)
			EverythingList.remove(enemy)
			Lives -= 1

	for heart in HeartList:
		if heart.yPos > HEIGHT:
			HeartList.remove(heart)
			EverythingList.remove(heart)

	if totalFrames % 60 == 0:
		NCX = randint(-100, -50)
		NCY = randint(64, 128)
		NewCloud = Cloud(NCX, NCY, 128, 64)
		CloudList.append(NewCloud)
		EverythingList.append(NewCloud)

		if randint(1,2) == 1:

			NEX = randint(-100,0)
			NEY = randint(64,300)

			NewEnemy = Enemy(NEX, NEY, 32, 16,'helicopter')

			EnemyList.append(NewEnemy)
			EverythingList.append(NewEnemy)

		if randint(1,2) == 1:

			NEX = randint(-100,0)
			NEY = HEIGHT-16

			NewEnemy = Enemy(NEX, NEY, 32, 16, 'tank')

			TankList.append(NewEnemy)
			EverythingList.append(NewEnemy)

	for tank in TankList:

		if tank.xPos > WIDTH/2:
			if tank in TankList:
				TankList.remove(tank)
				EverythingList.remove(tank)
				Lives -= 1

	for everything in EverythingList:
		everything.render(screen)
		everything.xPos += everything.xVel
		everything.yPos += everything.yVel

	pygame.draw.rect(screen, (0,0,0), (mPos[0] - 16, mPos[1] - 1, 32, 2))
	pygame.draw.rect(screen, (0,0,0), (mPos[0] - 1, mPos[1] - 16, 2, 32))
	pygame.draw.circle(screen, (200, 60, 70), (mPos[0], mPos[1]), 2)
	pygame.draw.circle(screen, (0,0,0), (mPos[0], mPos[1]),12,2)


	clock.tick(60)

	shootCount += 1
	totalFrames += 1

	pygame.display.flip()

