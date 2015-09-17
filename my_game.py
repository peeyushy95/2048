import random,pygame, sys
import consoleGame
import time
from pygame.locals import *

pygame.init()

FPS = 30
SLIDINGSPEED = 8

icons = [2,4,8,16,32,64,128,256,512,1024,2048,4096,8192]

WINDOWWIDTH = 900
WINDOWHEIGHT = 600
BOARDWIDTH = 4
BOARDHEIGHT = 4
BOXSIZE = 100
GAPSIZE = 5

XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (160, 160, 160)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
CYAN = (0, 255, 255)
NAVYBLUE = (60, 60, 100)
GREEN = (0, 255, 0)
ORANGE = (255, 128, 0)
PURPLE = (255, 0, 255)

BOXCOLOR = BLACK
BGCOLOR = GREEN

DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH , WINDOWHEIGHT))

pygame.display.set_caption('2048')

def leftTopCoordsOfBox(boxx, boxy):
    # Convert board coordinates to pixel coordinates
    left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN
    top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN
    return (left, top)

def drawBasicBoard():
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))

def getBoard():
    
    board = []

    foo = [1,2,3,4]
    
    x1 = (random.choice(foo))
    y1 = (random.choice(foo))
    x2 = (random.choice(foo))
    y2 = (random.choice(foo))

    idx = [0,1]
    
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            if (x1 == x+1 and y1 == y+1) or (x2 == x+1 and y2 == y+1):
                index = (random.choice(idx))
                column.append(icons[index])
            else:
                column.append(0)
        board.append(column)
    return board

def plotNumber( val ,left ,top ):
    if len(val) == 1:
        newleft = left + 40
    elif len(val) == 2:
        newleft = left + 30
    elif len(val) == 3:
        newleft = left + 24
    elif len(val) == 4:
        newleft = left + 14
    newtop = top + 32
    myfont = pygame.font.SysFont("monospace", 30 , bold = True)
    label = myfont.render(val, 1, YELLOW )
    DISPLAYSURF.blit(label, (newleft, newtop))

def drawMainBoard( Board ):
      for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
             if( Board[x][y] != 0 ):
                 left, top = leftTopCoordsOfBox(x, y)
                 val = Board[x][y]
                 val = str(val)
                 plotNumber( val ,left ,top )

MainBoard = getBoard()

#pygame.mixer.music.load('Pata_Chalgea_Imran_Khan[www.ogg')
#pygame.mixer.music.play(-1, 46.0)

GameOn = True

while GameOn: # main game loop
    
    DISPLAYSURF.fill(BGCOLOR)
    
    drawBasicBoard()

    boardNow = consoleGame.getBoard()

    drawMainBoard( boardNow )

    SCORE = consoleGame.SCORE

    with open('bestScore.txt') as f:
        BESTSCORE = f.readline()
        BESTSCORE = int( BESTSCORE )

    if SCORE > BESTSCORE:
        BESTSCORE = SCORE
        BESTSCORE = str(BESTSCORE)
        f = open('bestScore.txt','w')
        f.write(BESTSCORE)
        f.close()
    
    SCORE = str(SCORE)
    myfont = pygame.font.SysFont("monospace", 20 , bold = True)
    label = myfont.render("SCORE:" + SCORE, 1, NAVYBLUE )

    left = 0 * (BOXSIZE + GAPSIZE) + XMARGIN
    top = 35
                    
    DISPLAYSURF.blit(label, (left, top ))

    BESTSCORE = str(BESTSCORE)
    myfont = pygame.font.SysFont("monospace", 20 , bold = True)
    label = myfont.render("BESTSCORE:" + BESTSCORE, 1, NAVYBLUE )

    left = 2 * (BOXSIZE + GAPSIZE) + XMARGIN
    top = 35
                    
    DISPLAYSURF.blit(label, (left, top ))

    
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                result = consoleGame.action(8)
            if event.key == pygame.K_RIGHT:
                result = consoleGame.action(2)
            if event.key == pygame.K_UP:
                result = consoleGame.action(4)
            if event.key == pygame.K_DOWN:
                result = consoleGame.action(6)
            if result == 0:
                
                drawBasicBoard()

                boardNow = consoleGame.getBoard()

                drawMainBoard( boardNow )

                myfont = pygame.font.SysFont("monospace", 70 , bold = True)
                label = myfont.render("Game Over!", 1, RED )

                left = 0 * (BOXSIZE + GAPSIZE) + XMARGIN
                top = 1.5 * (BOXSIZE + GAPSIZE) + YMARGIN
                
                DISPLAYSURF.blit(label, (left + 5, top + 15))

                soundObj = pygame.mixer.Sound('supermario_ho4nQ7bW_mp3cut.ogg')
                soundObj.play()
                time.sleep(2)
                soundObj.stop()
                
                GameOn = False
                
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
