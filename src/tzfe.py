import numpy as np
from random import randint, choice

class TZFE:
    """2048 game setup. """
    
    GROUNDTILE = 2
    GOAL = GROUNDTILE**11
    PROB4 = 0.1
    
    ACTIONS = dict(UP=0, RIGHT=1, DOWN=2, LEFT=3)
    
    def __init__(self, board_height=4, board_width=4):
        self.board_height = board_height
        self.board_width = board_width
        
        self.board = self.init_board(board_height, board_width)
        self.init_tiles()
        
        self.done = False
        self.score = 0
        self.num_goal = 0
        
    @staticmethod
    def init_board(height, width):
        board = np.zeros((height, width))
        return board
        
    def init_tiles(self, initial_tiles=2):
        """Find values and coordinates of initial tiles. """
        for i in range(initial_tiles):
            tile_val = self.new_tile()
            self._place_tile(tile_val)
            
    @staticmethod
    def new_tile(num_choices=10):
        """Find the value of the new tile. """
        # Create array with all the choices
        num_4 = int(TZFE.PROB4 * num_choices)    # Number of 4s
        choices = TZFE.GROUNDTILE * np.ones(num_choices)
        choices[:num_4] = 2 * TZFE.GROUNDTILE * np.ones(num_4)
        return choice(choices)          # Value of new tile

    def _place_tile(self, tile_val):
        """Find a random empty spot to place the new tile. """
        points = 1
        while points:
            x = randint(0, self.board_height-1)   # Proposed row
            y = randint(0, self.board_width-1)    # Proposed column 
            points = self.board[x,y]
        self.board[x,y] = tile_val
        return x, y
        
    def __call__(self,action):
        assert action in self.ACTIONS.values()
    
        self._check_done()
    
        if self.done:
            return self
            
            
        if self._move_tiles(action):
            tile_val = self.new_tile()
            self._place_tile(tile_val)
            
        return self
        
        
    def _move_tiles(self,action):
        """Move all tiles in correct direction. """
        
        # Rotate board
        board = np.rot90(self.board, action)
        board_height = board.shape[0]
        board_width = board.shape[1]
        
        moves = 0           #Number of tiles moving by one swipe
        merges = 0          #Number of tiles merging by one swipe

        # Move tiles
        for j in range(board_width):
            for i in range(board_height-1):
                if np.any(board[i:,j] > 0):
                    while board[i,j]==0:
                        for k in range(i, board_height-1):
                            board[k,j]=board[k+1,j]    
                        board[board_height-1,j]=0
                        moves += 1

        # Merge tiles
        for j in range(board_width):
            for i in range(board_height-1):
                if board[i,j]==board[i+1,j] and board[i,j]!=0:
                    board[i,j]=board[i,j]+board[i+1,j]
                    for k in range(i+1, board_height-1):
                        board[k,j] = board[k+1,j]
                    board[board_height-1,j]=0
                    self.score += board[i,j]
                    if board[i,j] == self.GOAL:
                        self.num_goal += 1
                    merges += 1
        
        # Rotate board back
        self.board = np.rot90(board, -action)
        if moves + merges == 0:
            return False
        else:
            return True
            
    def _check_done(self):
        """Check if board is filled and no merge
        is possible. """
        if not np.any(self.board == 0):
            pairs = 0
            for i in range(self.board_height-1):
                for j in range(self.board_width):
                    if self.board[i,j] == self.board[i+1,j]:
                        pairs += 1
            for i in range(self.board_height):
                for j in range(self.board_width-1):
                    if self.board[i,j] == self.board[i,j+1]:
                        pairs += 1
            if pairs == 0:
                self.done = True
                        
            
if __name__ == "__main__":
    tzfe = TZFE(5, 5)
    print(tzfe.board)
