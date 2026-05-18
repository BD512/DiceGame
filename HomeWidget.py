from LeaderBoard import *
from ColourPicker import ColourSelector
from Colour import Colour
from tkinter import Message, Toplevel, BooleanVar, ttk, Button, Label

class InstructionsWin(Toplevel): # a child of tkinter toplevel, creating a popup window to show instructions
    def __init__(self, master, colour1, colour2, font):
        super().__init__(master, bg=colour1)
        self.title("Instructions") # sets window heading
        ## initialising widgets in the window
        Label(self, text="Instructions", bg=colour1, fg=Colour(colour1).getTextColour(), font=(font, 14, "bold")).pack()
        Message(self, text="Log in or create and account roll the dice on your turn you try and score as highly as possible. The winner is the player with the highest score at the end of 5 rolls - an additional roll is done if there is a tie. The winning player will then get their score recorded and the highest score recorded for each player is shown on the leaderboard.", font=(font, 12), bg=colour1, fg=Colour(colour1).getTextColour()).pack()
        Label(self, text="Scoring rules:", bg=colour1, fg=Colour(colour1).getTextColour(), font=(font, 14, "bold")).pack()
        Message(self,
                text="If total of the two dice rolled is odd: \n5 points are subtracted from current score.\nIf total of the two dice rolled is even: \n10 points are added to the total of the two dice. \nIf the two dice are the same: \nThe player gets an extra roll. ",
                font=(font, 12), bg=colour1, fg=Colour(colour1).getTextColour()).pack()
        Button(self, text="Ok", command=self.destroy, bg=colour2, fg=Colour(colour2).getTextColour()).pack() # button to close window when pressed

class SettingsMenu(Toplevel): #
    def __init__(self, master, feedback_func, colour1="#000000", colour2="#000000", font="Arial"):
        super().__init__(master)
        self.title("Settings")
        for col in range(0, 2): self.columnconfigure(col, weight=1)
        for row in range(0, 3): self.rowconfigure(row, weight=1)
        self.attributes('-topmost', True)
        self.feedback_func = feedback_func
        Label(self, text="Primary colour:", font=(font, 10)).grid(row=0, column=0, sticky="nsew")
        self.colour1_select = ColourSelector(self, colour1)
        self.colour1_select.grid(row=0, column=1, sticky="nsew")
        Label(self, text="Second colour:", font=(font, 10)).grid(row=1, column=0, sticky="nsew")
        self.colour2_select = ColourSelector(self, colour2)
        self.colour2_select.grid(row=1, column=1, sticky="nsew")
        Label(self, text="Sound on:").grid(row=2, column=0, sticky="nsew")
        self.sound_on = False
        self.sound_on_var = BooleanVar()
        self.sound_check = ttk.Checkbutton(self, variable=self.sound_on_var, command=self.changeSoundOn)
        self.sound_check.grid(row=2, column=1, sticky="nsew")
        Button(self, text="OK", command=self.submitSettings).grid(row=3, column=1, sticky="nsew")

    def getColour1(self):
        return self.colour1_select.getColour()

    def changeSoundOn(self):
        self.sound_on = not self.sound_on

    def getColour2(self):
        return self.colour2_select.getColour()

    def getSoundOn(self):
        return self.sound_on

    def submitSettings(self):
        self.feedback_func(self.getColour1(), self.getColour2(), self.getSoundOn())
        self.destroy()


class HomeWidget(Frame):
    def __init__(self, master, new_game_func, alter_settings_func, people, colour1="#000000", colour2="#000000", font="Arial"):
        super().__init__(master, bg=colour1)
        self.colour1 = colour1
        self.colour2 = colour2
        for col in range(0, 2): self.columnconfigure(col, weight=1)
        self.rowconfigure(0, weight=1)
        self.alter_settings_func = alter_settings_func
        self.side1_frame = Frame(self, bg=colour1)
        self.side1_frame.columnconfigure(0, weight=1)
        for row in range(0, 4): self.side1_frame.rowconfigure(row, weight=1)
        self.welcome_label = Label(self.side1_frame, text="Welcome!", bg=colour1, fg=Colour(colour1).getTextColour(), font=font)
        self.welcome_label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.new_game_button = Button(self.side1_frame, text="New game", command=new_game_func, bg=colour2, fg=Colour(colour2).getTextColour(), font=font)
        self.new_game_button.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.settings_button = Button(self.side1_frame, text="Settings", command=self.showSettings, bg=colour2, fg=Colour(colour2).getTextColour(), font=font)
        self.settings_button.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        self.info_button = Button(self.side1_frame, text="Instructions", command=self.showInstructions, bg=colour2, fg=Colour(colour2).getTextColour(), font=font)
        self.info_button.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")
        self.side1_frame.grid(row=0, column=0, sticky="nsew")
        self.leaderboard = LeaderBoardGui(self, people, height=10, width=100)
        self.leaderboard.grid(row=0, column=1, sticky="nsew")
        self.count = 0

    def showSettings(self):
        settings_win = SettingsMenu(self, self.enterSettings, colour1=self.colour1, colour2=self.colour2, font="Arial")
        settings_win.mainloop()

    def showInstructions(self):
        self.count += 1
        print(self.count)
        instructions_win = InstructionsWin(self, colour1=self.colour1, colour2=self.colour2, font="Arial")
        instructions_win.mainloop()

    def enterSettings(self, colour1, colour2, sound_on):
        self.changeColours(colour1, colour2)
        print(self.alter_settings_func)
        self.alter_settings_func(colour1, colour2, sound_on)

    def changeColours(self, colour1, colour2):
        self.colour1 = colour1
        self.colour2 = colour2
        self.new_game_button.config(bg=colour2, fg=Colour(colour2).getTextColour())
        self.settings_button.configure(bg=colour2, fg=Colour(colour2).getTextColour())
        self.info_button.configure(bg=colour2, fg=Colour(colour2).getTextColour())
        self.side1_frame.configure(bg=colour1)
        self.welcome_label.config(bg=colour1, fg=Colour(colour1).getTextColour())
        self.config(bg=colour1)
