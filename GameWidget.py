from DiceAnimation import Dice
from tkinter.ttk import *
from tkinter import *
from Game import Game
from Colour import Colour
from SoundPlayer import SoundPlayer

class MultipleDice(Frame): # a class which inherits frame. Creates a widget showing any number of dice side by side
    def __init__(self, master, number_of_dice, colour1="white", colour2="black", sound_on=True):
        super().__init__(master, bg=colour1, borderwidth=0)
        self.play_sound = sound_on # stores whether sound should be played as the dice is rolled
        self.sound = SoundPlayer("Dice.mp4") # creates an object of SoundPlayer which can be used to play the audio file
        self.dice: list[Dice] = [] # a list which will store all the dice in the frame
        self.colour1 = colour1 # attribute stores colour1
        self.colour2 = colour2 # attribute stores colour2
        self.__createDice(number_of_dice) # creates the number of dice taken in as a parameter in self frame

    def changeNumberOfDice(self, new_number_of_dice) -> None: # changes the number of dice in the frame
        # clears frame of previous dice
        self.dice.clear()
        self.clearFrame()
        self.__createDice(new_number_of_dice) # creates dice of new number

    def clearFrame(self) -> None: # clears the frame the dice are in
        for child in self.winfo_children(): # goes through all the children objects in the frame and destroys the children
            child.destroy()

    def __createDice(self, number_of_dice) -> None: # draws however many dice taken in as parameter in frame
        for dice_number in range(number_of_dice):
            current_dice = Dice(self, dice_number, face_colour=self.colour2, background_colour=self.colour1)
            self.dice.append(current_dice)
            current_dice.grid(row=0, column=dice_number)

    def getNumberOfDice(self) -> int: # returns number of dice currently displayed
        return len(self.dice)

    def rollADice(self, dice_index: int, end_number: int, end_function) -> None: # rolls the dice at the index position, passing in the number is should roll to and the function/method it should call when finished
        if self.play_sound: self.sound.playSoundUntilStopped()
        if dice_index >= self.getNumberOfDice(): raise IndexError("The index of the dice should be below or the number of dice")
        self.dice[dice_index].rotateRandomlyToNumber(end_number, lambda:self.endRoll(end_function))

    def endRoll(self, end_function) -> None: # called when dice in frame has finished rolling
        end_function() # calls the method/ function to finish the dice roll
        if self.play_sound: self.sound.stopSound() # stops playing the sound

class UserScoreWidget(Frame): # class which has inherited frame to create a widget displaying a users name, score and highscore
    def __init__(self, master, user, bg="white", fg="black"):
        super().__init__(master, bg=bg)
        self.user = user # the user the widget will show info about
        ## creates the widgets in the frame:
        Label(self, text="Name:", bg=bg, fg=fg).grid(row=0, column=0)
        self.name_label = Label(self, text=user.getName(), bg=bg, fg=fg)
        self.name_label.grid(row=0, column=1)
        Label(self, text="Score:", bg=bg, fg=fg).grid(row=1, column=0)
        self.score_label = Label(self, text="0", bg=bg, fg=fg)
        self.score_label.grid(row=1, column=1)
        Label(self, text="Highscore:", bg=bg, fg=fg).grid(row=2, column=0)
        self.highscore_label = Label(self, text=user.getHighScore(), bg=bg, fg=fg)
        self.highscore_label.grid(row=2, column=1)

    def changeUser(self, user): # changes the user who the user is showing info about
        self.user = user
        self.name_label["text"] = self.user.getName()
        self.score_label["text"] = self.user.getHighScore()
        self.highscore_label["text"] = self.user.getHighscore()

    def updateScoreLabels(self): # updates the score label to show new score
        self.score_label["text"] = self.user.getCurrentScore()

