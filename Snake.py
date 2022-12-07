# Wormy (a Nibbles clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

# Sameek Sharma - SS
# Abbygail Willett - AW
# Melanie Bouzanne- MB

import random, pygame, sys
from pygame.locals import * #imports pygame and all of the neccessary functions that are neccessary to run the game - SS

FPS = 15 #sets game speed - SS
WINDOWWIDTH = 640 #game window width (x-direction) -SS
WINDOWHEIGHT = 480 #game window height (y-direction) -SS
CELLSIZE = 20 #size value for individual square -SS
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size." #ensures correct aspect ratio for window width -SS
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size." #ensures correct aspect ratio for window height -SS
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE) #finds int value of squares in horizontal -SS
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE) #finds int value of squares in vertical -SS

#             R    G    B
WHITE     = (255, 255, 255) #RGB value of white -AW
BLACK     = (  0,   0,   0) #RGB value of black - AW
RED       = (255,   0,   0) #RGB value of red - AW
GREEN     = (  0, 255,   0) #RBG value of green (lighter shade) - AW
DARKGREEN = (  0, 155,   0) #RGB value of green (darker shade - AW
DARKGRAY  = ( 40,  40,  40) #RGB value of grey (lighter black) - AW
BGCOLOR = BLACK #game background is black - AW

UP = 'up' # assigns variable UP to str 'up' - MB
DOWN = 'down' # assigns variable DOWN to str 'down' -MB
LEFT = 'left' # assigns variable LEFT to str 'left' -MB
RIGHT = 'right' # assigns variable RIGHT to str 'right' -MB

HEAD = 0 # sets variable HEAD to value 0 to make code easier to read when indexing the worm's head -MB

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT #sets global variables to be used in this function and other functions -MB

    pygame.init() # initialize all pygame functions -> needs to be run before using pygame -MB
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT)) #displays the game window with the specified dimensions -MB
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18) # defines style and size of font for title -MB
    pygame.display.set_caption('Wormy')

    
    showStartScreen() # calls function showStartScreen() (defined below) to run once before starting the game -SS
    while True:
        runGame() # main game function (defined below) -SS
        showGameOverScreen() #once rungame() returns (by player colliding into wall or self) the showGameOverScreen() (defined below) will run -SS
#above function ->  Opens the game and shows the window over the current on (sets priority), sets a clock animation for start screen, display surface (new window), fonts (to display wording and numbers), and sets window caption (name of the open window running on the computer) -AW


