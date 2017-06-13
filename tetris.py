import random, time, pygame, sys
import pickle
from pygame.locals import *
from os import path
# from random import randrange as rand
# import pygame, sys

FPS = 25
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
BOXSIZE = 20
BOARDWIDTH = 10
BOARDHEIGHT = 20
BLANK = '.'
muteFlag = 0

highScoreFile = open("score.txt", "r")
highScore = int(highScoreFile.read())
highScoreFile.close()

MOVESIDEWAYSFREQ = 0.15
MOVEDOWNFREQ = 0.1

XMARGIN = int((WINDOWWIDTH - BOARDWIDTH * BOXSIZE) / 2)
TOPMARGIN = WINDOWHEIGHT - (BOARDHEIGHT * BOXSIZE) - 5

#               R    G    B
WHITE       = (255, 255, 255)
GRAY        = (185, 185, 185)
BLACK       = (  0,   0,   0)
RED         = (155,   0,   0)
LIGHTRED    = (175,  20,  20)
GREEN       = (  0, 155,   0)
LIGHTGREEN  = ( 20, 175,  20)
BLUE        = (  0,   0, 155)
LIGHTBLUE   = ( 20,  20, 175)
YELLOW      = (155, 155,   0)
LIGHTYELLOW = (175, 175,  20)

BORDERCOLOR = WHITE
BGCOLOR = BLACK
TEXTCOLOR = WHITE
TEXTSHADOWCOLOR = GRAY
COLORS      = (     BLUE,      GREEN,      RED,      YELLOW)
LIGHTCOLORS = (LIGHTBLUE, LIGHTGREEN, LIGHTRED, LIGHTYELLOW)
assert len(COLORS) == len(LIGHTCOLORS) # each color must have light color

TEMPLATEWIDTH = 5
TEMPLATEHEIGHT = 5

S_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '..OO.',
                     '.OO..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '...O.',
                     '.....']]

Z_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '.O...',
                     '.....']]

I_SHAPE_TEMPLATE = [['..O..',
                     '..O..',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     'OOOO.',
                     '.....',
                     '.....']]

O_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '.OO..',
                     '.....']]

J_SHAPE_TEMPLATE = [['.....',
                     '.O...',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..OO.',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '...O.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '.OO..',
                     '.....']]

L_SHAPE_TEMPLATE = [['.....',
                     '...O.',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '.O...',
                     '.....'],
                    ['.....',
                     '.OO..',
                     '..O..',
                     '..O..',
                     '.....']]

T_SHAPE_TEMPLATE = [['.....',
                     '..O..',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '..O..',
                     '.....']]

PIECES = {'S': S_SHAPE_TEMPLATE,
          'Z': Z_SHAPE_TEMPLATE,
          'J': J_SHAPE_TEMPLATE,
          'L': L_SHAPE_TEMPLATE,
          'I': I_SHAPE_TEMPLATE,
          'O': O_SHAPE_TEMPLATE,
          'T': T_SHAPE_TEMPLATE}

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, BIGFONT, MIDFONT, BFONT, BGCOLOR, muteFlag, SFONT
    pygame.init()
    pygame.display.set_caption("Tetromino")
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    DISPLAYSURF.fill(BGCOLOR)
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    MIDFONT = pygame.font.Font('freesansbold.ttf', 70)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 100)
    BFONT = pygame.font.Font('freesansbold.ttf', 80)
    SFONT = pygame.font.Font('freesansbold.ttf', 25)
    titleSurf, titleRect = makeTextObjs('Tetetetris', BFONT, TEXTCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2)-3, int(WINDOWHEIGHT / 2)-50)
    DISPLAYSURF.blit(titleSurf, titleRect)
    showTextScreen2(' ')
    DISPLAYSURF.fill(BGCOLOR)
    choose = dumbmenu(DISPLAYSURF, [
                        'Start Game',
                        'Mute',
                        'Show Highscore',
                        'Instruction',
                        'Quit Game'], 160,250,None,40,1.4)
    DISPLAYSURF.fill(BGCOLOR)
    if choose == 0:
        DISPLAYSURF.fill(BGCOLOR)

        if muteFlag == 0 :
            if random.randint(0, 1) == 0:
                pygame.mixer.music.load('Tell_me.mid')
            else:
                pygame.mixer.music.load('Tell_me.mid')
            pygame.mixer.music.play(1, 0.0)
        runGame()
        pygame.mixer.music.stop()
        showTextScreen3('Game Over')
        main()

    elif choose == 1:
        DISPLAYSURF.fill(BGCOLOR)
        showTextScreen2('About Mute')
        DISPLAYSURF.fill(BGCOLOR)
        choose2 = dumbmenu(DISPLAYSURF, [
                                'Mute',
                                'Unmute',
                                'Back'], 160,350,None,30,1.4)
        if choose2 == 0 :
            muteFlag = -1
            main()
        elif choose2 == 1 :
            muteFlag = 0
            main()
        elif choose2 == 2 :
            main()

    elif choose == 2:
        DISPLAYSURF.fill(BGCOLOR)
        showScoreScreen()

        choose2 = dumbmenu(DISPLAYSURF, [
                                'Back'], 160,350,None,30,1.4)
        if choose2 == 0 :
            DISPLAYSURF.fill(BGCOLOR)
            main()

    elif choose == 3:
        DISPLAYSURF.fill(BGCOLOR)
        showTextScreen4()

        choose2 = dumbmenu(DISPLAYSURF, [
                                'Back'], 160,350,None,30,1.4)
        if choose2 == 0 :
            DISPLAYSURF.fill(BGCOLOR)
            main()

