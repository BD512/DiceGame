from tkinter import *
from tkinter import colorchooser

class ColourSelector(Frame): # a widget (inherits tkinter frame) which should sit in a toplevel settings menu for user to set a colour from
    def __init__(self, master:Toplevel, start_colour="#000000"):
        super().__init__(master)
        self.master = master
        ## setting up frame config:
        for c in range(0, 3): self.columnconfigure(c, weight=2-c%2)
        self.rowconfigure(0, weight=1)
        ## storing colour info
        self.colour = start_colour
        ## setting up the widgets in frame
        self.colour_name_label = Label(self, text=start_colour)
        self.colour_name_label.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.colour_label = Label(self, text="__", bg=start_colour, fg=self.colour)
        self.colour_label.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        Button(self, text="Change", command=self.changeColour).grid(row=0, column=2, sticky="nsew", padx=5, pady=5)

    def changeColour(self): # called by pressing the change colour button for the user to select a colour
        self.master.withdraw() # hides the window this widget is in before the colour selection window is opened
        colour = colorchooser.askcolor(title ="Choose colour")[1] # opens a built in tkinter colour selection window
        self.colour = colour if colour != None else self.colour
        # changes the labels for which colour has been chosen:
        self.colour_name_label["text"] = self.colour
        self.colour_label["bg"] = self.colour
        self.colour_label["fg"] = self.colour
        self.master.deiconify() # unhides the window behind the colour selection

    def getColour(self): # gets the colour which has been selected by the user
        return self.colour