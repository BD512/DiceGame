from tkinter import *
from tkinter import ttk
from People import *
from Colour import *

class LoginWidget(Frame): # a class which inherits frame to create a widget for the user to enter their details to log in
    def __init__(self, master, people, colour):
        super().__init__(master, bg=colour)
        self.people = people # attribute storing the object of People which stores the users which could log in
        self.colour = colour # attribute storing the main colour of this widget
        ## Initialising the GUI widgets:
        Label(self, text="Enter details", bg=colour, fg=Colour(colour).getTextColour()).grid(row=0, column=0)
        Label(self, text="Username", bg=colour, fg=Colour(colour).getTextColour()).grid(row=1, column=0)
        self.username_entry = Entry(self)
        self.username_entry.grid(row=1, column=1)
        Label(self, text="Password", bg=colour, fg=Colour(colour).getTextColour()).grid(row=2, column=0)
        self.password_entry = Entry(self, show='*')
        self.password_entry.grid(row=2, column=1)
        self.feedback_label = Label(self, bg=colour)
        self.feedback_label.grid(row=3, column=1)

    def getPassword(self) -> str: # returns the password the user entered from the entry box
        return self.password_entry.get()

    def getUsername(self) -> str: # returns the username the user entered from the entry box
        return self.username_entry.get()

    def showIncorrectDetailsError(self) -> None: # displays a message if the details entered are incorrect
        self.feedback_label.config(text="Incorrect login details", fg=("#ffe6e6" if Colour(self.colour).getTextColour() == "white" else "#b30000"))

    def showLoggedIn(self, person:Person): # displays a message to show a user has logged in
        self.feedback_label.config(text=f"Logged in {person.getName()}", fg=("#e6ffe6" if Colour(self.colour).getTextColour() == "white" else "#00cc00"))

    def disableEntryBoxes(self): # disables the entry boxes so the user can no longer type in them
        self.username_entry.configure(state="disabled", disabledbackground="light gray")
        self.password_entry.configure(state="disabled", disabledbackground="light gray")

    def enableEntryBoxes(self): # enables the entry boxes so the user can type in them
        self.username_entry.configure(state="normal", disabledbackground="white")
        self.password_entry.configure(state="normal", disabledbackground="white")

    def submitDetails(self): # submits the details the user has entered
        person = self.people.findNameAndPasswordMatch(self.getUsername(), self.getPassword())
        if person is None:
            self.showIncorrectDetailsError()
            return False, None
        else:
            self.showLoggedIn(person)
            return True, person



class CreateUserWidget(Frame): #
    def __init__(self, master, people, colour):
        super().__init__(master, bg=colour)
        self.people = people
        self.colour = colour
        Label(self, text="Enter details", bg=colour, fg=Colour(colour).getTextColour()).grid(row=0, column=0)
        Label(self, text="Username", bg=colour, fg=Colour(colour).getTextColour()).grid(row=1, column=0)
        self.username_entry = Entry(self)
        self.username_entry.grid(row=1, column=1)
        Label(self, text="Password", bg=colour, fg=Colour(colour).getTextColour()).grid(row=2, column=0)
        self.password_entry = Entry(self, show='*')
        self.password_entry.grid(row=2, column=1)
        Label(self, text="Confirm password", bg=colour, fg=Colour(colour).getTextColour()).grid(row=3, column=0)
        self.password_confirmation_entry = Entry(self, show='*')
        self.password_confirmation_entry.grid(row=3, column=1)
        self.feedback_label = Label(self, bg=colour)
        self.feedback_label.grid(row=4, column=1)

    def getUsername(self) -> str:
        return self.username_entry.get()

    def getPassword(self) -> str:
        return self.password_entry.get()

    def getConfirmationPassword(self) -> str:
        return self.password_confirmation_entry.get()

    def showUserAlreadyExistsError(self) -> None:
        self.feedback_label.config(text="Username taken", fg=("#ffe6e6" if Colour(self.colour).getTextColour() == "white" else "#b30000"))

    def showPasswordsDontMatchError(self):
        self.feedback_label.config(text="Passwords don't match", fg=("#ffe6e6" if Colour(self.colour).getTextColour() == "white" else "#b30000"))

    def showUserCreated(self):
        self.feedback_label.config(text="Account created", fg=("#e6ffe6" if Colour(self.colour).getTextColour() == "white" else "#00cc00"))

    def doPasswordsMatch(self) -> bool:
        return self.getPassword() == self.getConfirmationPassword()

    def showNoUsernameEnteredError(self):
        self.feedback_label.config(text="Enter username", fg=("#ffe6e6" if Colour(self.colour).getTextColour() == "white" else "#b30000"))

    def showPasswordNotLongEnoughError(self):
        self.feedback_label.config(text="Enter longer password", fg=("#ffe6e6" if Colour(self.colour).getTextColour() == "white" else "#b30000"))

    def submitDetails(self):
        username = self.getUsername()
        password = self.getPassword()
        if not self.doPasswordsMatch():
            self.showPasswordsDontMatchError()
            return False, None
        elif self.people.doesPersonExist(username):
            self.showUserAlreadyExistsError()
            return False, None
        elif len(username) == 0:
            self.showNoUsernameEnteredError()
            return False, None
        elif len(password) <= 2:
            self.showPasswordNotLongEnoughError()
            return False, None
        else:
            self.showUserCreated()
            person = Person(username, password)
            return True, person

    def enableEntryBoxes(self):
        self.username_entry.configure(state="normal", disabledbackground="white")
        self.password_entry.configure(state="normal", disabledbackground="white")
        self.password_confirmation_entry.configure(state="normal", disabledbackground="white")

    def disableEntryBoxes(self):
        self.username_entry.configure(state="disabled", disabledbackground="light gray")
        self.password_entry.configure(state="disabled", disabledbackground="light gray")
        self.password_confirmation_entry.configure(state="disabled", disabledbackground="light gray")