def runGame():
    # setup variables for the start of the game
    board = getBlankBoard()
    lastMoveDownTime = time.time()
    lastMoveSidewaysTime = time.time()
    lastFallTime = time.time()
    movingDown = False # note: there is no movingUp variable
    movingLeft = False
    movingRight = False
    score = 0
    level, fallFreq = calculateLevelAndFallFreq(score)

    fallingPiece = getNewPiece()
    nextPiece = getNewPiece()

    while True: # game loop
        if fallingPiece == None:
            # No falling piece in play, so start a new piece at the top
            fallingPiece = nextPiece
            nextPiece = getNewPiece()
            lastFallTime = time.time() # reset lastFallTime

            if not isValidPosition(board, fallingPiece):
                return # can't fit a new piece on the board, so game over

        checkForQuit()
        for event in pygame.event.get(): # event handling loop
            if event.type == KEYUP:
                if (event.key == K_p):
                    # Pausing the game
                    # DISPLAYSURF.fill(BGCOLOR)
                    pygame.mixer.music.stop()
                    showTextScreen('Paused') # pause until a key press
                    pygame.mixer.music.play(-1, 0.0)
                    lastFallTime = time.time()
                    lastMoveDownTime = time.time()
                    lastMoveSidewaysTime = time.time()
                elif (event.key == K_LEFT or event.key == K_a):
                    movingLeft = False
                elif (event.key == K_RIGHT or event.key == K_d):
                    movingRight = False
                elif (event.key == K_DOWN or event.key == K_s):
                    movingDown = False

            elif event.type == KEYDOWN:
                # moving the piece sideways
                if (event.key == K_LEFT or event.key == K_a) and isValidPosition(board, fallingPiece, adjX=-1):
                    fallingPiece['x'] -= 1
                    movingLeft = True
                    movingRight = False
                    lastMoveSidewaysTime = time.time()

                elif (event.key == K_RIGHT or event.key == K_d) and isValidPosition(board, fallingPiece, adjX=1):
                    fallingPiece['x'] += 1
                    movingRight = True
                    movingLeft = False
                    lastMoveSidewaysTime = time.time()

                # rotating the piece (if there is room to rotate)
                elif (event.key == K_UP or event.key == K_w):
                    fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(PIECES[fallingPiece['shape']])
                    if not isValidPosition(board, fallingPiece):
                        fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(PIECES[fallingPiece['shape']])
                elif (event.key == K_q): # rotate the other direction
                    fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(PIECES[fallingPiece['shape']])
                    if not isValidPosition(board, fallingPiece):
                        fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(PIECES[fallingPiece['shape']])

                # making the piece fall faster with the down key
                elif (event.key == K_DOWN or event.key == K_s):
                    movingDown = True
                    if isValidPosition(board, fallingPiece, adjY=1):
                        fallingPiece['y'] += 1
                    lastMoveDownTime = time.time()

                # move the current piece all the way down
                elif event.key == K_SPACE:
                    movingDown = False
                    movingLeft = False
                    movingRight = False
                    for i in range(1, BOARDHEIGHT):
                        if not isValidPosition(board, fallingPiece, adjY=i):
                            break
                    fallingPiece['y'] += i - 1
