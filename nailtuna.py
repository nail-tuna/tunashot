import pygame
import sys
import random
from time import sleep

BLACK = (0,0,0)
padWidth = 480
padHeight = 640

faceImage = ['game-resource/detua.png','game-resource/hong.png','game-resource/wakeup.png','game-resource/tiffany.png']
explosionSound = ['game-resource/chanho.wav','game-resource/detua.wav','game-resource/tiffany.wav']


def drawObject(obj,x,y):
    global gamePad
    gamePad.blit(obj,(x,y))

def initGame():
    global gamePad, clock, background, tuna, nail, explosion, nailSound, gameOverSound
    pygame.init()
    gamePad = pygame.display.set_mode((padWidth,padHeight))
    pygame.display.set_caption("Nail Tuna")
    background = pygame.image.load("game-resource/background.png")
    tuna = pygame.image.load('game-resource/tuna.png')
    nail = pygame.image.load('game-resource/nail.png')
    explosion = pygame.image.load('game-resource/explosion.png')

    pygame.mixer.music.load('game-resource/background.wav')
    pygame.mixer.music.play(-1)
    nailSound = pygame.mixer.Sound('game-resource/missile.wav')
    gameOverSound = pygame.mixer.Sound('game-resource/gameover.wav')



    clock = pygame.time.Clock()


def writeScore(count):
    global gamePad
    font = pygame.font.Font('game-resource/NanumGothic-Regular.ttf',15)
    text = font.render('Destroyed faces:' + str(count), True, (255,255,255))
    gamePad.blit(text,(10,0))

def writePassed(count):
    global gamePad
    font = pygame.font.Font('game-resource/NanumGothic-Regular.ttf',15)
    text = font.render('Loss faces:' + str(count), True, (255,0,0))
    gamePad.blit(text,(360,0))

def writeMessage(text):
    global gamePad, gameOverSound
    textfont = pygame.font.Font('game-resource/NanumGothic-Regular.ttf',80)
    text = textfont.render(text,True,(255,0,0))
    textpos = text.get_rect()
    textpos.center = (padWidth/2, padHeight/2)

    gamePad.blit(text,textpos)
    pygame.display.update()
    pygame.mixer_music.stop()
    gameOverSound.play()

    sleep(2)

    pygame.mixer_music.play(-1)

    runGame()

def crash():
    global gamePad
    writeMessage("못참치!")

def gameOver():
    global gamePad
    writeMessage("못~~참치!")



def runGame():
    global gamepad, clock, background, tuna, nail, explosion, nailSound




    tunaSize = tuna.get_rect().size
    tunaWidth = tunaSize[0]
    tunaHeight = tunaSize[1]

    nailXY = []

    face = pygame.image.load(random.choice(faceImage))
    faceSize = face.get_rect().size
    faceWidth = faceSize[0]
    faceHeight = faceSize[1]
    destroySound = pygame.mixer.Sound(random.choice(explosionSound))

    faceX = random.randrange(0,padWidth- faceWidth)
    faceY = 0
    faceSpeed = 2

    x = padWidth * 0.45
    y = padHeight * 0.9
    tunaX = 0


    isShot = False
    shotCount = 0
    facePassed = 0

    onGame = False

    while not onGame:
        for event in pygame.event.get():
            if event.type in [pygame.QUIT]:
                pygame.quit()
                sys.exit()

            if event.type in [pygame.KEYDOWN]:
                if event.key == pygame.K_LEFT:
                    tunaX -= 5

                elif event.key == pygame.K_RIGHT:
                    tunaX += 5

                elif event.key == pygame.K_SPACE:
                    nailSound.play()
                    nailX = x + tunaWidth/2
                    nailY = y - tunaHeight
                    nailXY.append([nailX,nailY])

            if event.type in [pygame.KEYUP]:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    tunaX = 0

        drawObject(background,0,0)

        x += tunaX
        if x < 0 :
            x = 0
        elif x > padWidth - tunaWidth:
            x = padWidth - tunaWidth

        if y < faceY + faceHeight:
            if (faceX > x and faceX < x + tunaWidth) or \
                (faceX + faceWidth > x and faceX + faceWidth < x + tunaWidth):
                crash()


        drawObject(tuna,x,y)

        if len(nailXY) != 0:
            for i, bxy in enumerate(nailXY):
                bxy[1] -= 10
                nailXY[i][1] = bxy[1]


            if bxy[1] < faceY:
                if bxy[0] > faceX and bxy[0] < faceX + faceWidth:
                    nailXY.remove(bxy)
                    isShot = True
                    shotCount += 1


            if bxy[1] <= 0:
                try:
                    nailXY.remove(bxy)
                except:
                    pass
        if len(nailXY) != 0:
            for bx, by in nailXY:
                drawObject(nail,bx,by)

        writeScore(shotCount)
        faceY += faceSpeed

        if faceY > padHeight:

            face = pygame.image.load(random.choice(faceImage))
            faceSize = face.get_rect().size
            faceWidth = faceSize[0]
            faceHeight = faceSize[1]

            faceX = random.randrange(0, padWidth - faceWidth)
            faceY = 0
            facePassed += 1

        if facePassed == 3:
            gameOver()

        writePassed(facePassed)

        if isShot:
            drawObject(explosion,faceX,faceY)
            destroySound.play()

            face = pygame.image.load(random.choice(faceImage))
            faceSize = face.get_rect().size
            faceWidth = faceSize[0]
            faceHeight = faceSize[1]

            faceX = random.randrange(0, padWidth - faceWidth)
            faceY = 0
            destroySound = pygame.mixer.Sound(random.choice(explosionSound))
            isShot = False

            faceSpeed += 0.1
            if faceSpeed >= 10:
                faceSpeed = 10


        drawObject(face,faceX,faceY)


        #pygame.display.update()

        #gamePad.fill(BLACK)



        pygame.display.update()

        clock.tick(60)

    pygame.quit()

initGame()
runGame()
