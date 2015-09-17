# -*- coding: utf-8 -*-
import random,pygame, sys
import copy
from pygame.locals import *
BOARDWIDTH = 4
BOARDHEIGHT = 4
TARGET_POINTS = 2048
MINIMUM_WIN_SCORE = 18432
SCORE = 0
icons = [2,4,8,16,32,64,128,256,512,1024,2048,4096,8192]




def initializeBoard():
    
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



Board = initializeBoard()




def getBoard():
    global Board
    return Board



def printBoard():
    global SCORE
    global Board
    print "-------------------"
    print "Score:     ",SCORE
    for x in  range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            print "   ",Board[x][y],
        print " "
    print "-------------------"





def rotateLeft(arrayBoard):
    #global Board
    rotatedBoard = []
    for x in range(BOARDWIDTH-1,-1,-1):
        row = []
        for y in range(BOARDHEIGHT):
            #rotatedBoard[BOARDWIDTH-y-1][x]=Board[x][y];
            row.append(arrayBoard[y][x])
        rotatedBoard.append(row)
    return rotatedBoard
    """
    for x in  range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            print "   ",rotatedBoard[x][y],
        print " "
    print "-------------------"
    """



    
def rotateRight(arrayBoard):
    #global Board
    rotatedBoard = []
    for x in range(BOARDWIDTH):
        row = []
        for y in range(BOARDHEIGHT):
            #rotatedBoard[x][y] = Board[BOARDWIDTH-y-1][x];
            row.append(arrayBoard[BOARDWIDTH-y-1][x])
        rotatedBoard.append(row)
    return rotatedBoard



    
def move(direction,arrayBoard,flag):
    global SCORE
    global Board
    points=0
    if(direction == 8): #up
        arrayBoard=rotateLeft(arrayBoard)
    elif(direction == 6): #right
        arrayBoard=rotateLeft(arrayBoard)
        arrayBoard=rotateLeft(arrayBoard)
    elif(direction == 2): #down
        arrayBoard=rotateRight(arrayBoard)
    for x in range(BOARDWIDTH) :
        lastmergePosition=0
        for y in range(1,BOARDHEIGHT): #from1
            if(arrayBoard[x][y] == 0):
                continue
            previousposition=y-1
            while(previousposition>lastmergePosition and arrayBoard[x][previousposition]==0):
                previousposition = previousposition-1
            #if(previousposition == y):
            if(arrayBoard[x][previousposition]==0):
                arrayBoard[x][previousposition]=arrayBoard[x][y]
                arrayBoard[x][y]=0
            elif(arrayBoard[x][previousposition] == arrayBoard[x][y]):
                arrayBoard[x][previousposition]*=2
                arrayBoard[x][y]=0
                points+=arrayBoard[x][previousposition]
                lastmergePosition=previousposition+1
            elif(arrayBoard[x][previousposition]!=arrayBoard[x][y] and previousposition+1!=y):
                arrayBoard[x][previousposition+1]=arrayBoard[x][y]
                arrayBoard[x][y]=0

    SCORE+=points

    if(direction == 8): #up
        arrayBoard=rotateRight(arrayBoard)
    elif(direction == 6): #right
        arrayBoard=rotateRight(arrayBoard)
        arrayBoard=rotateRight(arrayBoard)
    elif(direction == 2): #down
        arrayBoard=rotateLeft(arrayBoard)

    if(flag == 1):
        Board = arrayBoard
    return points




def isEqual(currentBoard,newBoard):
    """
    print "currentBoard"
    for x in  range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            print "   ",currentBoard[x][y],
        print " "
    print "-------------------"
    

    print "newBoard"
    for x in  range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            print "   ",newBoard[x][y],
        print " "
    print "-------------------"

    """
    
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if(currentBoard[x][y]!=newBoard[x][y]):
                return 0
    return 1




def hasWon():
    global Board
    global SCORE
    if(SCORE < MINIMUM_WIN_SCORE):
        return 0
    for x in range(BOARDWIDTH):
        for y in range(BOARDHIGHT):
            if(Board[x][y] >= TARGET_POINTS):
                return 1
    return 0




def getEmptyCellIds():
    global Board
    cells = []
    for x in range(BOARDWIDTH):
        for y in range(BOARDWIDTH):
            if(Board[x][y] == 0):
                cells.append(BOARDWIDTH*x+y)
    return cells