# block change!@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                elif event.key == K_z:
                    savePiece = fallingPiece
                    fallingPiece = nextPiece
                    nextPiece = savePiece
                    nextPiece['x'] = int(BOARDWIDTH / 2) - int(TEMPLATEWIDTH / 2)
                    nextPiece['y'] = -2
                    lastFallTime = time.time()


        # handle moving the piece because of user input
        if (movingLeft or movingRight) and time.time() - lastMoveSidewaysTime > MOVESIDEWAYSFREQ:
            if movingLeft and isValidPosition(board, fallingPiece, adjX=-1):
                fallingPiece['x'] -= 1
            elif movingRight and isValidPosition(board, fallingPiece, adjX=1):
                fallingPiece['x'] += 1
            lastMoveSidewaysTime = time.time()

        if movingDown and time.time() - lastMoveDownTime > MOVEDOWNFREQ and isValidPosition(board, fallingPiece, adjY=1):
            fallingPiece['y'] += 1
            lastMoveDownTime = time.time()

        # let the piece fall if it is time to fall
        if time.time() - lastFallTime > fallFreq:
            # see if the piece has landed
            if not isValidPosition(board, fallingPiece, adjY=1):
                # falling piece has landed, set it on the board
                addToBoard(board, fallingPiece)
                score += removeCompleteLines(board)
                if highScore < score :
                    newHighScore = score
                    highScoreFile = open("score.txt", "w")
                    highScoreFile.write(str(newHighScore))
                    highScoreFile.close()
                level, fallFreq = calculateLevelAndFallFreq(score)
                fallingPiece = None
            else:
                # piece did not land, just move the piece down
                fallingPiece['y'] += 1
                lastFallTime = time.time()

        # drawing everything on the screen
        DISPLAYSURF.fill(BGCOLOR)
        drawBoard(board)
        drawStatus(score, level)
        drawNextPiece(nextPiece)
        if fallingPiece != None:
            drawPiece(fallingPiece)

        pygame.display.update()
        FPSCLOCK.tick(FPS)

    


def makeTextObjs(text, font, color):
    surf = font.render(text, True, color)
    return surf, surf.get_rect()


def terminate():
    pygame.quit()
    sys.exit()


def checkForKeyPress():
    # Go through event queue looking for a KEYUP event.
    # Grab KEYDOWN events to remove them from the event queue.
    checkForQuit()

    for event in pygame.event.get([KEYDOWN, KEYUP]):
        if event.type == KEYDOWN:
            continue
        return event.key
    return None


def showTextScreen(text):
    # This function displays large text in the
    # center of the screen until a key is pressed.
    # Draw the text drop shadow
    titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTSHADOWCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
    DISPLAYSURF.blit(titleSurf, titleRect)

    # Draw the text
    titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) - 3)
    DISPLAYSURF.blit(titleSurf, titleRect)

    # Draw the additional "Press a key to play." text.
    pressKeySurf, pressKeyRect = makeTextObjs('Press a key to play.', BASICFONT, TEXTCOLOR)
    pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 100)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

    while checkForKeyPress() == None:
        pygame.display.update()
        FPSCLOCK.tick()

def showTextScreen2(text):
    # This function displays large text in the
    # center of the screen until a key is pressed.
    # Draw the text drop shadow
    titleSurf, titleRect = makeTextObjs(text, MIDFONT, TEXTSHADOWCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
    DISPLAYSURF.blit(titleSurf, titleRect)
    titleSurf, titleRect = makeTextObjs(text, MIDFONT, TEXTCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) - 3)
    DISPLAYSURF.blit(titleSurf, titleRect)

    # Draw the additional "Press a key to play." text.
    # pressKeySurf, pressKeyRect = makeTextObjs('Press a key to play.', BASICFONT, TEXTCOLOR)
    # pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 100)
    # DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

    while checkForKeyPress() == None:
        pygame.display.update()
        FPSCLOCK.tick()

