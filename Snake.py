# Wormy (a Nibbles clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

# Sameek Sharma - SS
# Abbygail Willett - AW
# Melanie Bouzanne- MB

import random, pygame, sys
from pygame.locals import * #imports pygame and all of the neccessary functions that are neccessary to run the game

FPS = 15 #sets game speed
WINDOWWIDTH = 640 #game window width (x-direction)
WINDOWHEIGHT = 480 #game window height (y-direction)
CELLSIZE = 20 #size value for individual square
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size." #ensures correct aspect ratio for window
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size." #ensures correct aspect ratio for window
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE) #finds int value of squares in horizontal
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE) #finds int value of squares in vertical

#             R    G    B
WHITE     = (255, 255, 255) #RGB value of white
BLACK     = (  0,   0,   0) #RGB value of black
RED       = (255,   0,   0) #RGB value of red
GREEN     = (  0, 255,   0) #RBG value of green (lighter shade)
DARKGREEN = (  0, 155,   0) #RGB value of green (darker shade
DARKGRAY  = ( 40,  40,  40) #RGB value of grey (lighter black)
BGCOLOR = BLACK #game background is black

UP = 'up' 
DOWN = 'down' 
LEFT = 'left' 
RIGHT = 'right' 

HEAD = 0 # index of the worm's head

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT)) #displays the game window with the specified dimensions
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Wormy')

    showStartScreen()
    while True:
        runGame()
        showGameOverScreen()
#above function ->  Opens the game and shows the window over the current on (sets priority), sets a clock animation for start screen, display surface (new window), fonts (to display wording and numbers), and sets window caption (name of the open window running on the computer)


def runGame():
    # Set a random start point.
    startx = random.randint(5, CELLWIDTH - 6) # variable startx chooses a random value for the x coordinate (CELLWIDTH - 6 makes sure the starting x coordinate is not to close to the edge of the board) -MB 
    starty = random.randint(5, CELLHEIGHT - 6) # variable starty chooses a random value for the y coordinate (CELLHEIGHT - 6 makes sure the starting y coordinate is not to close to the edge of the board) -MB 
    
    # the variable wormCoords stores the cordinates of the body of the worm in a list of dictionary values, the XY coordinates have keys 'x' & 'y' -MB
    wormCoords = [{'x': startx,     'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}]
    direction = RIGHT
    # the worm starts with an inital direction right, with a head (at coordinates 'x' and 'y') and two more body segments -MB

    # Start the apple in a random place.
    apple = getRandomLocation()

    while True: # main game loop
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN: 
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    direction = LEFT #when left button is pressed, move left
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                    direction = RIGHT #when right button is pressed, move left
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    direction = UP #when up button is pressed, move up
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                    direction = DOWN #when down button is pressed, move down
                elif event.key == K_ESCAPE:
                    terminate() #when escape is pressed, terminate
                #purpose of previous 5 statements -> assign keybinds for the game
      
        # checks if worm has hit edge
        # checks if the x or y coordinates of the head is past the left or top edge (if wormCoords[HEAD] 'x' or 'y' = -1) or if the  x or y coordinates of the head are past the right or bottom edge (when wormCoords[HEAD] 'x' or 'y' = the CELLWIDTH or CELLHEIGHT) -MB
        if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['x'] == CELLWIDTH or wormCoords[HEAD]['y'] == -1 or wormCoords[HEAD]['y'] == CELLHEIGHT:
            return # game over
        
        # check if the worm has hit itself
        # runs a loop to check each index in wormCoord, which store the body segments (execpt for the head at index [0]) to see if the x and y coordinates of the head ever equal the x and y coordinates of the body -MB
        for wormBody in wormCoords[1:]:
            if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
                return # game over

        # check if both the x and y coordinates of the worm = the same x and y coordinates of the apple -MB
        if wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y']:
            apple = getRandomLocation() # set a new apple somewhere
        else:
            del wormCoords[-1] # if the head doesn't collied with an apple then the last segment of the worm (index [-1]) gets removed -MB

        # move the worm by adding a segment in the direction it is moving
        # the new body segment is being added to the beginning of the list therfore the coordinates of the new head is + or - 1 of the x or y coordinate depending on the choosen direction -MB
        if direction == UP:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] - 1}
        elif direction == DOWN:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] + 1}
        elif direction == LEFT:
            newHead = {'x': wormCoords[HEAD]['x'] - 1, 'y': wormCoords[HEAD]['y']}
        elif direction == RIGHT:
            newHead = {'x': wormCoords[HEAD]['x'] + 1, 'y': wormCoords[HEAD]['y']}
        wormCoords.insert(0, newHead) # the insert function* changes wormCoord by adding the value of newHead coordinates in index[0], therfore replacing the old head coordinates -MB
        DISPLAYSURF.fill(BGCOLOR) # calls function DISPLAYSURF (defined above) fills entire display surface with the background color (defined above)
        drawGrid() # calls function drawGrid (defined below) -MB
        drawWorm(wormCoords) # calls function drawWorm (defined below) using the wormCoords variable -MB
        drawApple(apple) # calls function drawApple (defied below) using the apple variable -MB
        drawScore(len(wormCoords) - 3) # calls function drawScore using the len function to determine the lenght of variable wormCoords (which stores the body), then subtacks the starting body (lenght 3) to determine score -MB 
        pygame.display.update() 
        FPSCLOCK.tick(FPS)

def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play.', True, DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)
#above function -> design and print of message prompting the viewer to enter a key to start the game

def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key
#above function -> checks for a key press and does what the key requests: quit the game when the quit button is pressed, 

def showStartScreen():
    titleFont = pygame.font.Font('freesansbold.ttf', 100)
    titleSurf1 = titleFont.render('Wormy!', True, WHITE, DARKGREEN)
    titleSurf2 = titleFont.render('Wormy!', True, GREEN)
#above funciton -> Purpose: show start screen (what is displayed when the window is opened?), It will display <Wormy!> in white, darkgreeen, and green (colours defined earlier)
    
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
            pygame.event.get() # clear event queue
            return
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        degrees1 += 3 # rotate by 3 degrees each frame
        degrees2 += 7 # rotate by 7 degrees each frame


def terminate():
    pygame.quit()
    sys.exit()
#above function -> terminates the game and window when the user inputs that the game should be closed

def getRandomLocation():
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}
#above function -> gets a random number that lies on the playing field for different applications

def showGameOverScreen():
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
    gameSurf = gameOverFont.render('Game', True, WHITE)
    overSurf = gameOverFont.render('Over', True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, 10)
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25)

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress() # clear out any key presses in the event queue

    while True:
        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return
#above function -> sets the <game over> visual with colour, size and position, clears key press que, and waits for a new key input (to restart game)
        
def drawScore(score):
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 120, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)
#above function -> sets scoreboard visual with colour, size, and position

def drawWorm(wormCoords):
    for coord in wormCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, DARKGREEN, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, GREEN, wormInnerSegmentRect)


def drawApple(coord):
    x = coord['x'] * CELLSIZE 
    y = coord['y'] * CELLSIZE
    appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, RED, appleRect)


def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))


if __name__ == '__main__':
    main()
