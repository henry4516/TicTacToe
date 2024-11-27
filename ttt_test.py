### test files for tic_tac_toe.py
from tic_tac_toe import *
game = TTT(3)
print(game)
print(game.complete())
move12 = game.move(X, (1, 2))
print(move12, game)
move12 = game.move(O, (1, 2))
print(move12, game)
remove12 = game.remove((1, 2))
print(remove12, game)
"""
game.move(X, (0, 0))
game.move(X, (1, 1))
game.move(X, (2, 2))
print(game.complete(), game)
"""

print("now AI would play: ", AIplay(game, X))
#game.move(X, AIplay(game, X)[0])
#print(game)
newgame = TTT(3)
AIfight(newgame)