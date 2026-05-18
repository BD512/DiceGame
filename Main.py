from LoginWidget import SelectUsers
from GameWidget import GamePlayWidget
from tkinter import Frame, Button, Tk, Label
from HomeWidget import HomeWidget
from Colour import Colour
from People import People

class WinnerFrame(Frame): # a class which inherits frame to create a widget to show the winner and a button to go to the next state
    def __init__(self, master, winning_player, next_func, colour1, colour2, font="arial"):
        super().__init__(master, bg=colour1)
        Label(self, text=f"{winning_player.getName()} won!!", bg=colour1, fg=Colour(colour1).getTextColour(), font=(font, 14)).pack(expand=True, fill="both")
        Button(self, text="Next", command=next_func, bg=colour2, fg=Colour(colour2).getTextColour()).pack(expand=True)

class Main(Tk): # the main game class - inherits Tk making it a window
    def __init__(self, colour1="#e6fff5", colour2="#33ffad"):
        super().__init__()
        self.configure(background=colour1) # sets the window background colour to colour 1
        self.minsize(500, 375) # sets the minimum size the window can be changed to
        self.maxsize(700, 500) # sets the maximum size the window can be changed to
        self.geometry('600x400') # sets the starting window size
        self.title("Dice Game!!") # sets the title of the window
        self.states = ["WELCOME", "LOGIN", "PLAYING"] # initialises what states the game can be in
        self.sound = True # sets the sound attribute which shows whether or not the sound should be played (True = sound will be played)
        self.current_state = self.states[0] # sets the current state to the first state which will be "WELCOME"
        self.home_button = Button(self, text="Home", command=self.goToWelcomeScreen, bg=colour2, fg=Colour(colour2).getTextColour()) # initialises the home button which can be pressed any time to return to the welcome state
        self.home_button.pack(fill="both")
        self.current_frame = Frame(self) # creates an object of Frame. Current frame stores the object of the current frame which is being displayed. Starts with an empty frame which will then be changed to welcome frame by calling goToWelcomeScreen method
        self.people = People("people.txt") # creates an object of people for the users to be stored in
        self.actions = {"WELCOME":self.goToWelcomeScreen,
                        "LOGIN":self.goToLoginScreen,
                        "PLAYING":self.goToPlayingScreen} # dictionary sets the methods to be called when going into each state
        self.colour1 = colour1 # sets attribute colour 1
        self.colour2 = colour2 # sets attribute colour 1
        self.user1 = None # sets an attribute which will store user 1 when playing
        self.user2 = None # sets an attribute which will store user 2 when playing
        self.goToWelcomeScreen() # calls function to go to the first welcome screen

    def getNextState(self): # returns the next state to go to (next state is next in list)
        return self.states[(self.states.index(self.current_state) + 1) % len(self.states)]

    def nextState(self): # calls the method to start the next state
        self.current_state = self.getNextState()
        self.actions[self.current_state]()

    def goToWelcomeScreen(self): # goes to the welcome screen state
        self.current_frame.destroy()
        self.current_frame = HomeWidget(self, alter_settings_func=self.changeSettings, new_game_func=self.nextState, people=self.people, colour1=self.colour1, colour2=self.colour2)
        self.current_frame.pack(expand=True, fill="both")
        self.current_state = "WELCOME"

    def changeSettings(self, colour1, colour2, sound): # changes the setting to the parameter passed in
        self.colour1 = colour1
        self.colour2 = colour2
        self.sound = sound
        self.home_button.config(bg=colour2, fg=Colour(colour2).getTextColour())

    def goToLoginScreen(self): # goes to the state showing the login screen
        self.current_frame.destroy()
        self.current_frame = SelectUsers(self, self.people, self.finishLoggingIn, self.colour1, self.colour2)
        self.current_frame.pack(expand=True, fill="both")
        self.current_state = "LOGIN"

    def finishLoggingIn(self, user1, user2): # goes to the state after finished logging in and sets the users to the ones logged in as
        self.user1 = user1
        self.user2 = user2
        self.nextState()

    def goToPlayingScreen(self): # goes to the state showing the main game playing screen
        self.current_frame.destroy()
        self.current_frame = GamePlayWidget(self, self.user1, self.user2, self.finishPlaying, self.colour1, self.colour2, sound_on=self.sound)
        self.current_frame.pack(expand=True, fill="both")
        self.current_state = "PLAYING"

    def finishPlaying(self, winner): # goes to the state after finished playing the game and stores the scores
        self.people.writeToFile()
        self.current_frame.destroy()
        self.current_frame = WinnerFrame(self, winner, self.nextState, self.colour1, self.colour2)
        self.current_frame.pack(expand=True, fill="both")

Main().mainloop()