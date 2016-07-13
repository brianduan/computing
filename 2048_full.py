"""
Clone of 2048 game.
"""

import random


# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}


def appendlist(temp_list,temp_list2,direction):
    """
    Function that append rows/cols (stored in temp_list2) to a temp_list 
    """
    if direction == UP or direction == LEFT:
        temp_list.append(merge(temp_list2))
    if direction == DOWN or direction == RIGHT:
        mergelist = merge(temp_list2)
        mergelist.reverse()
        temp_list.append(mergelist)



def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    if len(line) == 1:
        return line
    
    num0 = line.count(0)
    
    newline = [n for n in line if n != 0]
    newline.extend(num0*[0])

    newline2 = []
    index=0
   
    while index < len(line):
        if newline[index]==newline[index+1]:
            newline2.append(newline[index]*2) 
            if index+2 == len(line)-1:
                #this determines if the next index
                #is the last index
                newline2.append(newline[-1]) 
                break
            else:
                index += 2
        else:
            newline2.append(newline[index])
            if index+1 == len(line)-1:
                #this determines if the next index
                #is the last index
                newline2.append(newline[-1]) 
                break
            else:
                index += 1

    
    filler0 = len(line)-len(newline2)
    newline2.extend(filler0*[0])
    
    return newline2

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        # replace with your code
        
        self._grid_height = grid_height
        self._grid_width = grid_width
        self.reset()
        self._initial_tiles_up = [(0,x) for x in range(self._grid_width)]
        self._initial_tiles_down = [(self._grid_height-1,x) for x in range(self._grid_width)]
        self._initial_tiles_left = [(x,0) for x in range(self._grid_height)]
        self._initial_tiles_right = [(x,self._grid_width-1) for x in range(self._grid_height)]
        self._initial_tiles_dict = {UP:self._initial_tiles_up,DOWN:self._initial_tiles_down,
                                   LEFT:self._initial_tiles_left,RIGHT:self._initial_tiles_right}
        
    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        # replace with your code
        
        self._board = [[0 for dummy_i in range(self._grid_width)] for dummy_x in range(self._grid_height)]
        self.new_tile()
        self.new_tile()

        #return self.board 

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        return str(self._board)

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        # replace with your code
        return self._grid_height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        # replace with your code
        return self._grid_width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        # replace with your code
        
        #for eg: for a 4x4 board
        #For UP, initial tiles be: [(𝟶, 𝟶), (𝟶, 𝟷), (𝟶, 𝟸), (𝟶, 𝟹)]
        #offset is (1,0)
        
        #For DOWN, initial tiles be: [(3, 𝟶), (3, 𝟷), (3, 𝟸), (3, 𝟹)]
        #offset is (-1,0)
       
        #For RIGHT, initial tiles be: [(0, 3), (1, 3), (2, 3), (3, 𝟹)]
        #offset is (0,-1)        
        
        temp_list = []
        temp_list2 = []
        offset = OFFSETS[direction]
        initial_tiles = self._initial_tiles_dict[direction]
        
        
        for item in initial_tiles:
            temp_list2 = []
            if direction == UP or direction == DOWN:
                for index in range(self._grid_height):
                    temp_list2.append(self._board[item[0]+index*offset[0]]
                                       [item[1]+index*offset[1]] )
                
                appendlist(temp_list,temp_list2,direction)

                
                
                
            elif direction == LEFT or direction == RIGHT:
                for index in range(self._grid_width):
                    temp_list2.append(self._board[item[0]+index*offset[0]]
                                       [item[1]+index*offset[1]] )
                appendlist(temp_list,temp_list2,direction)
       
        
        has_moved = False 
        
        if direction == UP or direction == DOWN:
            for row in range(self._grid_height):
                for col in range(self._grid_width):
                    if self._board[row][col] != temp_list[col][row]:
                        has_moved = True
                    self._board[row][col] = temp_list[col][row]
            
        else:
            if self._board != temp_list: 
                has_moved = True
            self._board = temp_list
            
        
        if has_moved:
            self.new_tile()
        
        
           

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        
        ran_num= random.randrange(0, 10)
        if ran_num == 0:
            newtile = 4
        else:
            newtile = 2
        
        has_0 = False
        row_col_list = []
        
        for row in range(self._grid_height):
            for col in range(self._grid_width):
                if self._board[row][col] == 0:
                    has_0 = True
                    row_col_list.append([row,col])
                 
        if has_0:
            ran_num2 = random.randrange(0,len(row_col_list))
            ran_row_col = row_col_list[ran_num2]
            ran_row = ran_row_col[0]
            ran_col = ran_row_col[1]
            self._board[ran_row][ran_col] = newtile


            
    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._board[row][col] = value
        

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        # replace with your code
        return self._board[row][col]

#import user41_gdwzueO6OW_12 as poc_2048_testsuite
#poc_2048_testsuite.run_suite(TwentyFortyEight)

import poc_2048_gui
poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
