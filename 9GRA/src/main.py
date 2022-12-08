# game gui library
import pygame
# quit program
import sys
# pause program
import time
# generation random position of knight or king
import random
# implementation of algo for move
from knight_tour import KnightTour

class Game(object):
    def __init__(self):
        # set up color
        self.light_tile_color = (245, 245, 220)
        self.dark_tile_color = (107, 142, 35)
        self.black_color = (0, 0, 0)
        self.red_actual_color = (255, 0, 0)
    
    # private method:
    #   input: board size, tile size
    #   return
    # Note: Create chess board
    def __draw_background(self, board_size: list, tile_size: int):
        # draws tiles background on Chessboard
        self.screen.fill(self.dark_tile_color)
        # every second fill rectangle by green color
        for i in range(board_size[0]):
            for j in range(board_size[1]):
                if((i + j) % 2 == 0):
                    pygame.draw.rect(
                        self.screen, 
                        self.light_tile_color, 
                        (tile_size * j, tile_size * i, tile_size, tile_size), 
                        0
                    )

    # private method:
    #   input: board size, tile size, actual knight positioin, chess board
    #   return
    # Note: Draw actual position of the knight / king - red, and old positions - black
    def __draw_tiles(self, board_size: list, tile_size: int, knight_pos: list, board: list):
        # draws mark on Chessboard tiles during King's moving
        for i in range(board_size[0]):
            for j in range(board_size[1]):
                if(knight_pos == [i, j]):
                    pygame.draw.circle(
                        self.screen, 
                        self.red_actual_color,
                        (tile_size * j + tile_size // 2, tile_size * i + tile_size // 2), 
                        tile_size // 12, 
                        0
                    )

                elif(board[i][j] != 0):
                    pygame.draw.circle(
                        self.screen, 
                        self.black_color,                        
                        (tile_size * j + tile_size // 2, tile_size * i + tile_size // 2), 
                        tile_size // 12,  
                        0
                    )

    # private method:
    #   input: start tile, end tile, size of tile
    #   return
    # Note: Draw line from old position to new position
    def __draw_line(self, start: list, end: list, tile_size: int):
        # draws line during King's moving on the Chessboard
        pygame.draw.line(
            self.screen, 
            self.black_color,
            (tile_size * start[1] + tile_size // 2, tile_size * start[0] + tile_size // 2),
            (tile_size * end[1] + tile_size // 2, tile_size * end[0] + tile_size // 2),
            2
        )

    # public method:
    #   - main
    def main(self, board_size: list, knight_pos: list, speed: float, option: int = 1):
        # height of window
        screenSizeX = 600
        # width of window
        screenSizeY = 600

        # setting up of tile size
        if(screenSizeX//board_size[1] >= screenSizeY//board_size[0]):
            tile_size = screenSizeY // board_size[0]
        
        else:
            tile_size = screenSizeX // board_size[1]

        # init algorithm
        knight_tour = KnightTour(board_size=board_size, option = option)

        # pygame init
        pygame.init()

        # draw background, and draw tiles into game
        self.screen = pygame.display.set_mode((tile_size * board_size[1], tile_size * board_size[0]))
        self.__draw_background(board_size, tile_size)

        board = knight_tour.board
        runUpdate = True
        self.__draw_tiles(board_size, tile_size, knight_pos, board)
        
        while True:
            # if quit is press, process is quit
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if runUpdate:
                last_knight_pos = knight_pos

                if last_knight_pos:
                    # find next position from actual position
                    knight_pos = knight_tour.warnsdorff(knight_pos) 
                    board = knight_tour.board
                    if knight_pos:
                        self.__draw_line(last_knight_pos, knight_pos, tile_size)
                    self.__draw_tiles(board_size, tile_size, knight_pos, board)
                    time.sleep(speed)
                    
                else:
                    # all tiles on the Chessboard are marked
                    runUpdate = False
            
            pygame.display.set_caption("Knight\'s Tour by Warnsdorff\'s algorithm")
            pygame.display.update()


if __name__ == "__main__":
    # SETTINGS:
    # set number of tiles on the chessboard
    board_size = [8, 8]

    # set initial position of knight (min: 0, max: board_size-1)
    init_pos = [random.randint(0, board_size[0] - 1), random.randint(0, board_size[1] - 1)]
    
    print("---------------------------------------------")
    print("[INFO] IACS FME BUT")
    print("[INFO] Author: Martin Juricek")
    print("[INFO] Knight's Tour by Warndorff's algorithm")
    print("---------------------------------------------")

    game = Game()
    # input: board size, init position, pause, king = 2 or knights = 1 move
    game.main(board_size, init_pos, 0.5, 2)