class GamePlayWidget(Frame): # A class which inherits frame, creating a widget showing main game play
    def __init__(self, master, user1, user2, finished_function, colour1="#330066", colour2="#d9b3ff", font="Arial", sound_on=True):
        super().__init__(master, bg=colour1)
        ### Initialise the window configuration
        self.config(width=500, height=400)
        self.pack_propagate(False)
        ### create new game object
        self.game = Game(user1, user2)
        self.finished_function = finished_function
        ### set attributes to keep track of what is happening currently
        self.states_commands = {"FIRST ROLL":self.rollDice, "FINISH ROLL TO SECOND ROLL":self.finishToSecondRoll, "TO SECOND ROLL":self.changeToSecondRoll, "SECOND ROLL":self.rollSecondDice, "TO FIRST ROLL":self.resetToNewFirstRoll, "FINISH TURN":self.finishPlayerTurn}
        self.current_state = "FIRST ROLL"
        self.dice_finished_rolling = 2
        self.current_number_of_dice = 2
        self.sound = sound_on
        ### Initialise the GUI
        self.user1_info_widget = UserScoreWidget(self, user1, bg=colour1, fg=Colour(colour1).getTextColour())
        self.user2_info_widget = UserScoreWidget(self, user2, bg=colour1, fg=Colour(colour1).getTextColour())
        self.user1_info_widget.place(in_=self, relx=0.03, rely=0.03, x=0.5, y=0.5, anchor="nw")
        self.user2_info_widget.place(in_=self, relx=0.97, rely=0.03, x=0.5, y=0.5, anchor="ne")
        self.info_label = Label(self, text=f"{self.game.getCurrentPlayer().getName()}'s turn", font=(font, 15), bg=colour1, fg=Colour(
            colour1).getTextColour())
        self.info_label.place(in_=self, relx=.5, rely=0.03, x=0.5, y=0.5, anchor="n")
        self.current_score_label = Label(self, text="Score: 0", font=(font, 10), bg=colour1, fg=Colour(
            colour1).getTextColour())
        self.current_score_label.place(in_=self, relx=.5, rely=0.1, x=0.5, y=0.5, anchor="n")
        self.roll_number_label = Label(self, text="Roll number: 1", font=(font, 10), bg=colour1, fg=Colour(colour1).getTextColour())
        self.roll_number_label.place(in_=self, relx=0.5, rely=0.15, x=0.5, y=0.5, anchor="n")
        self.dice = MultipleDice(self, 2, colour1=colour1, colour2=colour2, sound_on=self.sound)
        self.dice.place(in_=self, relx=.5, rely=0.5, x=0.5, y=0.5, anchor="center")
        self.roll_button = Button(self, text="Roll!", command=self.performNextAction, bg=colour2, fg=Colour(
            colour2).getTextColour())
        self.roll_button.place(in_=self, relx=0.5, rely=0.9, x=0.5, y=0, anchor="s")
        self.feedback_label = Label(self, text="Roll", font=(font, 12), bg=colour1, fg=Colour(colour1).getTextColour())
        self.feedback_label.place(in_=self, relx=0.5, rely=1, x=0.5, y=0, anchor="s")

    def performNextAction(self): # performs the action which is stored to be done next
        self.states_commands[self.current_state]()

    def rollDice(self): # rolls the dice when there are two dice - shows them rolling and updates the user score
        print("FIRST ROLL DICE")
        dice1_roll, dice2_roll, additional_roll = self.game.rollNextNumber()
        self.roll_button["state"] = "disabled"
        self.feedback_label["text"] = "Rolling...."
        self.dice_finished_rolling = 0
        self.dice.rollADice(0, dice1_roll, self.performNextAction)
        self.dice.rollADice(1, dice2_roll, self.performNextAction)
        if additional_roll:
            self.current_state = "FINISH ROLL TO SECOND ROLL"
        else:
            self.current_state = "FINISH TURN"

    def finishToSecondRoll(self): # called at the end of a second single dice roll to show score
        print("FINISH ROLL TO SECOND ROLL")
        self.dice_finished_rolling += 1
        if self.dice_finished_rolling == self.current_number_of_dice:
            self.roll_button["state"] = "normal"
            self.current_score_label["text"] = f"Total:{self.game.getCurrentScore()}"
            self.feedback_label["text"] = "You rolled a double - roll again"
            self.roll_button["text"] = "Next"
            self.current_state = "TO SECOND ROLL"

    def finishPlayerTurn(self): # finishes a players turn, showing their score
        print("FINISH TURN")
        self.dice_finished_rolling += 1
        if self.dice_finished_rolling == self.current_number_of_dice:
            self.user1_info_widget.updateScoreLabels()
            self.user2_info_widget.updateScoreLabels()
            self.roll_button["state"] = "normal"
            self.current_score_label["text"] = f"Total:{self.game.getCurrentScore()}"
            self.feedback_label["text"] = f"You scored {self.game.getCurrentScore()}"
            self.roll_button.config(text="Next")
            self.current_state = "TO FIRST ROLL"

    def resetToNewFirstRoll(self): # resets to a 2 dice roll for the next player to roll after checking whether the game has finished
        print("TO FIRST ROLL")
        if self.game.isFinished():
            self.game.endGame()
            self.finished_function(self.game.getWinner())
        else:
            self.roll_number_label["text"] = f"Roll number:{self.game.getRollNumber()}"
            self.resetRollingBoard()

    def resetRollingBoard(self): # resets the screen for the next players roll
        self.info_label["text"]  = f"{self.game.getCurrentPlayer().getName()}'s turn"
        if self.current_number_of_dice == 1:
            self.dice.changeNumberOfDice(2)
        self.current_number_of_dice = 2
        self.roll_button["state"] = "normal"
        self.current_score_label["text"] = f"Total:0"
        self.feedback_label["text"] = "Roll dice"
        self.roll_button["text"] = "Roll"
        self.current_state = "FIRST ROLL"

    def changeToSecondRoll(self): # goes to the screen showing the second single dice to be rolled if double rolled
        print("TO SECOND ROLL")
        self.current_number_of_dice = 1
        self.dice.changeNumberOfDice(1)
        self.roll_button["state"] = "normal"
        self.feedback_label["text"] = "Roll dice"
        self.roll_button["text"] = "Roll"
        self.current_state = "SECOND ROLL"

    def rollSecondDice(self): # rolls the second single dice
        print("SECOND ROLL")
        self.dice_finished_rolling = 0
        dice_roll = self.game.rollSecondRoll()
        self.roll_button["state"] = "disabled"
        self.feedback_label["text"] = "Rolling...."
        self.dice.rollADice(0, dice_roll, self.performNextAction)
        self.current_state = "FINISH TURN"