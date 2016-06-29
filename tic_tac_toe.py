"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

"""myboard = provided.TTTBoard(3)
print myboard
print myboard.get_dim()
print myboard.get_empty_squares()
print myboard.square(0,1)
myboard.move(1,1,provided.PLAYERO)
print myboard
print myboard.check_win()
print myboard.clone() """

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 1         # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player
    
# Add your functions here.

def mc_trial(board,player):
    """
    This function takes a current board and the next player to move. 
    The function should play a game starting with the given player by making random moves, 
    alternating between players. The function should return when the game is over. 
    The modified board will contain the state of the game, so the function does not return anything. 
    In other words, the function should modify the board input.
    """
    #dimension = board.get_dim()
    #for dummy_i in range(NTRIALS):
    empty_squares = board.get_empty_squares()
    
    while len(empty_squares)>0 and board.check_win() == None:
        
        ran_index = random.randrange(len(empty_squares))
        row = empty_squares[ran_index][0]
        col = empty_squares[ran_index][1]
        
        board.move(row,col,player)
        
        player = provided.switch_player(player)  #caution
        empty_squares.pop(ran_index)
    


def update_score(scores, lst, increment):
    """
    This is a helper function used in mc_update_scores
    """
    for index_tuple in lst:   
        scores[index_tuple[0]][index_tuple[1]] += increment
    
    
    
def mc_update_scores(scores,board,player):
    """
    This function takes a grid of scores (a list of lists) with the same dimensions 
    as the Tic-Tac-Toe board, a board from a completed game, 
    and which player the machine player is. 
    The function should score the completed board and update the scores grid. 
    As the function updates the scores grid directly, it does not return anything,
    """
    dimension = board.get_dim()
    result = board.check_win()

    
    empty_list = board.get_empty_squares()
    win_list = []  #win as in the machine wins i.e. if player == result
    lose_list = []


    for dummy_x in range(dimension):
        for dummy_y in range(dimension):
            if board.square(dummy_x,dummy_y) == player:
                win_list.append((dummy_x,dummy_y))
            elif board.square(dummy_x,dummy_y) != provided.EMPTY:
                #print "detected"
                lose_list.append((dummy_x,dummy_y))
               
    #eg:win_list = [(0,1),(0,2),(1,1),(2,1)]
    #eg:win_list2 = [1,2,5,7]
    
    if result == player:

        update_score(scores,win_list,SCORE_CURRENT)
        update_score(scores,lose_list,-SCORE_OTHER)
        
        """
        for index_tuple in win_list:   
            scores[index_tuple[0]][index_tuple[1]] += SCORE_CURRENT
        for index_tuple in lose_list:
            scores[index_tuple[0]][index_tuple[1]] += -SCORE_OTHER
        """
        
    elif result != provided.DRAW: 
    
        update_score(scores,win_list,-SCORE_CURRENT)
        update_score(scores,lose_list, SCORE_OTHER)
        
        """
        for index_tuple in win_list:        
            scores[index_tuple[0]][index_tuple[1]] += -SCORE_CURRENT
        for index_tuple in lose_list:
            scores[index_tuple[0]][index_tuple[1]] += SCORE_OTHER
        """
    
    else:
        #It's a draw!
        
        update_score(scores,win_list, 0)
        update_score(scores,lose_list, 0)
        """
        for index_tuple in win_list:        
            scores[index_tuple[0]][index_tuple[1]] += 0
        for index_tuple in lose_list:
            scores[index_tuple[0]][index_tuple[1]] += 0        
        """
    
    for index_tuple in empty_list:
        scores[index_tuple[0]][index_tuple[1]] += 0
           

def get_best_move(board,scores):
    """
    This function takes a current board and a grid of scores. 
    The function should find all of the empty squares with the maximum score 
    and randomly return one of them as a (row,colume) tuple
    """
   
    score_loc_list = []
    score_list = []
    empty_list = board.get_empty_squares()
    
    if len(empty_list) == 0: 
        return None 
        
    for index_tuple in empty_list:
        score_list.append(scores[index_tuple[0]][index_tuple[1]])
    
    maximum = max(score_list)  
    
    for index_tuple in empty_list:
        if scores[index_tuple[0]][index_tuple[1]] == maximum:
            score_loc_list.append(index_tuple)
    
    ran_num = random.randrange(len(score_loc_list))
    best_move = score_loc_list[ran_num]
    
    return best_move


def mc_move(board,player,trials):
    """
    This function takes a current board, which player the machine player is, 
    and the number of trials to run. The function should use 
    the Monte Carlo simulation described above 
    to return a move for the machine player in the form of a (row,colume) tuple
    Be sure to use the other functions you have written!
    """
    
    dimension = board.get_dim()
    running_score = [[0]*dimension for dummy_n in range(dimension)] #caution
    scores = [[0]*dimension for dummy_n in range(dimension)]
    
    clone_board = board.clone()
    
    for dummy_i in range(trials):
        mc_trial(clone_board,player)
        mc_update_scores(scores,clone_board,player)
        for dummy_x in range(dimension):
            for dummy_y in range(dimension):
                running_score[dummy_x][dummy_y] += scores[dummy_x][dummy_y]
    
    (row,col) = get_best_move(board,running_score)

    return (row,col)
    


# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.

provided.play_game(mc_move, NTRIALS, False)        
poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
