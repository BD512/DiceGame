from tkinter import *
from tkinter import ttk
from People import *

class LeaderBoardGui(ttk.Treeview): # class inherits treeview to create a leaderboard listbox-type GUI widget
    def __init__(self, master, people, width=100, height=5):
        super().__init__(master, show="headings", columns=("c1", "c2", "c3"), height=height)
        ## initialises the treeview columns
        self.column("c1", stretch=NO, minwidth=10, width=int(width/5))
        self.column("c2", minwidth=70, width=int(width/5)*3)
        self.heading("c2", text="Name")
        self.column("c3",minwidth=50, width=int(width/5)*2)
        self.heading("c3", text="Score")
        ## sets an attribute of people the leaderboard will show:
        self.people = people
        self.showPeople() # puts the people on the leaderboard

    def showPeople(self): # adds the information for each person to each column of the leaderboard as a row
        count = 1
        for person in self.people.getOrderedByScore():
            self.insert('', "end",
                        values=(count, person.getName(), person.getHighScore()))
            count += 1

    def clear(self): # clears the leaderboard
        for item in self.get_children():
            self.delete(item)

    def updatePeople(self): # updates the leaderboard for potentially new scores
        self.clear()
        self.showPeople()

    def showNewPeople(self, people): # updates the leaderboard with a new People object
        self.people = people
        self.updatePeople()