def getNumberOfEmptyCells():
    #if()#not completed
    numberOfEmptycell=len(getEmptyCellIds())
    return numberOfEmptycell




def isGameTerminated():
    terminated = 0
    if(hasWon() == 1):
        terminsted = 1
    else:
        #may be error
        copyBoard=copy.deepcopy(Board)
        if(getNumberOfEmptyCells()==0):
            if(move(8,copyBoard,0) ==0 and move(2,copyBoard,0) == 0 and move(6,copyBoard,0) == 0 and move(4,copyBoard,0) ==0):
                terminated = 1

    return terminated




def setEmptyCell(x,y,randomCellValue):
    global Board
    if(Board[x][y] == 0):
        Board[x][y] = randomCellValue
        #set emptycells=0



def addRandomCell():
    emptyCells=getEmptyCellIds()
    size=len(emptyCells)
    if(size == 0):
        return 0
    randomCellId = (random.choice(emptyCells))
    foo = [2,4]
    randomCellValue = (random.choice(foo))
    x = randomCellId/BOARDWIDTH
    y = randomCellId%BOARDWIDTH
    setEmptyCell(x,y,randomCellValue)
    return 1




def action(direction):
    global Board
    result=1
    currentBoard = copy.deepcopy(Board)
    
    newpoints = move(direction,Board,1)
    newBoard = getBoard()
    newcellAdded = 0
    
    if (isEqual(currentBoard,newBoard) == 0):
        newcellAdded = addRandomCell()#addRandomcell
    
    if (newpoints == 0 and newcellAdded == 0):
        if( isGameTerminated()):
            result =0#no more move
        else:
            result =1#invalid move
    else:
        if(newpoints>=TARGET_POINTS):
            result = 2#win not completed
        
        else:
            if(isGameTerminated()):
                result = 0#no more move
        
    return result




def printmenu():
    print "Your Choices:"
    print "1. Play the 2048 Game"
    print "2. Estimate the Accuracy of AI Solver"
    print "3. Help"
    print "4. Quit"
    print "Enter a number from 1-4:"




def playGame():
    print "Play the 2048 Game!"
    print "Use up arrow key for up,right arrow key for right,left arrow key for left,down arrow key for down"
    print "Press a to paly automaticallly and q for quit"

    hintDepth = 7;
    #object of game class thegame
    #hint=AIsolverfindbestmove()
    printBoard()
    #while valid
    result=1
    while (result):
        input_key=raw_input()
        if (input_key == '\n' or input_key == '\r'):
            continue
        if input_key == '8':#up
            result = action(8)
        elif input_key == '6':#right
            result = action(6)
        elif input_key == '2':#down
            result = action(2)
        elif input_key == '4':#left
            result = action(4)
        elif input_key == 'a':#auto
            result = action(hint)
        elif input_key == 'q':#quit
            print "Game ended, user quit"
            break
        else:
            print "Invalid key! Use up arrow key for up,right arrow key for right,left arrow key for left,down arrow key for down"
            continue
        printBoard()
    #end while some extra invalid statement




def help():
    print "The main idea of the game is that you have a 4×4 grid with Integer values, all of which are powers of 2."
    print "Zero valued cells are considered empty. At every point during the game you are able to move the values towards 4 directions Up, Down, Right or Left."
    print "When you perform a move all the values of the grid move towards that direction and they stop either when they reach the borders of the grid or when they reach another cell with non-zero value."
    print "If that previous cell has the same value, the two cells are merged into one cell with double value."
    print "At the end of every move a random value is added in the board in one of the empty cells and its value is either 2 with 0.9 probability or 4 with 0.1 probability."
    print "The game ends when the player manages to create a cell with value 2048 (win) or when there are no other moves tomake (lose)."





def consoleGame():
    print "----------------------------------"
    print "The 2048 Game in Python and PyGame"
    print "----------------------------------"
    while True:
        printmenu()
        choice=raw_input()
        if choice =='1':
            playGame()
        elif choice =='2':
            calculateAccuracy()
        elif choice =='3':
            help()
        elif choice == '4':
            return
        else:
            print "Wrong choice"


#consoleGame()






