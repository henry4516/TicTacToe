
import numpy as np
from typing import List, Dict, Tuple

### Size is a positive integer, which is the size of the game board (square).
### Game is the game board.

DEPTH_LIMIT = 10
X = 1
O = -1

def col_complete(game, size: int, col):
    """
    check if a column is complete. 1 if all X, -1 if all O, 0 otherwise.

    """
    temp = game[0, col]
    if temp == 0:
        return 0
    for x in range(size):
        if game[x, col] != temp:
            return 0
    return temp

def row_complete(game, size: int, row):
    temp = game[row, 0]
    if temp == 0:
        return 0
    for y in range(size):
        if game[row, y] != temp:
            return 0
    return temp

def rdia_complete(game, size: int):
    """
    check if right diagonal is complete.
    """
    temp = game[0, 0]
    if temp == 0:
        return 0
    for xy in range(size):
        if game[xy, xy] != temp:
            return 0
    return temp

def ldia_complete(game, size: int):
    temp = game[0, size - 1]
    if temp == 0:
        return 0
    for x in range(size):
        if game[x, size - 1 - x] != temp:
            return 0
    return temp

def game_complete(game, size: int):
    """
    returns 1 if X wins, -1 if O wins, 0 otherwise.
    // 0 if neither but bourd is full (tie), False if there exits any empty positions.

    """
    for x in range(size):
        ans = row_complete(game, size, x)
        if ans:
            return ans
    for y in range(size):
        ans = col_complete(game, size, y)
        if ans:
            return ans
    rdia = rdia_complete(game, size)
    if rdia:
        return rdia
    return ldia_complete(game, size)

def possible_moves(game, size):
    """
    returns the all positions that are empty, where we can place a piece on each of them.

    """
    """
    result = []
    for x in range(size):
        for y in range(size):
            if game[x, y] == 0:
                result.append(Coordinate(x, y))
    return result
    """
    return np.argwhere(game == 0)


class TTT:
    """
    tic-tac-toe game.

    """
    def __init__(self, size: int):
        assert size > 0, "invalid size"
        self.__size = size
        self.__game = np.zeros((size, size), dtype = np.int8)

    def __repr__(self):
        return str(self.__game)
    
    def size(self):
        return self.__size

    def empty_girds(self):
        return np.argwhere(self.__game == 0)
    
    def move(self, who: int, grid: Tuple[int]) -> bool:
        """
        Returns True if success, False otherwise.
        Requires: grid must be in game board.
        """
        if self.__game[grid]:
            return False
        else:
            self.__game[grid] = who
            return True
    def remove(self, grid: Tuple[int]) -> bool:
        """
        Removes piece at grid returning True if any, False otherwise.

        """
        if self.__game[grid] == 0:
            return False
        else:
            self.__game[grid] = 0
            return True

    def complete(self):
        return game_complete(self.__game, self.__size)
    
    def moves(self):
        """
        Returns all possible moves.

        """
        return possible_moves(self.__game, self.__size)
    
    def at(self, grid: Tuple[int]):
        """
        returns the piece at this grid. [1: X, -1: O, 0: nothing].

        """
        return self.__game[grid]

def AIplay(t: TTT, who: int, depth = 0) -> Tuple[Tuple[int], int]:
    """
    play ttt with AI. It will make the best move.
    Returns: (current best move, current best predicated final result [anyof (-1: O wins), (0: tie), (1: X wins)])

    """
    result = t.complete()
    if result:
        return None, result
    moves = t.moves()
    ### game board is full
    if len(moves) == 0:
        return None, 0
    ### X's turn
    if who == X:
        max_score = -float('inf')
        best_move = None
        for move in moves:
            t.move(X, tuple(move))
            score = AIplay(t, O, depth + 1)[1]
            #next_move, score = AIplay(t, O, depth + 1)
            t.remove(tuple(move))
            #max_score = max(max_score, score)
            if score > max_score:
                ### update current best score&move
                max_score = score
                best_move = move
        return tuple(best_move), max_score
    ### O's turn
    elif who == O:
        min_score = float('inf')
        best_move = None
        for move in moves:
            t.move(O, tuple(move))
            score = AIplay(t, X, depth + 1)[1]
            t.remove(tuple(move))
            if score < min_score:
                min_score = score
                best_move = move
        return tuple(best_move), min_score
    else:
        raise TypeError("not valid player")

"""
def beatAI(t: TTT, first = True) -> None:
    while len(t.moves()) != 0:
        if t.complete():
            s
"""

def AIfight(t:TTT, first = X) -> None:
    who = first
    while len(t.moves()) != 0:
        if who == X:
            print("X's move:")
            move = AIplay(t, X)[0]
            t.move(X, move)
            who = O
        elif who == O:
            print("O's move:")
            move = AIplay(t, O)[0]
            t.move(O, move)
            who = X
        else:
            raise TypeError("not valid player")
        print(t)
        result = t.complete()
        if result == X:
            print("X wins!")
            return
        elif result == O:
            print("O wins!")
            return
        else:
            continue
    print("They tied")
        

def play(t: TTT, players: int, first = bool):
    """
    Try defeat AI! players -> number of players.
    0 players: two AI beat each other.
    1 player: you beat AI.
    2 players: no AI involved.

    """