def showTextScreen3(text):
    # This function displays large text in the
    # center of the screen until a key is pressed.
    # Draw the text drop shadow
    titleSurf, titleRect = makeTextObjs(text, MIDFONT, TEXTSHADOWCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
    DISPLAYSURF.blit(titleSurf, titleRect)
    titleSurf, titleRect = makeTextObjs(text, MIDFONT, TEXTCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) - 3)
    DISPLAYSURF.blit(titleSurf, titleRect)

    # Draw the additional "Press a key to play." text.
    pressKeySurf, pressKeyRect = makeTextObjs('Press a key to go main', BASICFONT, TEXTCOLOR)
    pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 100)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

    while checkForKeyPress() == None:
        pygame.display.update()
        FPSCLOCK.tick()

def showTextScreen4():

    lSurf, lRect = makeTextObjs('Left arrow : Move left', SFONT, TEXTCOLOR)
    rSurf, rRect = makeTextObjs('Right arrow : Move right', SFONT, TEXTCOLOR)
    uSurf, uRect = makeTextObjs('Up arrow : rotate right', SFONT, TEXTCOLOR)
    dSurf, dRect = makeTextObjs('Down arrow : Slow drop', SFONT, TEXTCOLOR)
    sSurf, sRect = makeTextObjs('Space bar : Fast drop', SFONT, TEXTCOLOR)
    pSurf, pRect = makeTextObjs('P key : Pause game', SFONT, TEXTCOLOR)
    zSurf, zRect = makeTextObjs('Z key : Get next block', SFONT, TEXTCOLOR)
    lRect.center = (int(WINDOWWIDTH / 2)-3, int(WINDOWHEIGHT / 2)-150)
    rRect.center = (int(WINDOWWIDTH / 2)-3, int(WINDOWHEIGHT / 2)-120)
    uRect.center = (int(WINDOWWIDTH / 2)-3, int(WINDOWHEIGHT / 2)-90)
    dRect.center = (int(WINDOWWIDTH / 2)-3, int(WINDOWHEIGHT / 2)-60)
    sRect.center = (int(WINDOWWIDTH / 2)-3, int(WINDOWHEIGHT / 2)-30)
    pRect.center = (int(WINDOWWIDTH / 2)-3, int(WINDOWHEIGHT / 2))
    zRect.center = (int(WINDOWWIDTH / 2)-3, int(WINDOWHEIGHT / 2)+30)
    DISPLAYSURF.blit(lSurf, lRect)
    DISPLAYSURF.blit(rSurf, rRect)
    DISPLAYSURF.blit(uSurf, uRect)
    DISPLAYSURF.blit(dSurf, dRect)
    DISPLAYSURF.blit(sSurf, sRect)
    DISPLAYSURF.blit(pSurf, pRect)
    DISPLAYSURF.blit(zSurf, zRect)

    while checkForKeyPress() == None:
        pygame.display.update()
        FPSCLOCK.tick()

def showScoreScreen():

    highScoreFile = open("score.txt", "r")
    highScore = int(highScoreFile.read())
    highScoreFile.close()
    sSurf, sRect = makeTextObjs('High Score: %s' % highScore, MIDFONT, TEXTCOLOR)
    sRect.center = (int(WINDOWWIDTH / 2)-3, int(WINDOWHEIGHT / 2)-30)
    DISPLAYSURF.blit(sSurf, sRect)

    while checkForKeyPress() == None:
        pygame.display.update()
        FPSCLOCK.tick()

def checkForQuit():
    for event in pygame.event.get(QUIT): # get all the QUIT events
        terminate() # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate() # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event) # put the other KEYUP event objects back

def calculateLevelAndFallFreq(score):
    # Based on the score, return the level the player is on and
    # how many seconds pass until a falling piece falls one space.
    level = int(score / 10) + 1
    fallFreq = 0.27 - (level * 0.02)
    return level, fallFreq

def getNewPiece():
    # return a random new piece in a random rotation and color
    shape = random.choice(list(PIECES.keys()))
    newPiece = {'shape': shape,
                'rotation': random.randint(0, len(PIECES[shape]) - 1),
                'x': int(BOARDWIDTH / 2) - int(TEMPLATEWIDTH / 2),
                'y': -2, # start it above the board (i.e. less than 0)
                'color': random.randint(0, len(COLORS)-1)}
    return newPiece


def addToBoard(board, piece):
    # fill in the board based on piece's location, shape, and rotation
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if PIECES[piece['shape']][piece['rotation']][y][x] != BLANK:
                board[x + piece['x']][y + piece['y']] = piece['color']


