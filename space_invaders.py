import random

import pygame

from pygame import mixer

pygame.init()
# screen
screen = pygame.display.set_mode((800, 600))

# title and icon image
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# background
background = pygame.image.load('bg.png')

#background_music
mixer.music.load("background.wav")
mixer.music.play(-1)

# player
playerImg = pygame.image.load("spaceship.png")
playerX = 370
playerY = 480
PlayerxChange = 0

# enemy

EnemyImg = []
enemyX = []
enemyY = []
enemyXChange = []
enemyYChange = []
num_of_enemies = 6
for i in range(num_of_enemies):
    EnemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyXChange.append(0.3)
    enemyYChange.append(40)

# bullet

# ready-you cant see the bullet
# fire -the bullet has been shot
bulletImg = pygame.image.load("bullets.png")
bulletX = 0
bulletY = 480
bulletXChange = 0
bulletYChange = 1
bulletState = "ready"

# Score
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
textX = 10
textY = 10

#game over text
over_font = pygame.font.Font("freesansbold.ttf", 72)

def show_score(x,y):
    score=font.render("Score is: "+ str(score_value), True,(255,255,255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER" , True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def player(x, y):
    screen.blit(playerImg, (x, y))


def Enemy(x, y, i):
    screen.blit(EnemyImg[i], (x, y))


def fire_bullet(x, y):
    global bulletState
    bulletState = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = ((enemyX - bulletX) ** 2 + (enemyY - bulletY) ** 2) ** 0.5
    if distance <= 27:
        return True
    else:
        return False


# game loop
running = True

while running:

    # screen RGB

    screen.fill((255, 255, 255))


    # background
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if keystroke is pressed whatever right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                PlayerxChange = -0.5

            if event.key == pygame.K_RIGHT:
                PlayerxChange = 0.5

            if event.key == pygame.K_SPACE:
                if bulletState == "ready":

                    bullet_sound=mixer.Sound("laser.wav")
                    bullet_sound.play()

                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                PlayerxChange = 0

    playerX += PlayerxChange

    if playerX <= 0:
        playerX = 790
    elif playerX >= 790:
        playerX = 0

    for i in range(num_of_enemies):

        #game_over

        if enemyY[i]>440:
            for j in range(num_of_enemies):
                enemyY[j]=2000
            game_over_text()
            break



        enemyX[i] += enemyXChange[i]

        if enemyX[i] <= 0:
            enemyXChange[i] = 0.3
            enemyY[i] += enemyYChange[i]

        elif enemyX[i] >= 736:
            enemyXChange[i] = -0.3
            enemyY[i] += enemyYChange[i]

        # collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:

            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()

            bulletY = 480
            bulletState = "ready"
            score_value += 1

            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)


        Enemy(enemyX[i], enemyY[i], i)

    if bulletY <= 0:
        bulletY = 480
        bulletState = "ready"

    if bulletState == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletYChange

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
