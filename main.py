import pygame
import random
import math
from pygame import mixer


# Initialize the pygame module
pygame.init()

# Create screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load("./imgs/Background/spaceBG1.jpg")

# Background Music
mixer.music.load("./imgs/Sounds/BGM8.wav")
mixer.music.play(-1)  # -1 for play in loop music

# Title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("./imgs/game-controller(1).png")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load("./imgs/spaceship(2).png")
playerX = 375
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyXChange = []
enemyYChange = []
numOfEnemies = 6
for num in range(numOfEnemies):
    enemyImg.append(pygame.image.load("./imgs/ufo.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(20, 100))
    enemyXChange.append(3.2)
    enemyYChange.append(40)

# Bullet
bulletImg = pygame.image.load("./imgs/bullet.png")
bullet_x = 0
bullet_y = 480
bullet_xChange = 0
bullet_yChange = 10
bulletState = "ready"  # Ready = can't see bullet / Fire = bullet is shoot

# Score
scoreValue = 0
fontText = pygame.font.Font("./imgs/Fonts/BalsamiqSans-Bold.ttf", 32)

textX = 10
textY = 10

# Game Over
gameOverText = pygame.font.Font("./imgs/Fonts/BalsamiqSans-Bold.ttf", 64)

def gameOver():
    overText = gameOverText.render("GAME OVER", True, (255, 255, 255))
    screen.blit(overText, (230, 250))

def showScore(x, y):
    score = fontText.render("Score: " + str(scoreValue), True, (255, 255, 255))
    screen.blit(score, (x, y))

def player(x, y):
    screen.blit(playerImg, (x, y))  # Drawing player


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def reallocateEnemy(enemyX, enemyY):
    enemyX = random.randint(0, 735)
    enemyY = random.randint(20, 100)
    return enemyX, enemyY


def fire_bullet(x, y):
    global bulletState
    bulletState = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 27:
        return True
    else:
        return False


# Game loop
running = True
while running:
    # Change the RGB color bg
    screen.fill((0, 255, 255))
    # Background image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Check for keyboard arrows left or right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change -= 4
            if event.key == pygame.K_RIGHT:
                playerX_change += 4
            if event.key == pygame.K_SPACE:
                if bulletState is "ready":
                    bulletSound = mixer.Sound("./imgs/Sounds/LaserSound.wav")
                    bulletSound.play()
                    # Get the current cordenate of the player.
                    bullet_x = playerX
                    fire_bullet(bullet_x, bullet_y)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Check for player doesn't go out of bounds
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy movement
    for i in range(numOfEnemies):

        # Game Over
        if enemyY[i] > 440:
            for j in range(numOfEnemies):
                enemyY[j] = 2000
            gameOver()
            break

        enemyX[i] += enemyXChange[i]
        if enemyX[i] <= 0:
            enemyXChange[i] = 0
            enemyY[i] += enemyYChange[i]
            enemyXChange[i] += 3.2
        elif enemyX[i] >= 736:
            enemyXChange[i] = 0
            enemyY[i] += enemyYChange[i]
            enemyXChange[i] -= 3.2

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bullet_x, bullet_y)
        if collision:
            explodeSound = mixer.Sound("./imgs/Sounds/Explosion2.wav")
            explodeSound.play()
            bullet_y = 480
            bulletState = "ready"
            scoreValue += 1
            print(scoreValue)
            enemyX[i], enemyY[i] = reallocateEnemy(enemyX, enemyY)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bullet_y <= 0:
        bullet_y = 480
        bulletState = "ready"
    if bulletState is "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_yChange

    player(playerX, playerY)
    showScore(textX, textY)
    pygame.display.update()