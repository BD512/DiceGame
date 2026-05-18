import random
from People import *

class Game: # a class to store what's going on in the background of the game being played - controls the scoring, storing the scores and what scores are rolled
    def __init__(self, player1=None, player2=None):
        self.player1:Person = player1 # attribute storing the object of the player 1
        self.player2:Person = player2 # attribute storing the object of the player 2
        self.player1.resetCurrentScore() # resets the current (score for this game) of player 1
        self.player2.resetCurrentScore() # resets the current (score for this game) of player 2
        self.current_score:int = 0 # sets the current score (score of the current player to 0) will currently be score of first player
        self.current_player:Person = self.player1 # attribute storing the object of the current player
        self.roll_number:int = 1 # the current roll number

    def rollNextNumber(self) -> tuple[int, int, bool]: # generates a random number for dice 1 and dice 2 to be rolled on, calculates the score from this, stores this in current score and returns the two scores and if they are equal
        self.current_score = 0
        if self.current_player == self.player2: self.roll_number += 1
        dice1 = random.randint(1, 6)
        dice2 = random.randint(1, 6)
        self.current_score, are_equal = self.calculateScore(dice1, dice2)
        self.current_player.addToCurrentScore(self.current_score)
        if not are_equal: self.current_player = self.player2 if self.current_player == self.player1 else self.player1
        return dice1, dice2, are_equal

    def rollSecondRoll(self) -> int: # rolls a second dice for if the dice were equal, adds this to current score and returns the roll score
        roll = random.randint(1, 6)
        self.current_player.addToCurrentScore(roll)
        self.current_score += roll
        self.current_player = self.player2 if self.current_player == self.player1 else self.player1
        return roll

    def updateHighScores(self) -> None: # calls Player object method so the high scores are compared and updated from current game score
        self.player1.updateHighscore()
        self.player2.updateHighscore()

    @staticmethod
    def calculateScore(dice1, dice2) -> tuple[int, bool]: # calculates the score of two dice rolled and whether another roll is required
        total = dice1 + dice2
        if total % 2 == 0:
            total += 10
        else:
            total -= 5
        return total, dice1 == dice2

    def getCurrentPlayer(self) -> Person: # gets the current person playing
        return self.current_player

    def getCurrentScore(self) -> int: # gets the current score
        return self.current_score

    def getRollNumber(self) -> int: # returns the count of roll number
        return self.roll_number

    def arePlayerScoresEqual(self) -> bool:  # returns a boolean of whether the player scores are equal
        return self.player1.getCurrentScore() == self.player2.getCurrentScore()

    def isFinished(self) -> bool: # checks whether the game is finished (5 rolls per player and player scores not equal)
        if self.current_player == self.player2:
            return False
        elif self.getRollNumber() <= 5:
            return False
        elif self.arePlayerScoresEqual():
            return False
        else:
            return True

    def endGame(self) -> None: # ends the game by updating the high score of the winner to be max(current score, high score)
        self.getWinner().updateHighscore()

    def getWinner(self) -> Person: # returns the highest scoring person
        return self.player1 if self.player1.getCurrentScore() > self.player2.getCurrentScore() else self.player2