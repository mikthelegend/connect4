from copy import deepcopy
import curses
import math
import random

MAX_DEPTH = 5

# Recursively check all options, alternating turns, until someone has won. Return a +1 for yellow win, -1 for red win. Sum all options and return.
mainScore = 0
playingAs = "Y"
def calculateMoveScore(board, piece, depth = 1):
    global mainScore
    global playingAs
    if depth > MAX_DEPTH: return 0
    newBoard = deepcopy(board)
    columns = list(range(7))
    random.shuffle(columns)
    for i in columns:
        if newBoard.place(i, piece):
            printBoard(newBoard)
            if newBoard.checkWin(piece):
                if piece == playingAs:
                    mainScore += 1/depth
                else:
                    mainScore -= 1
                return

            if piece == "Y":
                newPiece = "R"
            else:
                newPiece = "Y"
            
            scr.addstr(14, 0, str(mainScore))
            calculateMoveScore(newBoard, newPiece, depth+1)
            
        

# Check all 7 moves for all possible outcomes, scoring each by how many scenarios end in victory or defeat.
def calculateBestMove(board, piece = "Y"):
    scr.clear()
    best = -math.inf
    choice = None
    global playingAs
    playingAs = piece
    for i in range(7):
        newBoard = deepcopy(board)
        if newBoard.place(i, piece):
            if newBoard.checkWin(piece): return i
            global mainScore
            mainScore = 0
            if piece == "R":
                adversaryPiece = "Y"
            else:
                adversaryPiece = "R"
            calculateMoveScore(newBoard, adversaryPiece)
            score = mainScore
            if score > best:
                best = score
                choice = i
            scr.addstr(i, 40, "Col: " + str(i) + ", Score: " + str(score) + ", Choice: " + str(choice))
    
    return choice

scr = curses.initscr()
scr.clear()
def printBoard(board):
    for i in range(6):
        scr.addstr(2*i+1, 0, "|---------------------------|")
        for j in range(7):
            scr.addch(2*i,0, "|")
            if 5-i < len(board.grid[j]):
                scr.addstr(2*i, 4*j+2, board.grid[j][5-i] + " |")
            else:
                scr.addstr(2*i, 4*j+2, "  |")
    
    scr.refresh()

def end():
    curses.endwin()