def runGame():
    # Set a random start point.
    startx = random.randint(5, CELLWIDTH - 6) # variable startx chooses a random value for the x coordinate (CELLWIDTH - 6 makes sure the starting x coordinate is not to close to the edge of the board) -AW 
    starty = random.randint(5, CELLHEIGHT - 6) # variable starty chooses a random value for the y coordinate (CELLHEIGHT - 6 makes sure the starting y coordinate is not to close to the edge of the board) -AW 
    
    wormCoords = [{'x': startx,     'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}]
    # the variable wormCoords stores the cordinates of the body of the worm in a list of dictionary values, the XY coordinates have keys 'x' & 'y' -AW
    direction = RIGHT
    # the worm starts with an inital direction right, with a head (at coordinates 'x' and 'y') and two more body segments -AW

    apple = getRandomLocation()  # calls function getRandomLocation (defined below) to start the apple in a random place -AW

    while True: # main game loop -SS
        for event in pygame.event.get(): # event handling loop -SS
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN: 
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    direction = LEFT #when left button is pressed, move left -SS
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                    direction = RIGHT #when right button is pressed, move right -SS
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    direction = UP #when up button is pressed, move up -SS
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                    direction = DOWN #when down button is pressed, move down -SS
                elif event.key == K_ESCAPE:
                    terminate() #when escape is pressed, terminate -SS
                #purpose of previous 5 statements -> assign keybinds for the game -SS
      
        # checks if worm has hit edge -MB
        if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['x'] == CELLWIDTH or wormCoords[HEAD]['y'] == -1 or wormCoords[HEAD]['y'] == CELLHEIGHT:
            return # game over -MB
        # checks if the x or y coordinates of the head is past the left or top edge (if wormCoords[HEAD] 'x' or 'y' = -1) or if the  x or y coordinates of the head are past the right or bottom edge (when wormCoords[HEAD] 'x' or 'y' = the CELLWIDTH or CELLHEIGHT) -MB
        
        
        # check if the worm has hit itself -MB
        for wormBody in wormCoords[1:]:
            if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
                return # game over-MB
        # runs a loop to check each index in wormCoord, which store the body segments (execpt for the head at index [0]) to see if the x and y coordinates of the head ever equal the x and y coordinates of the body -MB

        
        if wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y']: # check if both the x and y coordinates of the worm = the same x and y coordinates of the apple -MB
            apple = getRandomLocation() # set a new apple somewhere -MB
        else:
            del wormCoords[-1] # if the head doesn't collied with an apple then the last segment of the worm (index [-1]) gets removed -MB

       
        if direction == UP:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] - 1}
        elif direction == DOWN:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] + 1}
        elif direction == LEFT:
            newHead = {'x': wormCoords[HEAD]['x'] - 1, 'y': wormCoords[HEAD]['y']}
        elif direction == RIGHT:
            newHead = {'x': wormCoords[HEAD]['x'] + 1, 'y': wormCoords[HEAD]['y']}
        # move the worm by adding a segment in the direction it is moving -MB
        # the new body segment is being added to the beginning of the list therfore the coordinates of the new head is + or - 1 of the x or y coordinate depending on the choosen direction -MB 
           
        wormCoords.insert(0, newHead) # the insert function* changes wormCoord by adding the value of newHead coordinates in index[0], therfore replacing the old head coordinates -AW
        DISPLAYSURF.fill(BGCOLOR) # calls function DISPLAYSURF (defined above) fills entire display surface with the background color (defined above) -AW
        drawGrid() # calls function drawGrid (defined below) -AW
        drawWorm(wormCoords) # calls function drawWorm (defined below) using the wormCoords variable -AW
        drawApple(apple) # calls function drawApple (defied below) using the apple variable -AW
        drawScore(len(wormCoords) - 3) # calls function drawScore using the len function to determine the lenght of variable wormCoords (which stores the body), then subtacks the starting body (lenght 3) to determine score -AW 
        pygame.display.update() 
        FPSCLOCK.tick(FPS)

def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play.', True, DARKGRAY) # renders text, TRUE means the characters will have smooth edges, color of text (DARKGRAY) -SS
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30) # postion of text on display -SS
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)
#above function -> displays a message ('Press a key to play') at the bottom right corner of the screen, prompting the viewer to enter a key to start the game -SS

def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key
#above function -> checks for a key press any key results in returning the function except ESCAPE terminates the game: quit the game when the quit button is pressed -AW

def showStartScreen():
    titleFont = pygame.font.Font('freesansbold.ttf', 100) # defines style and size of font for title -MB
    titleSurf1 = titleFont.render('Wormy!', True, WHITE, DARKGREEN) # renders text, TRUE means the characters will have smooth edges, color of text (WHITE), color of text background(DARKGREEN) -MB
    titleSurf2 = titleFont.render('Wormy!', True, GREEN) # renders text, TRUE means the characters will have smooth edges, color of text(GREEN) -MB
   

    degrees1 = 0
    degrees2 = 0
    while True:
        DISPLAYSURF.fill(BGCOLOR) #fills the display surface with a color -MB
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2) # postion of text on display -MB
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2) # postion of text on display -MB
        DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)
# while True -> it rotates the two text "Wormy!' -MB
        
        drawPressKeyMsg() #calls function drawPressKeyMsg() (defined below to display a message) -MB

        if checkForKeyPress(): # calls function checkForKeyPress() (defined below) -MB
            pygame.event.get() # clear event queue -MB
            return
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        degrees1 += 3 # rotate by 3 degrees each frame -MB
        degrees2 += 7 # rotate by 7 degrees each frame -MB
