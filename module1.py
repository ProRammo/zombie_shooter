#MAIN

#This is a top-down shooter game, where a player will face a round based system of zombies,
#where different rounds add different zombies and more zombies. It is play as long as you live and
#when you die you will be able to start over. In the game you have a store where you will be able
#to purchase more guns for a price, as well as grenades, nukes and lives.

from pygame import *
from random import *
from math import *
from sys import *

screen = display.set_mode((800,600),FULLSCREEN)

#--------------FUNCTIONS-------------#
#------------------------------------#

def cosd(degree):
    ang = degrees(degree)
    return cos(ang)

def sind(degree):
    ang = degrees(degree)
    return sin(ang)

#---------------CLASSES--------------#
#------------------------------------#

class Shooter:
    #this class will display the player and allow him to move around
    def __init__(self, image):
        self.image = image
        self.x, self.y = (400,300) #starting position 
        self.ang = 0 #starting anle of player
        self.picNum = 0
        self.count = 0 #sets a delay between the shooter sprites so he walks at a steady pace
        self.pic = 0
        self.health = 5 #health of the player
    def move(self):
        mx, my = mouse.get_pos()
        self.count += 1



        keys = key.get_pressed()

        if keys[K_a] and self.x > 50: #moves to the left
            self.x -= 4
            self.image = shooters[self.picNum] 
        if keys[K_d] and self.x < 750: #moves to the right
            self.x += 4
            self.image = shooters[self.picNum] 
        if keys[K_s] and self.y < 550: #moves downwards
            self.y += 4
            self.image = shooters[self.picNum]
        if keys[K_w] and self.y > 30: #moves forwards
            self.y -= 4
            self.image = shooters[self.picNum]

        self.ang = degrees(atan2(self.y - my, mx - self.x)) #changes the players angle to face the mouse

        self.pic = transform.rotate(self.image, self.ang) #changes the actual picture's angle
        imageWidth = self.pic.get_width()
        imageHeight = self.pic.get_height()
        screen.blit(self.pic, (self.x-imageWidth//2, self.y-imageHeight//2))

        self.image = shooters [0]
        if self.picNum == 0:
            self.picNum = 1
        if self.count % 7 == 0:
            if self.picNum == 1:
                self.picNum = 2
            elif self.picNum == 2:
                self.picNum = 1
    def getPicSize(self):
        imageSize=[self.pic.get_height(),self.pic.get_width()]
        return imageSize
    def getPicAngle(self):
        imageAngle=self.ang
        return imageAngle


class Bullet():
    def __init__(self, player, coord, imageSize, gunType):

        #Calculate unit vector between mouse and player
        self.player = player #x,y position of the player
        self.mx, self.my = coord #coordinates of the mouse
        dist = hypot(self.mx-self.player[X],self.my-self.player[Y]) #gets the distance between the player and the mouse

        try: 
            self.vx = (self.mx-self.player[X])/dist #finds the unit vector if the distance is greater than 0
            self.vy = (self.my-self.player[Y])/dist
        except:
            if dist == 0:
                dist = 1
                
        #Assume the gun is on an offset of of 21 pixels (X) from the center of the shooter
        #and 5 pixels (Y).
        self.x = self.player[X] + 21*self.vx - 5*self.vy
        self.y = self.player[Y] + 21*self.vy + 5*self.vx

        self.gunType = gunType
        self.bulletSize = 2
    def draw(self, bulletPositions, listPos):

        speed = 15 #speed of the bullet 

        bullet_vector = [self.vx * speed, self.vy * speed] #finds the unit vector in relation to the speed of the bullet 
        
        self.x += bullet_vector[0]  #adds the vector one unit at a time to the player's current position
        self.y += bullet_vector[1]

        bulletPositions[listPos][0] = self.x
        bulletPositions[listPos][1] = self.y


#---------------------------------------------------------------------------#
#defines the colour and size of the bullet for all of the
#different guns.
        if self.gunType == 'pistol':
            bulletColor = (0, 255, 255)
            self.bulletSize = 2
        elif self.gunType == 'gun1':
            bulletColor = (150, 150, 150)
            self.bulletSize = 2
        elif self.gunType == 'gun2':
            bulletColor = (200, 200, 200)
            self.bulletSize = 2
            
        elif self.gunType == 'gun3':
            bulletColor = (0, 255, 255)
            self.bulletSize = 1
        elif self.gunType == 'gun4':
            bulletColor = (200, 50, 60)
            self.bulletSize = 4
        elif self.gunType == 'gun5':
            bulletColor = (0, 0, 255)
            self.bulletSize = 2
        elif self.gunType == 'gun6':
            bulletColor = (200, 100, 50)
            self.bulletSize = 2
        elif self.gunType == 'gun7':
            bulletColor = (255, 0, 0)
            self.bulletSize = 2
        elif self.gunType == 'gun8':
            bulletColor = (0, 255, 0)
            self.bulletSize = 6
#---------------------------------------------------------------------------#
        draw.circle(screen, bulletColor, (int(self.x),int(self.y)), self.bulletSize) #draws the bullet
        
class Grenades():
    def __init__(self, position, grenadePic):
        self.x, self.y = position #pos where it will be dropped 
        self.image = grenadePic 
        self.timer = 200 #wait time before it explodes
        self.pause = 0 #delay time in between sprites
        
    def drop(self):
        #displays the grenade and waits for the timer to finish
        self.timer -= 1
        screen.blit(self.image, (self.x - 128/2, self.y - 130/2)) 
        if self.timer <= 0:
            return True
        return False

    def explode(self, picList):
        #displays the sprites with a delay in between  
        self.pause += 1

        if self.pause / 2 == 1:
            screen.blit(picList[0], (self.x - 128/2, self.y - 130/2))
        elif self.pause / 4 == 1:
            screen.blit(picList[1], (self.x - 128/2, self.y - 130/2))
        elif self.pause / 6 == 1:
            screen.blit(picList[2], (self.x - 128/2, self.y - 130/2))
        elif self.pause / 8 == 1:
            screen.blit(picList[3], (self.x - 128/2, self.y - 130/2))
        elif self.pause / 10 == 1:
            screen.blit(picList[4], (self.x - 128/2, self.y - 130/2))
        elif self.pause / 12 == 1:
            screen.blit(picList[5], (self.x - 128/2, self.y - 130/2))
            
            return True
        display.flip()
        return False
            
        
        

class Zombies():
    def __init__(self, zombieType, zombiePics, spawnPoint, playerPos):

        self.x, self.y = spawnPoint
        self.px, self.py = playerPos

        self.picNum = 1
        self.images = zombiePics
        self.image = self.images[self.picNum]
        self.ang = 0
        self.pic = self.image
        
        self.timer = 0

        # stats by zombie type
        self.type = zombieType
        if self.type == 1:          # regular zombie
            self.speed = -(uniform (0.6, 1.2))
            self.health = 1
            self.value = 50
        elif self.type == 2:        # beast zombie
            self.speed = -(uniform (0.2, 0.6))
            self.health = randint(10, 15)
            self.value = 500
        elif self.type == 3:        #freak zombie
            self.speed = -uniform(2.2, 2.8)
            self.health = 2
            self.value = 75
        elif self.type == 4:        #ghost zombie
            self.speed = -uniform(0.5, 2.0)
            self.health = 5
            self.value = 200
        elif self.type == 5:        #ninja zombie
            self.speed = -uniform(2.0, 2.5)
            self.health = randint(1, 8)
            self.value = 400

    def move(self, target, bulletPos):

        self.timer += 1

        # Choose rate at which zombie sprite changes
        # Formula assumes zombie speed is between (0.4, 1.9) -> timer speed (10, 15)
        # timer_speed = (34-10*zombie_speed) // 3
        if self.timer % ((34-10*self.speed)//3) == 0:
            self.picNum = (self.picNum+1)%4
        self.image = self.images[self.picNum]
        targetx, targety = target
        dist = hypot(targetx-self.x,targety-self.y)
        try:                                            #Make sure you are not dividing by 0
            self.vx = (targetx-self.x)/dist
            self.vy = (targety-self.y)/dist
        except:
            if dist ==0:
                dist=1
                
        speed = self.speed
        self.oldAng = self.ang
        self.ang = degrees(atan2(self.y - targety, targetx - self.x))

        zombie_vector = [self.vx * speed, self.vy * speed]              #Unit vector towards the player from the zombie


        self.x -= zombie_vector[0]
        self.y -= zombie_vector[1]

        self.pic = transform.rotate(self.image, self.oldAng)        #rotate the image to face the player

        imageWidth = self.pic.get_width()
        imageHeight = self.pic.get_height()
        #draw.rect(screen, (255,255,255), (self.x - pic.get_width()//2, self.y - pic.get_height()//2, pic.get_width(), pic.get_height()), 1)
        screen.blit(self.pic, (self.x-imageWidth//2, self.y-imageHeight//2))


        for bullet in bulletPos:        #Check if a bullet hit a zombie
            if bullet[0] > self.x - self.pic.get_width()//2 and bullet[0] <  self.x + self.pic.get_width()//2 and bullet[1] > self.y - self.pic.get_height()//2 and bullet[1] < self.y + self.pic.get_height()//2:
                return [True, bullet]


    def remove(self, zombiePic, spawnPoint, playerPos):
        self.x, self.y = spawnPoint
        self.px, self.py = playerPos
        self.image = zombiePic
        

#----------------VARIABLES----------------#
#-----------------------------------------#
pistol = [image.load("pistol.png"),0,"pistol"]
availableGuns = []
availableGuns.append(pistol)  
X = 0
Y = 1
stand = 0
rightFoot = 2
leftFoot = 1
black = ( 0, 0, 0)
white = ( 255, 255, 255)
red = ( 255, 0, 0)
blue = ( 0, 0, 255)
#---------------------------------------------------------------------------#
#---------------------------------------------------------------------------#
shooters = [image.load("shooter2002.png"), image.load("shooter2001.png"), image.load("shooter2003.png")]
shotgun = image.load("shotgun.png")
startMenu = image.load("startMenu.png")
startScreen = image.load("start.png").convert()
pauseMenu = image.load("pauseMenu.png")
buttonTransRect = image.load("transRectMenu.png")
storePic = image.load("store.png")
itemsTransRect = image.load("items.png")
menuTransRect = image.load("storeMenu.png")
rightArrow = image.load("rightArrowTrans.png")
leftArrow = image.load("leftArrow.png")
transLeftArrow = image.load("leftArrowTrans.png")
transRightArrow = image.load("rightArrow.png")
roundPage = image.load("roundPage.png")
gameOverScreen = image.load("gameOverScreen.png")
creditsPic = image.load("credits.png")
optionsPic = image.load("options.png")
nukePic = image.load("nuke.png")
gPic = image.load("grenadePic.png")
explosionPic = image.load("explosion.png").convert()

# multidimensional array where each dimension contains an array of sprite images
#   - index 0 = zombie type 1 = regular zombie
#   - index 1 = zombie type 2 = beast zombie
zombPics = [[],[], [], [], [], []]
for i in range(1, 5):
    zombPics[0].append(image.load("zombie - "+str(i)+".png"))       # regular (type 1)
    zombPics[1].append(image.load("zombieBeast - "+str(i)+".png"))  # beast (type 2)
    zombPics[2].append(image.load("zombieFreak - "+str(i)+".png"))  # freak (type 3)
    zombPics[3].append(image.load("zombieGhost - "+str(i)+".png"))  # ghost (type 4)
    zombPics[4].append(image.load("zombieNinja - "+str(i)+".png"))  # ninja (type 5)

grenadePics = []
for i in range (1, 7):
    grenadePics.append(image.load("ex"+str(i)+".png"))

grenadePic = image.load("grenade1.png")
bgr = [image.load("Map1.png"),image.load("Map2.png")]
bgrReal = choice(bgr)
blood = image.load("blood.png").convert()
playerPic = image.load("shooter2002.png")
#---------------------------------------------------------------------------#
#---------------------------------------------------------------------------#


#---------------------------------------------------------------------------#
#-------------------------------Flags---------------------------------------#
paused = False
running = True
zombieSpawn = True
playerAlive = True
bloodHit = False        #if the player got hit
started = False
clicked = False         #if you click the mouse to shoot
tapped = False          #if you press a keyboard button
startOver = False
store = False
roundOver = False
gun1Bought = False
gun2Bought = False
gun3Bought = False
gun4Bought = False
gun5Bought = False
gun6Bought = False
gun7Bought = False
gun8Bought = False
canShoot = True            #Time between shots for different guns
gameOver = False
options = False
creditss = False
optionss = False
creditsss = False
nukeOn = False

#---------------------------------------------------------------------------#
#---------------------------------------------------------------------------#

#---------------------------------------------------------------------------#
#------------------------------Rects----------------------------------------#
startRect = Rect(290,200,215,61)
optionsRect = Rect(288,280,215,61)
creditsRect = Rect(288,362,215,61)
quitRect = Rect(288,442,215,61)
resumeRect = Rect(288,171,215,61)
storeRect = Rect(288,253,215,61)
pauseOptionsRect = Rect(288,335,215,61)
pauseCreditsRect = Rect(288,415,215,61)
pauseQuitRect = Rect(288,495,215,61)
storeMenuRect = Rect(10,12,132,61)
gun1Rect = Rect(77,238,112,62)
gun2Rect = Rect(209,238,112,62)
gun3Rect = Rect(341,238,112,62)
gun4Rect = Rect(473,238,112,62)
gun5Rect = Rect(605,238,112,62)
gun6Rect = Rect(77,327,112,62)
gun7Rect = Rect(209,327,112,62)
gun8Rect = Rect(341,327,112,62)
grenadeRect = Rect(473,327,112,62)
perk1Rect = Rect(605,327,112,62)
perk4Rect = Rect(341,416,112,62)
rightArrowRect = Rect(250,5,37,41)
leftArrowRect = Rect(110,5,37,41)
#---------------------------------------------------------------------------#
#---------------------------------------------------------------------------#
blood.set_colorkey(blood.get_at((400,300)))
screen.blit(bgrReal ,(0,0))
bulletPositions = []


player = Shooter(playerPic)
bullets=[]
zombies=[]
myClock = time.Clock()

zombieAmt=16
zombieTimer = 0
playerTimer = 0
bloodTimer = 0
zombieHealth = 1
choiceList = [(0, 300), (400, 0), (400, 600), (800, 300)]           #Chose where the zombie will spawn (4 sides, random)

zombieRate = 100
score = 0
cash = 0
gunStrength = 0                     #Damage dealt to the zombies based on gun type
transCounter = 255                  #control transparency of pictures


roundCount = 0
roundNum = 1


#----------------------------------------------------------#
#------------------Weapon Variables------------------------#
gun1 = [image.load("gun1.png"),5000,"gun1"]
gun2 = [image.load("gun2.png"),9500,"gun2"]
gun3 = [image.load("gun3.png"),14000,"gun3"]
gun4 = [image.load("gun4.png"),17000,"gun4"]
gun5 = [image.load("gun5.png"),22000,"gun5"]
gun6 = [image.load("gun6.png"),29000,"gun6"]
gun7 = [image.load("gun7.png"),75000,"gun7"]
gun8 = [image.load("gun8.png"),500000,"gun8"]

gun = availableGuns[0][2]
zombTypeChoose = [1,1,1,1,1,1,1]            #Chose which zombie type you can spawn(random)
cash = 0

currentGun = 0
grenades = []
grenadeAmt = 3
nukeAmt = 1

exTransparency = 0
machineGunCounter = 0

#----------------------------------------------------------#
#-------------FONTS---------------------#
#---------------------------------------#
font.init()
scoreFont = font.SysFont(None, 36)
roundFont = font.SysFont(None, 36)
healthFont = font.SysFont(None, 36)
grenadeFont = font.SysFont(None, 28)
nukeFont = font.SysFont(None, 28)
newRoundFont = font.SysFont(None, 300)
scoreTxt = scoreFont.render(str(score), 1, (255,255,255))
roundTxt = roundFont.render("Round "+str(zombieHealth), 1, (255,255,255))
healthTxt = healthFont.render("Health --> "+str(player.health), 1, (255,255,255))
newRoundtxt = newRoundFont.render(str(roundNum+1), 1, (255,255,255))
screen.blit(scoreTxt, (10,10))
screen.blit(roundTxt, (10,590))
screen.blit(healthTxt, (550, 10))

#---------------MAIN--------------------#
#---------------------------------------#

display.flip()
while running:
    clicked = False
    tapped = False
    grenadeTF = True
    mx,my = mouse.get_pos()
    mb = mouse.get_pressed()
    keys = key.get_pressed()
    for evt in event.get():
        keys = key.get_pressed()
        mb = mouse.get_pressed() 
        if evt.type == QUIT:
            running = False
        if evt.type == KEYDOWN and keys[K_p]:
            paused = True
        if evt.type == MOUSEBUTTONDOWN and mb[0] == 1:
            clicked = True
        if evt.type == KEYDOWN:
            tapped = True
        if evt.type == KEYDOWN and keys[K_SPACE] and grenadeAmt >= 1:
            grenade = Grenades((player.x, player.y), grenadePic) #calls the grenade class
            grenades.append(grenade)
            grenadeAmt -= 1
        if evt.type == KEYDOWN and keys[K_x] and nukeAmt >= 1:
            nukeAmt -= 1
            del zombies[:] #deletes all of the zombies on the screen
            nukeOn = True
            
    if not started:
        player.health = 5
        healthTxt = healthFont.render("Health --> "+str(player.health), 1, (255,255,255))
        mouse.set_cursor(*cursors.arrow)
        while transCounter > 0:
            screen.fill((0, 0, 0))
            transCounter -= 0.1 #loading screen transparency
            startScreen.set_alpha(transCounter)
            screen.blit(startScreen, (0,0))
            display.flip()
        if transCounter <= 0: #when the loading screen is done, if starts the main menu
            screen.blit(startMenu, (0,0))
            if startRect.collidepoint(mx,my):
                screen.blit(buttonTransRect, (288,198))
                if clicked:
                    started = True #starts the game
                    screen.blit(bgrReal, (0,0))
                    screen.blit(scoreTxt, (10,10))
                    screen.blit(roundTxt, (10, 570))
                    screen.blit(healthTxt, (550, 10))
            if optionsRect.collidepoint(mx,my):
                screen.blit(buttonTransRect,(288,280))
                if clicked:
                    options = True #displays the options and instructions
            if creditsRect.collidepoint(mx,my):
                screen.blit(buttonTransRect,(288,362))
                if clicked:
                    creditss = True #displays the credits 
            if quitRect.collidepoint(mx,my):
                screen.blit(buttonTransRect,(288,442))
                if clicked:
                    running = False #kills the program
            if options:
                screen.blit(optionsPic,(0,0))
                if storeMenuRect.collidepoint(mx,my):
                    screen.blit(menuTransRect,(10,12))
                    if clicked:
                        options = False
            if creditss:
                screen.blit(creditsPic,(0,0))
                if storeMenuRect.collidepoint(mx,my):
                    screen.blit(menuTransRect,(10,12))
                    if clicked:
                        creditss = False
            display.flip()
    if started:
        if not paused:
            mouse.set_cursor(*cursors.broken_x)
            player.move() #calls the method inside of Shooter which allows him to move and be displayed on the screen 
            mx,my = mouse.get_pos()
            keys = key.get_pressed()
            zombPic = choice(zombPics)
            nukeTxt = nukeFont.render(str(nukeAmt), 1, (255,255,255))
            grenadeTxt = grenadeFont.render(str(grenadeAmt), 1, (255,255,255))
            screen.blit(nukePic,(630,563))
            screen.blit(nukeTxt,(675,573))
            screen.blit(gPic,(700,563))
            screen.blit(grenadeTxt,(740,573))
            screen.blit(leftArrow,(110,5))
            screen.blit(rightArrow,(250,5))
            screen.blit(availableGuns[currentGun][0],(145,0))
            #------------------------------------------------------------------------------#
            #---------------------------------Switching Guns-------------------------------#
            #switches between the guns you have purchased and displays the one you are using 
            if leftArrowRect.collidepoint(mx,my) or keys[K_q] and tapped:
                screen.blit(transLeftArrow,(110,5))
                if clicked or keys[K_q] and tapped:
                    canShoot = True
                    if currentGun != 0:
                        currentGun -= 1
                    else:
                        currentGun = len(availableGuns) - 1
            if rightArrowRect.collidepoint(mx,my) or keys[K_e] and tapped:
                screen.blit(transRightArrow,(250,5))
                if clicked or keys[K_e] and tapped:
                    canShoot = True
                    if currentGun == len(availableGuns) - 1:
                        currentGun = 0
                    else:
                        currentGun += 1
            #------------------------------------------------------------------------------#
            gun = availableGuns[currentGun][2] #sets gun to the gun in current
            
            #------------------------------------------------------------------------------#
            #-----------------------Setting what the Guns do-------------------------------#
            
            if gun == 'pistol':
                if clicked:
                    bullet = Bullet([player.x, player.y], (mx,my), player.getPicSize(), 'pistol')
                    bullets.append(bullet)
                    bulletPositions.append([bullet.x, bullet.y])
                    gunStrength = 1
            elif gun == 'gun1':   #pistol
                if playerTimer % 20 == 0:
                    canShoot = True
                if clicked and canShoot:
                    bullet = Bullet([player.x, player.y], (mx,my), player.getPicSize(), 'gun1')
                    bullets.append(bullet)
                    bulletPositions.append([bullet.x, bullet.y])
                    gunStrength = 1.5
            elif gun == 'gun2':     #pistol
                if mb[0]==1 and machineGunCounter % 10 == 0:
                    bullet = Bullet([player.x, player.y], (mx,my), player.getPicSize(), 'gun2')
                    bullets.append(bullet)
                    bulletPositions.append([bullet.x, bullet.y])
                    gunStrength = 1.5
            elif gun == 'gun3':     #submachinegun
                if mb[0]==1 and machineGunCounter % 4 == 0:
                    bullet = Bullet([player.x, player.y], (mx,my), player.getPicSize(), 'gun3')
                    bullets.append(bullet)
                    bulletPositions.append([bullet.x, bullet.y])
                    gunStrength = 0.4
            elif gun == 'gun4':     #shotgun
                if playerTimer % 20 == 0:
                    canShoot = True
                if clicked and canShoot:     
                    bullet = Bullet([player.x, player.y], (mx,my), player.getPicSize(), 'gun4')
                    bullets.append(bullet)
                    bulletPositions.append([bullet.x, bullet.y])
                    gunStrength = 6
                    canShoot = False
            elif gun == 'gun5':     #machinegun
                if mb[0]==1 and machineGunCounter % 11 == 0:
                    bullet = Bullet([player.x, player.y], (mx,my), player.getPicSize(), 'gun5')
                    bullets.append(bullet)
                    bulletPositions.append([bullet.x, bullet.y])
                    gunStrength = 2
            elif gun == 'gun6':     #machinegun
                if mb[0]==1 and machineGunCounter % 11 == 0:
                    bullet = Bullet([player.x, player.y], (mx,my), player.getPicSize(), 'gun6')
                    bullets.append(bullet)
                    bulletPositions.append([bullet.x, bullet.y])
                    gunStrength = 2.7
            elif gun == 'gun7':     #lightmachinegun
                if mb[0]==1 and machineGunCounter % 9 == 0:
                    bullet = Bullet([player.x, player.y], (mx,my), player.getPicSize(), 'gun7')
                    bullets.append(bullet)
                    bulletPositions.append([bullet.x, bullet.y])
                    gunStrength = 3
            elif gun == 'gun8':     #raygun
                if playerTimer % 15 == 0:
                    canShoot = True
                if clicked and canShoot:     
                    bullet = Bullet([player.x, player.y], (mx,my), player.getPicSize(), 'gun8')
                    bullets.append(bullet)
                    bulletPositions.append([bullet.x, bullet.y])
                    gunStrength = 3
                    canShoot = False
                    
            
                    
            playerTimer += 1
            for z in zombies:
                bulletHitStats= z.move((player.x,player.y), bulletPositions)
                z.move((player.x,player.y), bulletPositions)
                zombieRect = Rect(z.x - z.pic.get_width()//4, z.y - z.pic.get_height()//4, z.pic.get_width()//2, z.pic.get_height()//2)
                playerRect = Rect(player.x - player.pic.get_width()//4, player.y - player.pic.get_height()//4, player.pic.get_width()//2, player.pic.get_height()//2)
                if zombieRect.colliderect(playerRect) and playerTimer % 20 == 0:
                    player.health -= 1
                    healthTxt = healthFont.render("Health --> "+str(player.health), 1, (255,255,255))
                    bloodHit = True
                    bloodTimer = 0
                    bloodTransparency = 0
                    screen.blit(blood,(0,0))
                    time.wait(1)
                    
                    if player.health <= 0: #sets all of the variables back to what they were in the begining so that can restart
                        gameOver = True
                        playerAlive = False
                        started = False
                        del zombies[:]
                        del bullets[:]
                        del bulletPositions[:]
                        zombTypeChoose = [1,1,1,1,1,1,1]
                        roundNum = 1
                        player.health = 5
                        del availableGuns[:]
                        availableGuns.append(pistol)
                        score = 0
                        cash = 0
                        bloodTimer = 0
                        bloodTransparency = 0
                        display.flip()


                #deletes the bullet when it hits a zombie unless it is the ray gun
                if bulletHitStats!=None:
                    if bulletHitStats[0] and bulletHitStats[1]in bulletPositions:
                        if gun != 'gun8':
                            del bullets[bulletPositions.index(bulletHitStats[1])]
                            bulletPositions.remove(bulletHitStats[1])

                        z.health -= gunStrength
                        if z.health <= 0:
                            cash += z.value
                            
                            zombies.remove(z)
                            score = cash
                            scoreTxt = scoreFont.render(str(score), 1, (255,255,255))
            #sets a timer for the blood which fades out everytime you get hit                            
            if bloodHit == True:
                bloodTransparency += 1
                if bloodTransparency == 255:
                    bloodTransparency = 0
                    bloodHit = False
                    
            #sets a timer for the explosion which fades out everytime you use a nuke
            if nukeOn == True:
                exTransparency += 1
                if exTransparency == 255:
                    exTransparency = 0
                    nukeOn = False

                                
            if not roundOver and not nukeOn:
                zombieTimer += 1
                if zombieTimer % zombieRate == 0:
                    zombCoord = choice([(0,300),(400,0),(400,600),(800,300)])
                    zombType = choice(zombTypeChoose)
                    
                    zombie = Zombies(zombType, zombPics[zombType-1], zombCoord, (player.x, player.y))
                    roundCount += 1
                    zombies.append(zombie)
                    zombieRate = (roundNum+15)*2
                                
            
            if roundCount == roundNum*12: #adds more zombies each round 
                roundNum += 1
                roundTxt = roundFont.render("Round "+str(roundNum), 1, (255,255,255))
                roundCount = 0
                roundOver = True

            #displays a round page with the number everytime the round changes 
            if zombies == [] and roundOver and player.health > 0:
                newRoundtxt = newRoundFont.render(str(roundNum), 1, (255,255,255))
                screen.blit(roundPage, (0,0))
                screen.blit(newRoundtxt, (350, 300))
                display.flip()
                time.wait(2000)
                roundOver = False
                
            keys = key.get_pressed()

            
            for g in grenades:
                g.drop() #drops the grenade itself
                if g.drop():
                    g.explode(grenadePics) #runs the sprite for the explosion
                    
                    for z in zombies:
                        exDist = hypot(z.x - g.x, z.y - g.y)
                        if exDist <= 80:
                            cash += z.value//3
                            zombies.remove(z)
                    if g.explode(grenadePics): #removes that grenade when the explosion is complete 
                        grenades.remove(g)
                        
            for bullet in bullets:
                bullet.draw(bulletPositions, bullets.index(bullet)) #calls a method in Bullet which draws the bullets on the screen 

                if bullet.x > 800 or bullet.x < 0 or bullet.y > 600 or bullet.y < 0: #deletes the bullets if they're off the screen 
                    del bulletPositions[bullets.index(bullet)]
                    bullets.remove(bullet)

            
                
            machineGunCounter += 1
            if roundNum >= 22:
                zombTypeChoose.append(2)
                zombTypeChoose.append(2)
                zombTypeChoose.append(3)
                zombTypeChoose.append(4)
                zombTypeChoose.append(5)
            elif roundNum >= 15:
                zombTypeChoose.append(2)
                zombTypeChoose.append(3)
                zombTypeChoose.append(4)
                zombTypeChoose.append(3)
                zombTypeChoose.append(4)
                zombTypeChoose.remove(1)
            elif roundNum >= 8:
                zombTypeChoose.append(2)
                zombTypeChoose.append(3)
                zombTypeChoose.append(3)
                zombTypeChoose.append(3)
                zombTypeChoose.append(1)
            elif roundNum >= 4:
                zombTypeChoose.append(1)
                zombTypeChoose.append(1)
                zombTypeChoose.append(1)
                zombTypeChoose.append(1)
                zombTypeChoose.append(2)
            else:
                zombTypeChoose.append(1)
            
            myClock.tick(60)
            display.flip()
            screen.blit(bgrReal, (0,0))
            if bloodHit == True: #displays teh blood effect when you get hit
                blood.set_alpha(255-bloodTransparency)
                screen.blit(blood, (0,0))
            if nukeOn == True: #displays the explosion effect when you use a nuke 
                explosionPic.set_alpha(255-exTransparency)
                screen.blit(explosionPic, (0,0))
            screen.blit(scoreTxt, (10,10))
            screen.blit(roundTxt, (10, 570))
            screen.blit(healthTxt, (550, 10))
            
            if gameOver: #sets variables back to their original form and restarts the game 
                screen.blit(gameOverScreen, (0,0))
                gameOver = False
                bloodHit = False
                scoreTxt = scoreFont.render(str(score), 1, (255,255,255))
                roundTxt = roundFont.render("Round "+str(roundNum), 1, (255,255,255))
                player.x, player.y = (400,300)
                grenadeAmt = 3
                nukeAmt = 1
                display.flip()
                time.wait(3000)
                
                    
        else:
            #enters the pause menu 
            mouse.set_cursor(*cursors.arrow)
            screen.blit(pauseMenu,(0,0))
            for evt in event.get():
                keys = key.get_pressed()
                if evt.type == QUIT:
                    running = False
                if evt.type == MOUSEBUTTONDOWN:
                    clicked = True
            if resumeRect.collidepoint(mx,my):
                screen.blit(buttonTransRect,(288,171))
                if clicked:
                    paused = False #resumes the game 
            if storeRect.collidepoint(mx,my):
                screen.blit(buttonTransRect,(288,253))
                if clicked:
                    if mb[0] == False:
                        store = True #takes you into the store 
                    
            if pauseOptionsRect.collidepoint(mx,my):
                screen.blit(buttonTransRect,(288,335))
                if clicked:
                    optionss = True #displays the options/instructions 
                    
            if pauseCreditsRect.collidepoint(mx,my):
                screen.blit(buttonTransRect,(288,415))
                if clicked:
                    creditsss = True #displays the credits
            if pauseQuitRect.collidepoint(mx,my):
                screen.blit(buttonTransRect,(288,495))
                if clicked:
                    running = False #kills the program
                    
            if optionss:
                screen.blit(optionsPic,(0,0))
                if storeMenuRect.collidepoint(mx,my):
                    screen.blit(menuTransRect,(10,12))
                    if clicked:
                        optionss = False
            if creditsss:
                screen.blit(creditsPic,(0,0))
                if storeMenuRect.collidepoint(mx,my):
                    screen.blit(menuTransRect,(10,12))
                    if clicked:
                        creditsss = False
                #==============================================================#
                #=========================Setting Gun==========================#
            if store:
                screen.blit(storePic,(0,0))
                storeScoreTxt = scoreFont.render(str(score), 1, (0,0,0))
                screen.blit(storeScoreTxt, (615,50))


                #----------------------------------------------------------------#
                #allows you to purchase guns you have not already purchased and adds them to
                #your available guns and subtracts from your money 
                
                if gun1Rect.collidepoint(mx,my):
                    screen.blit(itemsTransRect,(gun1Rect[0],gun1Rect[1]))
                    if clicked and not gun1Bought and cash >= gun1[1]:
                        gun1Bought = True
                        cash -= gun1[1]
                        availableGuns.append(gun1)
                        store = False
                        

                if gun2Rect.collidepoint(mx,my):
                    screen.blit(itemsTransRect,(gun2Rect[0],gun2Rect[1]))
                    if clicked and not gun2Bought and cash >= gun2[1]:
                        gun2Bought = True
                        cash -= gun2[1]
                        availableGuns.append(gun2)
                        store = False
                        
                if gun3Rect.collidepoint(mx,my):
                    screen.blit(itemsTransRect,(gun3Rect[0],gun3Rect[1]))
                    if clicked and not gun3Bought and cash >= gun3[1]:
                        gun3Bought = True
                        cash -= gun3[1]
                        availableGuns.append(gun3)
                        store = False
                        
                if gun4Rect.collidepoint(mx,my):
                    screen.blit(itemsTransRect,(gun4Rect[0],gun4Rect[1]))
                    if clicked and not gun4Bought and cash >= gun4[1]:
                        gun4Bought = True
                        cash -= gun4[1]
                        availableGuns.append(gun4)
                        store = False
                    
                if gun5Rect.collidepoint(mx,my):
                    screen.blit(itemsTransRect,(gun5Rect[0],gun5Rect[1]))
                    if clicked and not gun5Bought and cash >= gun5[1]:
                        gun5Bought = True
                        cash -= gun5[1]
                        availableGuns.append(gun5)
                        store = False
                    
                if gun6Rect.collidepoint(mx,my):
                    screen.blit(itemsTransRect,(gun6Rect[0],gun6Rect[1]))
                    if clicked and not gun6Bought and cash >= gun6[1]:
                        gun6Bought = True
                        cash -= gun6[1]
                        availableGuns.append(gun6)
                        store = False
                    
                if gun7Rect.collidepoint(mx,my):
                    screen.blit(itemsTransRect,(gun7Rect[0],gun7Rect[1]))
                    if clicked and not gun7Bought and cash >= gun7[1]:
                        gun7Bought = True
                        cash -= gun7[1]
                        availableGuns.append(gun7)
                        store = False
                    
                if gun8Rect.collidepoint(mx,my):
                    screen.blit(itemsTransRect,(gun8Rect[0],gun8Rect[1]))
                    if clicked and not gun8Bought and cash >= gun8[1]:
                        gun8Bought = True
                        cash -= gun8[1]
                        availableGuns.append(gun8)
                        store = False
                #allows you to purchase on grenade at a time
                if grenadeRect.collidepoint(mx,my):
                    screen.blit(itemsTransRect,(grenadeRect[0],grenadeRect[1]))
                    if clicked and cash >= 2000:
                        grenadeAmt +=1
                        cash -= 2000
                #allows you to purchase a nuke                        
                if perk1Rect.collidepoint(mx,my):
                    screen.blit(itemsTransRect,(perk1Rect[0],perk1Rect[1]))
                    if clicked and cash >= 100000:
                        nukeAmt += 1
                        cash -= 100000
                    
                #allows you to purchase a life                                        
                if perk4Rect.collidepoint(mx,my):
                    screen.blit(itemsTransRect,(perk4Rect[0],perk4Rect[1]))
                    if clicked and cash >= 100000:
                        player.health += 1
                        cash -= 100000

                #exits the store 
                if storeMenuRect.collidepoint(mx,my):
                    screen.blit(menuTransRect,(10,12))
                    if clicked:
                        store = False
            display.flip()
print(score)

quit()
