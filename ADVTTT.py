# an advanced version of TTT game data structure and AI algorithm.
import numpy as np
from typing import List, Tuple

DEPTH_LIMIT = 1000
X = 1
O = -1

def row_complete(board, size: int, row: int):
    '''
    Returns 1 if all X on row, -1 if all O on row, 0 if otherwise.
    '''
    temp = board[row, 0]
    if temp == 0:
        return 0
    for y in range(size):
        if board[row, y] != temp:
            return 0
    return temp

def col_complete(board, size: int, col: int):
    '''
    Returns 1 if all X on col, -1 if all O on col, 0 if otherwise.
    '''
    temp = board[0, col]
    if temp == 0:
        return 0
    for x in range(size):
        if board[x, col] != temp:
            return 0
    return temp

def rdia_complete(board, size: int):
    '''
    Returns 1 if all X on right diagonal, -1 if all O on right diagonal, 0 if otherwise.
    '''
    temp = board[0, 0]
    if temp == 0:
        return 0
    for i in range(size):
        if board[i, i] != temp:
            return 0
    return temp

def ldia_complete(board, size: int):
    '''
    Returns 1 if all X on left diagonal, -1 if all O on left diagonal, 0 if otherwise.
    '''
    temp = board[0, size - 1]
    if temp == 0:
        return 0
    for i in range(size):
        if board[i, size - 1 - i] != temp:
            return 0
    return temp

def game_complete(board, size: int):
    '''
    returns 1 if X wins, -1 if O wins, 0 otherwise.
    
    '''
    for i in range(size):
        col_result = col_complete(board, size, i)
        if col_result : return col_result 
        row_result = row_complete(board, size, i)
        if row_result : return row_result
    ldia_result = ldia_complete(board, size)
    if ldia_result : return ldia_result
    return rdia_complete(board, size)


class Game:
    def __init__(self, size: int):
        assert size > 0, "invalid size"
        self._size = size
        self._board = np.zeros((size, size), dtype = np.int8)

    def __repr__(self):
        return str(self._board)
    
    def _check_line(self, line):
        temp = line[0]
        for i in range(self._size):
            if line[i] != temp:
                return 0
        return temp

    def empty_grids(self):
        '''
        Returns all empty grids. Game stops if no empty grids.

        '''
        return np.argwhere(self._board == 0)
    
    def make_move(self, who: int, grid: Tuple[int]):
        assert who in (X, O), "not valid player"
        if self._board[grid]:
            return False
        else:
            self._board[grid] = who
            return True
        
    def remove(self, grid: Tuple[int]):
        if self._board[grid]:
            self._board[grid] = 0
            return True
        else:
            return False

    def complete(self):
        lines = np.concatenate((self._board, self._board.T, np.array([np.diag(self._board), np.diag(np.fliplr(self._board))])), axis=0)
        for line in lines:
            result = self._check_line(line)
            if result:
                return result
        return 0
    
    def at(self, grid: Tuple[int]):
        return self._board[grid]
    

def pruning(game: Game, player, depth_limit=DEPTH_LIMIT, alpha=float('-inf'), beta=float('inf'), depth=0):
    '''
    Pruning algorithm, efficient for small sized board games, e.g. 3x3.

    '''
    moves = game.empty_grids()
    # game over
    if len(moves) == 0:
        return None, game_complete(game._board, game._size) # result
    best_move = None

    # exceed depth limit
    if depth > DEPTH_LIMIT:
        return tuple(moves[0]), 0 # return a mild score, neither them two wins

    if player == X:
        # current largest score among all possible moves
        largest_score = float('-inf')
        for move in moves:
            move = tuple(move)
            game.make_move(player, move)
            _, score = pruning(game, O, largest_score, beta, depth + 1)
            game.remove(move)
            if score > largest_score:
                largest_score = score
                best_move = move
            if largest_score >= beta: # following outcomes will only result in a larger score, 
                # which will already not considered by beta, the min layer. pruning
                break
        return best_move, largest_score
    
    elif player == O:
        # current smallest score among all possible moves
        smallest_score = float('inf')
        for move in moves:
            move = tuple(move)
            game.make_move(player, move)
            _, score = pruning(game, X, alpha, smallest_score, depth + 1)
            game.remove(move)
            if score < smallest_score:
                smallest_score = score
                best_move = move
            if smallest_score <= alpha: # pruning
                break
        return best_move, smallest_score
    else:
        raise ValueError("not valid player")
    