#All colours mentiond were defined earlier-MB

        

def terminate():
    pygame.quit()
    sys.exit()
#above function -> terminates the game and window when the user inputs that the game should be closed -SS

def getRandomLocation():
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}
#above function -> returns a dictionary with keys 'x' and 'y' that have random vaule within the defined areas CEllHEIGHT and CELLWIDTH -SS
#                  above function is called when new random coordinates for an apple are needed -SS

def showGameOverScreen():
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150) # defines style and size of font for title -AW
    gameSurf = gameOverFont.render('Game', True, WHITE) # renders text, TRUE means the characters will have smooth edges, color of text(WHITE) -AW
    overSurf = gameOverFont.render('Over', True, WHITE) # renders text, TRUE means the characters will have smooth edges, color of text(WHITE) -AW
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, 10) # postion of text on display -AW
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25) # postion of text on display -AW
    
    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress() # clear out any key presses in the event queue -AW

    while True:
        if checkForKeyPress():
            pygame.event.get() # clear event queue -AW
            return
#above function -> sets the <game over> visual with colour, size and position, clears key press que, and waits for a new key input (to restart game) -AW
        
def drawScore(score):
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, WHITE) # renders text, TRUE means the characters will have smooth edges, color of text (WHITE) -SS
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 120, 10) # postion of text on display -SS
    DISPLAYSURF.blit(scoreSurf, scoreRect)
#above function -> sets scoreboard visual with colour, size, and position -SS

def drawWorm(wormCoords):
    for coord in wormCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE) # pygame.Rect -> is an object for storing rectangular coordinates [.Rect(left, top, width, height)] -MB
        # wormSegmentRect use pygame.Rect to define a rectangle (left and top coordinates defined by x and y then height and width determine by CELLSIZE) -MB
            
        pygame.draw.rect(DISPLAYSURF, DARKGREEN, wormSegmentRect) # pygame.draw.rect -> draws a rectangle parameters: surface = DISPLAYSURF, color = DARKGREEN, rect = wormSegmentRect -MB
      
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
         # wormInnerSegmentRect use pygame.Rect to define a rectangle (left and top coordinates defined by x and y (+4 starts 4 pixels to right and below) then height and width determine by CELLSIZE (-8 height and width are 8 pixels less then the cellsize)) -MB
            
        pygame.draw.rect(DISPLAYSURF, GREEN, wormInnerSegmentRect) # pygame.draw.rect -> draws a rectangle, parameters: surface = DISPLAYSURF, color = GREEN, rect = wormInnerSegmentRect -MB

# above function -> runs a loop to draw a each segment of the worms body for each dictionary values in wormCoords;   each segment of the worms body is displayed as a green box -MB


def drawApple(coord):
    x = coord['x'] * CELLSIZE 
    y = coord['y'] * CELLSIZE
    appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE) # pygame.Rect -> is an object for storing rectangular coordinates [.Rect(left, top, width, height)] -AW
    # appleRect use pygame.Rect to define a rectangle (left and top coordinates defined by x and y then height and width determine by CELLSIZE) -AW
    
    pygame.draw.rect(DISPLAYSURF, RED, appleRect)  # pygame.draw.rect -> draws a rectangle, parameters: surface = DISPLAYSURF, color = RED, rect = appleRect -AW
# above function -> draws a red rectangle, using coordinates values stored in the dictionary keys 'x' and 'y' then scaled by CELLSIZE -AW


def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines -SS
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT)) # pygame.draw.line -> drawa a stright line, parameters: surface = DISPLAYSURF, color = DARKGRAY, start position (x, 0), end position (x, WINDOWHEIGHT) -SS
    for y in range(0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines -SS
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y)) # pygame.draw.line -> drawa a stright line, parameters: surface = DISPLAYSURF, color = DARKGRAY, start position (0, y), end position (WINDOWWIDTH, y) -SS
# above function -> draws the grid using a for loop to run through the range of x and y -SS


if __name__ == '__main__':
    main()
# main() function called to run the program -AW