class TabbedAuthOptions(ttk.Notebook):
    def  __init__(self, master, people, colour1, colour2):
        super().__init__(master)
        style = ttk.Style()
        style.theme_use("default")
        style.configure("TNotebook", background=colour1)
        style.configure("TNotebook.Tab", background=colour1, foreground=Colour(colour1).getTextColour())
        style.map("TNotebook.Tab", background=[("selected", colour2)], foreground=[("selected", Colour(colour2  ).getTextColour())])
        self.current_selected = "LOGIN"
        self.create_user_frame = CreateUserWidget(self, people, colour=colour2)
        self.login_frame = LoginWidget(self, people, colour=colour2)
        self.selection_options = {"Login":("LOGIN", self.login_frame), "Register":("REGISTER", self.create_user_frame)}
        self.add(self.login_frame, text="Login")
        self.add(self.create_user_frame, text="Register")
        self.bind("<<NotebookTabChanged>>", self.changeSelected)

    def changeSelected(self, event) -> None:
        notebook = event.widget
        tab_id = notebook.select()
        tab_text = notebook.tab(tab_id, 'text')
        self.current_selected = tab_text # self.selection_options[tab_text][0]

    def getEntryType(self) -> str:
        return self.selection_options[self.current_selected][0]

    def getCurrentFrame(self) -> Frame:
       return self.selection_options[self.current_selected][1]

    def disableAllEntries(self) -> None:
        self.create_user_frame.disableEntryBoxes()
        self.login_frame.disableEntryBoxes()

    def enableAllEntries(self) -> None:
        self.create_user_frame.enableEntryBoxes()
        self.login_frame.enableEntryBoxes()

class UserSelectionWidget(Frame):
    def __init__(self, master, number, people, colour1, colour2):
        super().__init__(master, bg=colour1)
        self.people = people
        self.person_found = False
        self.current_person = None
        self.user_already_exists = True
        Label(self, text=f"Player {number}:", bg=colour1, fg=Colour(colour1).getTextColour()).grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.user_selection = TabbedAuthOptions(self, people, colour1=colour1, colour2=colour2)
        self.user_selection.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.enter_button = Button(self, text="Enter", command=self.enter, bg=colour2, fg=Colour(colour2).getTextColour())
        self.enter_button.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")

    def enter(self):
        entry_frame = self.user_selection.getCurrentFrame()
        are_valid, person = entry_frame.submitDetails()
        if are_valid:
            self.current_person = person
            self.enter_button.config(text="Edit", command=self.enableEdit)
            self.user_selection.disableAllEntries()
        if self.user_selection.getEntryType() == "REGISTER": self.user_already_exists = False
        self.person_found = are_valid

    def enableEdit(self):
        self.person_found = False
        self.current_person = None
        self.user_already_exists = True
        self.user_selection.enableAllEntries()
        self.enter_button.config(text="Enter", command=self.enter)

    def finalSubmission(self):
        if not self.user_already_exists:
            self.people.addPerson(self.current_person)

    def getPerson(self):
        return self.current_person


class SelectUsers(Frame):
    def __init__(self, master, people, feedback_function, colour1, colour2, font="arial"):
        super().__init__(master, height=master.winfo_height(), width=master.winfo_width(), bg=colour1)
        self.people = people
        self.feedback_function = feedback_function
        self.user1 = None
        self.user2 = None
        Label(self, text="Select Users:", bg=colour1, fg=Colour(colour1).getTextColour(), font=(font, 14)).place(in_=self, relx=0.5, rely=0.05, x=0.5, y=.5, anchor="n")
        self.user1_selection = UserSelectionWidget(self, 1, people, colour1=colour1, colour2=colour2)
        self.user1_selection.place(in_=self, relx=0.48, rely=0.5, x=0.5, y=0.5, anchor="e")
        self.user2_selection = UserSelectionWidget(self, 2, people, colour1=colour1, colour2=colour2)
        self.user2_selection.place(in_=self, relx=0.52, rely=0.5, x=0.5, y=0, anchor="w")
        Label(self, text="VS", bg=colour1, fg=Colour(colour1).getTextColour()).place(in_=self, relx=0.5, rely=0.5, x=0.5, y=0, anchor="center")
        self.feedback_label = Label(self, bg=colour1, fg=Colour(colour1).getTextColour())
        self.feedback_label.place(in_=self, relx=0.5, rely=0.85, x=0.5, y=0, anchor="s")
        Button(self, text="Ok", command=self.enter, bg=colour2, fg=Colour(colour2).getTextColour()).place(in_=self, relx=0.5, rely=0.95, x=0.5, y=0, anchor="s")

    def enter(self):
        user1 = self.user1_selection.getPerson()
        user2 = self.user2_selection.getPerson()
        if user1 is None or user2 is None:
            self.feedback_label.config(text="Please log in or create an account for each player")
        elif user1 == user2:
            self.feedback_label.config(text="Users can't be the same")
        else:
            self.user1_selection.finalSubmission()
            self.user2_selection.finalSubmission()
            self.user1 = self.user1_selection.getPerson()
            self.user2 = self.user2_selection.getPerson()
            self.feedback_function(self.user1, self.user2)

    def getUser1(self):
        return self.user1

    def getUser2(self):
        return self.user2