def getBlankBoard():
    # create and return a new blank board data structure
    board = []
    for i in range(BOARDWIDTH):
        board.append([BLANK] * BOARDHEIGHT)
    return board


def isOnBoard(x, y):
    return x >= 0 and x < BOARDWIDTH and y < BOARDHEIGHT


def isValidPosition(board, piece, adjX=0, adjY=0):
    # Return True if the piece is within the board and not colliding
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            isAboveBoard = y + piece['y'] + adjY < 0
            if isAboveBoard or PIECES[piece['shape']][piece['rotation']][y][x] == BLANK:
                continue
            if not isOnBoard(x + piece['x'] + adjX, y + piece['y'] + adjY):
                return False
            if board[x + piece['x'] + adjX][y + piece['y'] + adjY] != BLANK:
                return False
    return True

def isCompleteLine(board, y):
    # Return True if the line filled with boxes with no gaps.
    for x in range(BOARDWIDTH):
        if board[x][y] == BLANK:
            return False
    return True


def removeCompleteLines(board):
    # Remove any completed lines on the board, move everything above them down, and return the number of complete lines.
    numLinesRemoved = 0
    y = BOARDHEIGHT - 1 # start y at the bottom of the board
    while y >= 0:
        if isCompleteLine(board, y):
            # Remove the line and pull boxes down by one line.
            for pullDownY in range(y, 0, -1):
                for x in range(BOARDWIDTH):
                    board[x][pullDownY] = board[x][pullDownY-1]
            # Set very top line to blank.
            for x in range(BOARDWIDTH):
                board[x][0] = BLANK
            numLinesRemoved += 1
            # Note on the next iteration of the loop, y is the same.
            # This is so that if the line that was pulled down is also
            # complete, it will be removed.
        else:
            y -= 1 # move on to check next row up
    return numLinesRemoved


def convertToPixelCoords(boxx, boxy):
    # Convert the given xy coordinates of the board to xy
    # coordinates of the location on the screen.
    return (XMARGIN + (boxx * BOXSIZE)), (TOPMARGIN + (boxy * BOXSIZE))

