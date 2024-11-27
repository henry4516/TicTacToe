### player/game info for tic tac toe.
import tic_tac_toe as ttt

class gameInfo:
    def __init__(self):
        self.__games = 0
        self.__Xwins = 0
        self.__Owins = 0
        self.__tie = 0
        self.__Xwinrate = 0
        self.__Owinrate = 0

    def __repr__(self):
        return f"Games: {self.__games}\n" + f"X: wins [{self.__Xwins}]\n" + f"O: wins [{self.__Owins}]\n" +\
                f"Tie: [{self.__tie}]\n" + f"X win rate: [{self.__Xwinrate:.1f}%]\n" + f"O win rate: [{self.__Owinrate:.1f}%]\n"
    
    def games(self):
        return self.__games
    
    def Xwins(self):
        return self.__Xwins
    
    def Owins(self):
        return self.__Owins
    
    def tie(self):
        return self.__tie

    def Xwinrate(self):
        return self.__Xwinrate
    
    def Owinrate(self):
        return self.__Owinrate

    def update(self, winner: int):
        self.__games += 1
        if winner == ttt.X:
            self.__Xwins += 1
        elif winner == ttt.O:
            self.__Owins += 1
        elif winner == 0:
            self.__tie += 1
        else:
            raise TypeError("invalid player")
        self.__Xwinrate = self.__Xwins / self.__games * 100
        self.__Owinrate = self.__Owins / self.__games * 100

"""
class roundsInfo:
    def __init__(self):
        self.__rounds = 0
"""