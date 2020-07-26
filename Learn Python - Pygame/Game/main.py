#main.py
# pip install pygame

import pygame
import math
import random

pygame.init()

# ปรับหน้าจอ
WIDTH = 1000
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Uncle vs COVID-19') # set name of game

icon = pygame.image.load('icon.png') # load image into pygame
pygame.display.set_icon(icon) # set icon to game

background = pygame.image.load('bg.png')

######## < PLAYER > ###############
# 1 - player - player.png
player_image = pygame.image.load('player.png')
player_size = 128

px = 100 # start positionX (Horizontal)
py = HEIGHT - player_size # start positionY (verticle)
pxchange = 0

def Player(x,y):
	screen.blit(player_image,(x,y)) # วางภาพในหน้าจอ

######## < ENEMY > ################
# 2 - enemy - covid.png
esize = 64
eimg = pygame.image.load('covid.png')
ex = 50
ey = 0
eychange = 1

def Enemy(x,y):
	screen.blit(eimg,(x,y))

######## < MULTI ENEMY > ##########
exlist = [] # ตำแหน่งแกน x ของ enemy
eylist = [] # ตำแหน่งแกน y ของ enemy
ey_change_list = [] # ความเร็วของ enemy
allenemy = 2

for i in range(allenemy):
	exlist.append(random.randint(50, WIDTH - esize))
	eylist.append(random.randint(0, 100))
	ey_change_list.append(1) # กำหนดความเร็ว enemy เป็น 1 หลังยิงโดน

######## < BULLET > ###############
# 3 - bullet - mask.png
msize = 32
mimg = pygame.image.load('mask.png')
mx = 100
my = HEIGHT - player_size
mychange = 20
mstate = 'ready'

def fire_mask(x,y):
	global mstate
	mstate = 'fire'
	screen.blit(mimg,(x,y))

################ < COLLISION > ######################
def isCollision(ecx,ecy,mcx,mcy):
	# isCollision เช็คว่าชนกันหรือไม่ ถ้าชนให้ขึ้น True
	distance = math.sqrt(math.pow(ecx - mcx,2) + math.pow(ecy - mcy,2))
	print(distance)
	if distance < 48:
		return True
	else:
		return False

############## < SCORE > ############################
allscore = 0
font = pygame.font.Font('angsana.ttc',50)

def showscore():
	score = font.render('SCORE : {} '.format(allscore),True,(0,0,0,0))
	screen.blit(score,(30,30))

############ < SOUND > #############################
pygame.mixer.music.load('bg_music.mp3')
pygame.mixer.music.play()
pygame.mixer.music.set_volume(0.2)

########## < GAME OVER > ##########################
fontover = pygame.font.Font('angsana.ttc',80)
gameover = False

def GameOver():
	global gameover
	overtext = fontover.render('Game Over',True,(0,0,0))
	screen.blit(overtext,(400,400))

	if gameover == False:
		gameover = True

################ < GAME LOOP > ######################

running = True # บอกให้โปรแกรมทำงาน

clock = pygame.time.Clock()
FPS = 30 # frame rate

while running:

	for event in pygame.event.get():
		# run loop to check for quit pygame [x]
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				pxchange = -20
			if event.key == pygame.K_RIGHT:
				pxchange = 20

			if event.key == pygame.K_SPACE:
				if mstate == 'ready':
					mx = px + 50
					fire_mask(mx,my)
			if event.key == pygame.K_n:
				gameover = False
				for i in range(allenemy):
					eylist[i] = random.randint(0,100)
					exlist[i] = random.randint(50,WIDTH - esize)

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
				pxchange = 0

	############ < RUN PLAYER > #######################
    # px,py is position start for player
	Player(px,py)
	
	### ทำให้ player ขยับซ้ายขวาเมื่อชนขอบจอ
	if px <= 0:
		# หากชนขอบจอซ้าย ให้ปรับค่า pxchange เป็น +1
		px = 0
		px += pxchange # px = px + 1
	elif px >= WIDTH - player_size:
		# WIDTH (ความกว้างหน้าจอ - ความกว้างของภาพ)
		# หากชนขอบจอขวา ให้ปรับค่า pxchange เป็น -1
		px = WIDTH - player_size
		px += pxchange 
	else:
		# หากอยู่ระหว่างหน้าจอ จะทำการบวก ลบ ตาม pxchange 
		px += pxchange
	
	############# < RUN ENEMY SINGLE > #####################
		# Enemy(ex,ey)
		# ey += eychange

	############# < RUN MULTI ENEMY > #####################
	for i in range(allenemy):
		# เพิ่มความเร็วของ enemy
		if eylist[i] > HEIGHT - esize and gameover == False:
			for i in range(allenemy):
				eylist[i] = 1000
			GameOver() 
			break

		eylist[i] += ey_change_list[i]
		collisionMulti = isCollision(exlist[i],eylist[i],mx,my)
		if collisionMulti == True:
			my = HEIGHT - player_size
			mstate = 'ready'
			eylist[i] = 0
			exlist[i] = random.randint(50,WIDTH - esize)
			allscore += 10
			ey_change_list[i] += 1

		Enemy(exlist[i], eylist[i])


	############ < FIRE MASK > ######################
	if mstate == 'fire':
		fire_mask(mx,my)
		my -= mychange

	# เช็คว่า mask วิ่งไปชนขอบบนแล้วยัง? ถ้าชน เปลี่ยน state เป็น ready
	if my <= 0:
		my = HEIGHT - player_size
		mstate = 'ready'

			
	# เช็คว่าชนกันหรือยัง?
	collision = isCollision(ex,ey,mx,my)
	if collision == True:
		my = HEIGHT - player_size
		mstate = 'ready'
		ey = 0
		ex = random.randint(50,WIDTH - esize) 
		allscore += 10
		# สุ่มตำแหน่ง ความกว้างหน้าจอ - ขนาดของ virus

	showscore()
	print(px)
	pygame.display.update()
	pygame.display.flip()
	pygame.event.pump()
	screen.fill((0,0,0,))
	clock.tick(FPS)
	screen.blit(background,(0,0))
	