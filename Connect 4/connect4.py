import pygame
import math
import ai
from time import sleep


pygame.init()

WIDTH = 700
HEIGHT = 600

BLACK =    (0,   0,   0  )
WHITE =    (255, 255, 255)
RED =      (255, 100, 100)
RED_T =    (255,   0,   0, 100)
YELLOW =   (255, 255, 100)
YELLOW_T = (255, 255, 0, 100)
BLUE =     (100, 100, 255)

class Board():
    def __init__(self):
        self.grid = []
        for i in range(7):
            self.grid.append([])

    def draw(self):
        for i in range(7):
            pygame.draw.line(screen, BLACK, (i * WIDTH/7, 0), (i * WIDTH/7, HEIGHT))
        for i in range(6):
            pygame.draw.line(screen, BLACK, (0, i * HEIGHT/6), (WIDTH, i * HEIGHT/6))
        
        for i in range(7):
            for j in range(len(self.grid[i])):
                pos = ((i+0.5) * WIDTH/7, HEIGHT - (j+0.5) * HEIGHT/6)
                if self.grid[i][j] == "R":
                    col = RED
                else:
                    col = YELLOW
                pygame.draw.circle(screen, col, pos, min(WIDTH/14, HEIGHT/12)-10)
    
    def place(self, col, piece):
        if len(self.grid[col]) < 6:
            self.grid[col].append(piece)
            return True
        else:
            return False
    
    def checkWin(self, piece):
        playerBoard = []
        for i in range(7):
            playerBoard.append([])
            for j in range(6):
                if j < len(self.grid[i]) and self.grid[i][j] == piece:
                    playerBoard[i].append(1)
                else:
                    playerBoard[i].append(0)
        kernels = [
            [[1],[1],[1],[1]],
            [[1,1,1,1]],
            [
                [1,0,0,0],
                [0,1,0,0],
                [0,0,1,0],
                [0,0,0,1]
            ],
            [
                [0,0,0,1],
                [0,0,1,0],
                [0,1,0,0],
                [1,0,0,0]
            ]

        ]
        for kernel in kernels:
            resultBoard = convolute(playerBoard, kernel)
            result = any(4 in sublist for sublist in resultBoard)
            if result:
                return True
        return False

def convolute(input, kernel):
    output = []
    for i in range(len(input)-len(kernel)+1):
        output.append([])
        for j in range(len(input[i])-len(kernel[0])+1):
            output[i].append(0)
            for x in range(len(kernel)):
                for y in range(len(kernel[x])):
                    if i+x >= len(input): continue
                    if j+y >= len(input[i]): continue
                    output[i][j] += kernel[x][y] * input[i+x][j+y]
    return output

def printBoard(board):
    for i in range(len(board[0])-1, -1, -1):
        for j in range(len(board)):
            print(board[j][i], end=" ")
        print()
    print('-------------')


def highlight(turn):
    mouseX, mouseY = pygame.mouse.get_pos()
    x = math.floor(mouseX/(WIDTH/7))
    mouseX = (x + 0.5) * WIDTH/7
    y = (5-len(board.grid[x])+0.5) * HEIGHT/6
    if turn == "R":
        col = RED_T
    else:
        col = YELLOW_T

    if len(board.grid[x]) < 6: 
        surface = pygame.Surface((WIDTH,HEIGHT), pygame.SRCALPHA)
        pygame.draw.circle(surface, col, (mouseX, y), WIDTH/14 - 10)
        screen.blit(surface, (0,0))

def mousePressed():
    mouseX, mouseY = pygame.mouse.get_pos()
    col = math.floor(mouseX/(WIDTH/7))
    global turn
    if board.place(col, turn):

        global winner
        if board.checkWin(turn): # Check if that move won the game.
            if turn == "R":
                winner = "Red"
            else:
                winner = "Yellow"
            return
        # If it didn't win the game, swap turns.
        if turn == "R":
            turn = "Y"
        else:
            turn = "R"

        # If it is in gamemode 1, calculate a response from the AI.
        if mode == 1:
            aiChoice = ai.calculateBestMove(board)
            if aiChoice != None and board.place(aiChoice, turn):
                # Check if that response won the game.
                if board.checkWin(turn):
                    if turn == "R":
                        winner = "Red"
                    else:
                        winner = "Yellow"
                    return
                
                # If it didn't win the game, swap turns.
                if turn == "R":
                    turn = "Y"
                else:
                    turn = "R"
    

def winScreen(text):
    font = pygame.font.Font(None, 64)
    winMessage = font.render(text, True, BLACK)
    textRect = winMessage.get_rect()
    textRect.center = (WIDTH // 2, HEIGHT // 2)
    screen.blit(winMessage, textRect)

# Set up the drawing window
screen = pygame.display.set_mode([WIDTH, HEIGHT])

# Run until the user asks to quit
running = True

board = Board()
turn = "Y"
pressed = False
winner = None
# 0 = PvP, 1 = PvC, 2 = CvC
mode = 1


while running:
    # Check for close.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ai.end()
            running = False
    
    # Draw the board onscreen
    screen.fill(BLUE)
    board.draw()

    if winner:
        winScreen(winner + " Wins!")
    else:
        # If in gamemode 0 or 1, wait for mouse press.
        if mode == 0 or mode == 1:

            highlight(turn)
            if pygame.mouse.get_pressed()[0] and not pressed:
                pressed = True
                mousePressed()
            if not pygame.mouse.get_pressed()[0] and pressed:
                pressed = False

        # If in gamemode 2, let AI's play.
        elif mode == 2: 
            # Decide on best move for current turn.
            aiChoice = ai.calculateBestMove(board, turn)
            if aiChoice != None and board.place(aiChoice, turn): # Attempt to play that move.
                if board.checkWin(turn): # Check if that move won the game.
                    if turn == "R":
                        winner = "Red"
                    else:
                        winner = "Yellow"
                # If it didn't win the game, swap turns and repeat.
                if turn == "R":
                    turn = "Y"
                else:
                    turn = "R"
            sleep(1)
                



    pygame.display.flip()

pygame.quit()