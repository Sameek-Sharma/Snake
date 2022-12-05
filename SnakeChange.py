# Wormy (a Nibbles clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

# Sameek Sharma - SS
# Abbygail Willett - AW
# Melanie Bouzanne- MB

import random, pygame, sys
from pygame.locals import * 

FPS = 8 #changed
WINDOWWIDTH = 1400 # CHANGED FROM 640 to 
WINDOWHEIGHT = 800 # CHANGED FROM 480 TO 1080
CELLSIZE = 20 
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size." 
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size." 
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE) 
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE) 

#             R    G    B
WHITE     = (255, 255, 255) 
BLACK     = (  0,   0,   0) 
RED       = (128,   0,   0) #added
LIGHTRED  = (255,   0,   0) #changed
GREEN     = (  0, 255,   0) 
YELLOW    = ( 255, 255, 0) #CHANGED
DARKYELLOW = (  155, 155, 0) #CHANGED
DARKGRAY  = ( 40,  40,  40) 
BGCOLOR = BLACK 

UP = 'up' 
DOWN = 'down' 
LEFT = 'left' 
RIGHT = 'right' 

HEAD = 0 

def choose_diff_screen():
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
    gameSurf = gameOverFont.render('Choose Difficulty', True, WHITE)
    overSurf = gameOverFont.render('E > Easy  H > Hard', True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, 10)
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25)

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT)) 
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Going Bananas')
    
        
    a = input("Easy (E) or Hard (H)? ")

    if type(a) == str:
        if a == "E":
            showStartScreenEasy()
            while True:
                runGame()
                showGameOverScreen()
        if a == "H":
            global FPS
            FPS = 20
            showStartScreenHard()
            while True:
                runGame()
                showGameOverScreen()
            
def runGame():

    startx = random.randint(5, CELLWIDTH - 6)
    starty = random.randint(5, CELLHEIGHT - 6)
    wormCoords = [{'x': startx,     'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}]
    direction = RIGHT

    
    apple = getRandomLocationApple()
    pear = getRandomLocationPear()
    

    while True: 
        for event in pygame.event.get(): 
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN: 
                if (event.key == K_LEFT or event.key == K_a) and direction != LEFT:
                    direction = RIGHT 
                elif (event.key == K_RIGHT or event.key == K_d) and direction != RIGHT:
                    direction = LEFT 
                elif (event.key == K_UP or event.key == K_w) and direction != UP:
                    direction = DOWN 
                elif (event.key == K_DOWN or event.key == K_s) and direction != DOWN:
                    direction = UP
        # reversed left and right and up and down
                elif event.key == K_ESCAPE:
                    terminate()
                
        
        if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['x'] == CELLWIDTH or wormCoords[HEAD]['y'] == -1 or wormCoords[HEAD]['y'] == CELLHEIGHT:
            return 
        for wormBody in wormCoords[1:]:
            if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
                return 

     
        
        
        if wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y']:
            
            apple = getRandomLocationApple()
            
            
        elif wormCoords[HEAD]['x'] == pear['x'] and wormCoords[HEAD]['y'] == pear['y']:          
                
            p = random.choice(['a','b'])
            
            if p == 'a':
                if direction == UP:
                    newTail = {'x': wormCoords[-1]['x'], 'y': wormCoords[-1]['y'] - 1}
                elif direction == DOWN:
                    newTail = {'x': wormCoords[-1]['x'], 'y': wormCoords[-1]['y'] + 1}
                elif direction == LEFT:
                    newTail = {'x': wormCoords[-1]['x'] - 1, 'y': wormCoords[-1]['y']}
                elif direction == RIGHT:
                    newTail = {'x': wormCoords[-1]['x'] + 1, 'y': wormCoords[-1]['y']}
                wormCoords.append(newTail)

                pear = getRandomLocationPear()   
                #return
                
            if p == 'b':
                return
            
        #Changes
        else:
            del wormCoords[-1] 

      
        if direction == UP:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] - 1}
        elif direction == DOWN:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] + 1}
        elif direction == LEFT:
            newHead = {'x': wormCoords[HEAD]['x'] - 1, 'y': wormCoords[HEAD]['y']}
        elif direction == RIGHT:
            newHead = {'x': wormCoords[HEAD]['x'] + 1, 'y': wormCoords[HEAD]['y']}
            
            
        wormCoords.insert(0, newHead)
        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()
        drawWorm(wormCoords)
        drawApple(apple)
        drawPear(pear)
        drawScore(len(wormCoords) - 3)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play.', True, WHITE)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)


def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key
 

def showStartScreenEasy():
    titleFont = pygame.font.Font('freesansbold.ttf', 100)
    titleSurf1 = titleFont.render('GOING', True, WHITE, DARKYELLOW)
    titleSurf2 = titleFont.render('BANANAS!', True, YELLOW)

    
    degrees1 = 0
    degrees2 = 0
    while True:
        DISPLAYSURF.fill(BGCOLOR)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)

        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get() 
            return
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        degrees1 += 3
        degrees2 += 7 
        
def showStartScreenHard():
    titleFont = pygame.font.Font('freesansbold.ttf', 100)
    titleSurf1 = titleFont.render('GOING', True, WHITE, LIGHTRED)
    titleSurf2 = titleFont.render('BANANAS!', True, RED)

    
    degrees1 = 0
    degrees2 = 0
    while True:
        DISPLAYSURF.fill(BGCOLOR)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)

        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get() 
            return
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        degrees1 += 20
        degrees2 += 40 


def terminate():
    pygame.quit()
    sys.exit()

    

def getRandomLocationApple():
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}

def getRandomLocationPear():
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}



    
    

def showGameOverScreen():
    gameOverFont = pygame.font.Font('freesansbold.ttf', 90)
    gameSurf = gameOverFont.render('YOU LOST!', True, WHITE)
    overSurf = gameOverFont.render('Press Space', True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, 10)
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 15 + 25)

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress() 

    while True:
        if checkForKeyPress():
            pygame.event.get() 
            return

        
def drawScore(score):
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 120, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)


def drawWorm(wormCoords):
    for coord in wormCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, DARKYELLOW, wormSegmentRect) #CHANGED
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, YELLOW, wormInnerSegmentRect) #CHANGED


def drawApple(coord_apple):
    x = coord_apple['x'] * CELLSIZE
    y = coord_apple['y'] * CELLSIZE
    appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, LIGHTRED, appleRect)
    
#CHANGED   
def drawPear(coord_pear):
    x = coord_pear['x'] * CELLSIZE
    y = coord_pear['y'] * CELLSIZE
    pearRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, GREEN, pearRect) 
    


def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))


if __name__ == '__main__':
    main()