def dumbmenu(screen, menu, x_pos = 100, y_pos = 100, font = None,
            size = 150, distance = 1.4, fgcolor = (255,255,255),
            cursorcolor = (255,0,0), exitAllowed = True):
    # Draw the Menupoints
    pygame.font.init()
    if font == None:
        myfont = pygame.font.Font(None, size)
    else:
        myfont = pygame.font.SysFont(font, size)
    cursorpos = 0
    renderWithChars = False
    for i in menu:
        if renderWithChars == False:
            text =  myfont.render(str(cursorpos + 1)+".  " + i,
                True, fgcolor)
        else:
            text =  myfont.render(chr(char)+".  " + i,
                True, fgcolor)
            char += 1
        textrect = text.get_rect()
        textrect = textrect.move(x_pos, 
                   (size // distance * cursorpos) + y_pos)
        screen.blit(text, textrect)
        pygame.display.update(textrect)
        cursorpos += 1
        if cursorpos == 9:
            renderWithChars = True
            char = 65

    # Draw the ">", the Cursor
    cursorpos = 0
    cursor = myfont.render(">", True, cursorcolor)
    cursorrect = cursor.get_rect()
    cursorrect = cursorrect.move(x_pos - (size // distance),
                 (size // distance * cursorpos) + y_pos)

    # The whole While-loop takes care to show the Cursor, move the
    # Cursor and getting the Keys (1-9 and A-Z) to work...
    ArrowPressed = True
    exitMenu = False
    clock = pygame.time.Clock()
    filler = pygame.Surface.copy(screen)
    fillerrect = filler.get_rect()
    while True:
        clock.tick(30)
        if ArrowPressed == True:
            screen.blit(filler, fillerrect)
            pygame.display.update(cursorrect)
            cursorrect = cursor.get_rect()
            cursorrect = cursorrect.move(x_pos - (size // distance),
                         (size // distance * cursorpos) + y_pos)
            screen.blit(cursor, cursorrect)
            pygame.display.update(cursorrect)
            ArrowPressed = False
        if exitMenu == True:
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return -1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and exitAllowed == True:
                    if cursorpos == len(menu) - 1:
                        exitMenu = True
                    else:
                        cursorpos = len(menu) - 1; ArrowPressed = True


                # This Section is huge and ugly, I know... But I don't
                # know a better method for this^^
                if event.key == pygame.K_1:
                    cursorpos = 0; ArrowPressed = True; exitMenu = True
                elif event.key == pygame.K_2 and len(menu) >= 2:
                    cursorpos = 1; ArrowPressed = True; exitMenu = True
                elif event.key == pygame.K_3 and len(menu) >= 3:
                    cursorpos = 2; ArrowPressed = True; exitMenu = True
                elif event.key == pygame.K_4 and len(menu) >= 4:
                    cursorpos = 3; ArrowPressed = True; exitMenu = True
                elif event.key == pygame.K_5 and len(menu) >= 5:
                    cursorpos = 4; ArrowPressed = True; exitMenu = True
                elif event.key == pygame.K_6 and len(menu) >= 6:
                    cursorpos = 5; ArrowPressed = True; exitMenu = True
                elif event.key == pygame.K_7 and len(menu) >= 7:
                    cursorpos = 6; ArrowPressed = True; exitMenu = True
                elif event.key == pygame.K_8 and len(menu) >= 8:
                    cursorpos = 7; ArrowPressed = True; exitMenu = True
                elif event.key == pygame.K_9 and len(menu) >= 9:
                    cursorpos = 8; ArrowPressed = True; exitMenu = True
                elif event.key == pygame.K_a and len(menu) >= 10:
                    cursorpos = 9; ArrowPressed = True; exitMenu = True
                elif event.key == pygame.K_b and len(menu) >= 11:
                    cursorpos = 10; ArrowPressed = True; exitMenu = True
                elif event.key == pygame.K_c and len(menu) >= 12:
                    cursorpos = 11; ArrowPressed = True; exitMenu = True
                elif event.key == pygame.K_d and len(menu) >= 13:
                    cursorpos = 12; ArrowPressed = True; exitMenu = True
                elif event.key == pygame.K_e and len(menu) >= 14:
                    cursorpos = 13; ArrowPressed = True; exitMenu = True
                elif event.key == pygame.K_f and len(menu) >= 15:
                    cursorpos = 14; ArrowPressed = True; exitMenu = True
                elif event.key == pygame.K_g and len(menu) >= 16:
                    cursorpos = 15; ArrowPressed = True; exitMenu = True
                elif event.key == pygame.K_h and len(menu) >= 17:
                    cursorpos = 16; ArrowPressed = True; exitMenu = True
                elif event.key == pygame.K_i and len(menu) >= 18:
                    cursorpos = 17; ArrowPressed = True; exitMenu = True
                elif event.key == pygame.K_j and len(menu) >= 19:
                    cursorpos = 18; ArrowPressed = True; exitMenu = True
                elif event.key == pygame.K_k and len(menu) >= 20:
                    cursorpos = 19; ArrowPressed = True; exitMenu = True
                elif event.key == pygame.K_l and len(menu) >= 21:
                    cursorpos = 20; ArrowPressed = True; exitMenu = True
                elif event.key == pygame.K_m and len(menu) >= 22:
                    cursorpos = 21; ArrowPressed = True; exitMenu = True
                elif event.key == pygame.K_n and len(menu) >= 23:
                    cursorpos = 22; ArrowPressed = True; exitMenu = True
                elif event.key == pygame.K_o and len(menu) >= 24:
                    cursorpos = 23; ArrowPressed = True; exitMenu = True
                elif event.key == pygame.K_p and len(menu) >= 25:
                    cursorpos = 24; ArrowPressed = True; exitMenu = True
                elif event.key == pygame.K_q and len(menu) >= 26:
                    cursorpos = 25; ArrowPressed = True; exitMenu = True
                elif event.key == pygame.K_r and len(menu) >= 27:
                    cursorpos = 26; ArrowPressed = True; exitMenu = True
                elif event.key == pygame.K_s and len(menu) >= 28:
                    cursorpos = 27; ArrowPressed = True; exitMenu = True
                elif event.key == pygame.K_t and len(menu) >= 29:
                    cursorpos = 28; ArrowPressed = True; exitMenu = True
                elif event.key == pygame.K_u and len(menu) >= 30:
                    cursorpos = 29; ArrowPressed = True; exitMenu = True
                elif event.key == pygame.K_v and len(menu) >= 31:
                    cursorpos = 30; ArrowPressed = True; exitMenu = True
                elif event.key == pygame.K_w and len(menu) >= 32:
                    cursorpos = 31; ArrowPressed = True; exitMenu = True
                elif event.key == pygame.K_x and len(menu) >= 33:
                    cursorpos = 32; ArrowPressed = True; exitMenu = True
                elif event.key == pygame.K_y and len(menu) >= 34:
                    cursorpos = 33; ArrowPressed = True; exitMenu = True
                elif event.key == pygame.K_z and len(menu) >= 35:
                    cursorpos = 34; ArrowPressed = True; exitMenu = True
                elif event.key == pygame.K_UP:
                    ArrowPressed = True
                    if cursorpos == 0:
                        cursorpos = len(menu) - 1
                    else:
                        cursorpos -= 1
                elif event.key == pygame.K_DOWN:
                    ArrowPressed = True
                    if cursorpos == len(menu) - 1:
                        cursorpos = 0
                    else:
                        cursorpos += 1
                elif event.key == pygame.K_KP_ENTER or \
                     event.key == pygame.K_RETURN:
                            exitMenu = True
    
    return cursorpos


def drawBox(boxx, boxy, color, pixelx=None, pixely=None):
    # draw a single box (each tetromino piece has four boxes)
    # at xy coordinates on the board. Or, if pixelx & pixely
    # are specified, draw to the pixel coordinates stored in
    # pixelx & pixely (this is used for the "Next" piece).
    if color == BLANK:
        return
    if pixelx == None and pixely == None:
        pixelx, pixely = convertToPixelCoords(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, COLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 1, BOXSIZE - 1))
    pygame.draw.rect(DISPLAYSURF, LIGHTCOLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 4, BOXSIZE - 4))


def drawBoard(board):
    # draw the border around the board
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (XMARGIN - 3, TOPMARGIN - 7, (BOARDWIDTH * BOXSIZE) + 8, (BOARDHEIGHT * BOXSIZE) + 8), 5)

    # fill the background of the board
    pygame.draw.rect(DISPLAYSURF, BGCOLOR, (XMARGIN, TOPMARGIN, BOXSIZE * BOARDWIDTH, BOXSIZE * BOARDHEIGHT))
    # draw the individual boxes on the board
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            drawBox(x, y, board[x][y])


def drawStatus(score, level):
    # draw the score text
    scoreSurf = BASICFONT.render('Score: %s' % score, True, TEXTCOLOR)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 600, 30)
    DISPLAYSURF.blit(scoreSurf, scoreRect)

    # draw the level text
    levelSurf = BASICFONT.render('Level: %s' % level, True, TEXTCOLOR)
    levelRect = levelSurf.get_rect()
    levelRect.topleft = (WINDOWWIDTH - 600, 60)
    DISPLAYSURF.blit(levelSurf, levelRect)

    # ruleSurf = BASICFONT.render('10 point: 1 level up', True, TEXTCOLOR)
    # ruleRect = ruleSurf.get_rect()
    # ruleRect.topright = (WINDOWWIDTH - 150, 10)
    # DISPLAYSURF.blit(ruleSurf, ruleRect)


def drawPiece(piece, pixelx=None, pixely=None):
    shapeToDraw = PIECES[piece['shape']][piece['rotation']]
    if pixelx == None and pixely == None:
        # if pixelx & pixely hasn't been specified, use the location stored in the piece data structure
        pixelx, pixely = convertToPixelCoords(piece['x'], piece['y'])

    # draw each of the boxes that make up the piece
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if shapeToDraw[y][x] != BLANK:
                drawBox(None, None, piece['color'], pixelx + (x * BOXSIZE), pixely + (y * BOXSIZE))


def drawNextPiece(piece):
    # draw the "next" text
    nextSurf = BASICFONT.render('Next:', True, TEXTCOLOR)
    nextRect = nextSurf.get_rect()
    nextRect.topleft = (WINDOWWIDTH - 120, 50)
    DISPLAYSURF.blit(nextSurf, nextRect)
    # draw the "next" piece
    drawPiece(piece, pixelx=WINDOWWIDTH-120, pixely=100)


if __name__ == '__main__':
    main()