# set up Knights and Kings move by chess game
KNIGHT_MOVES = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]
KINGS_MOVES = [(1, 0), (0, 1), (-1, 0), (0, -1), (-1, -1), (1, 1), (1, -1), (-1, -1)]

class KnightTour(object):
    def __init__(self, board_size: list, option: int):
        # set up board and board size
        self.board_size = board_size  
        self.board = []
        for _ in range(board_size[0]):
            temp = []
            for _ in range(board_size[1]):
                temp.append(0)
            self.board.append(temp) 
        self.move = 1
        self.option = option

    # public method:
    #   input: start position
    #   return next position
    # Note: compute from start position next position
    def warnsdorff(self, start_pos: list) -> list:

        x_pos, y_pos = start_pos
        self.board[x_pos][y_pos] = self.move

        if(self.move <= self.board_size[0] * self.board_size[1]):
            self.move += 1
            next_pos = self.__find_next_pos([x_pos, y_pos])
            return next_pos

    # public method:
    #   input: current position
    #   return next position
    # Note: compute closest neighbours for next move
    def __find_next_pos(self, current_pos: list) -> int:
        empty_neighbours = self.__find_neighbours(current_pos)
        
        if(len(empty_neighbours) == 0):
            return
        
        # set up least possible neighbour
        least_neighbour = 8
        least_neighbour_pos = []
        
        for neighbour in empty_neighbours:
            neighbours_of_neighbour = self.__find_neighbours(pos=neighbour)
            
            if(len(neighbours_of_neighbour) <= least_neighbour):
                least_neighbour = len(neighbours_of_neighbour)
                least_neighbour_pos = neighbour

        return least_neighbour_pos

    # public method:
    #   input: current position
    #   return neighbours
    # Note: compute neighbours depends on the chess game of knight or king
    def __find_neighbours(self, pos: list) -> list:
        neighbours = []
        
        if(self.option == 1):
            moves = KNIGHT_MOVES
        elif(self.option == 2):
            moves = KINGS_MOVES
        else:
            raise "Wrong input option!"
        
        for(dx, dy) in moves:
            x = pos[0] + dx
            y = pos[1] + dy
            if(0 <= x < self.board_size[0] and 0 <= y < self.board_size[1] and self.board[x][y] == 0):
                neighbours.append([x, y])

        return neighbours

