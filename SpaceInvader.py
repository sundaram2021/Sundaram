import pygame
import math
import random
from pygame import mixer
#initialize_pygame_in_it
pygame.init()




#create the screen 
screen = pygame.display.set_mode((800,600))   


#adding background image
background = pygame.image.load("background.png")


#background sound
mixer.music.load("background.wav")
mixer.music.play(-1)

#title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("UFO.png")
pygame.display.set_icon(icon)


#Player
player_img = pygame.image.load("Spaceship.png") 
playerX = 370
playerY = 480
playerX_change = 0

#enemy
enemy_img = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
no_of_enemy = 6


for i in range(no_of_enemy):
    enemy_img.append(pygame.image.load("Enemy.png")) 
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(4)
    enemyY_change.append(15)

#bullet
#ready-means bullet will not be seen in screen
#fire-means bullet will be fired in the y direction
bullet_img = pygame.image.load("bullet.png") 
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

#Score
scores = 0
font = pygame.font.Font("freesansbold.ttf",32)
textX = 10
textY = 10

#game over font
over_font = pygame.font.Font("freesansbold.ttf",64)


def text_screen(x,y):
    score = font.render("Score : " + str(scores),True,(255,255,255))
    screen.blit(score,(x,y))


def game_over_text():
    over_text = over_font.render("GAME OVER",True,(255,255,255))
    screen.blit(over_text,(200,250))

def player(x,y):
    screen.blit(player_img,(x,y))

def enemy(x,y,i):
    screen.blit(enemy_img[i],(x,y))


def bullet_fire(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img,(x+16,y+10))


def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX,2)) + (math.pow(enemyY-bulletY,2)))
    if distance < 27:
        return True
    else: return False     

#game loop
running = True
while running :
    #RGB-red,green,blue ----max_value--255
    screen.fill((0,0,0))
    #background image
    screen.blit(background,(0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        #control by keyboard
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5    
            
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    bullet_fire(bulletX,bulletY)


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    if playerX >= 736:
        playerX = 736 
    
    for i in range(no_of_enemy):

        #game over
        if enemyY[i] > 440:
            for j in range(no_of_enemy):
                enemyY[j] = 2000
            game_over_text()
            break    


        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        
        #Collision
        collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            scores += 1
            print(scores)
            enemyX[i] = random.randint(0,735)
            enemyY[i] = random.randint(50,150)
        enemy(enemyX[i],enemyY[i],i)

    #bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"



    if bullet_state == "fire":
        bullet_fire(bulletX,bulletY)
        bulletY -= bulletY_change

    player(playerX,playerY)
    text_screen(textX,textY)
    pygame.display.update()