import pickle

class PickleFile: # a class to manage the pickle file (did this incase I wanted to easily change it from no longer being a pickle file)
    def __init__(self, filename: str):
        self.filename = filename

    def getContentsList(self) -> list: # loads data from the pickle file and returns as list
        try:
            res = pickle.load(open(self.filename, "rb"))
            return res
        except FileNotFoundError:
            return []

    def writeNewList(self, l: list) -> None: # writes a new list to pickle file
        pickle.dump(l, open(self.filename, "wb"))


class Person: # a person class which stores and manages information about a person
    def __init__(self, name: str, password: str, score:int=0):
        ## attributes storing person info
        self.name = name
        self.password = password
        self.highscore = score
        self.current_score = 0

    def comparePassword(self, pwd: str) -> bool:
        return pwd == self.password

    def compareName(self, name: str) -> bool:
        return name == self.name

    def compareNameAndPassword(self, name, pwd) -> bool:
        return self.compareName(name) and self.comparePassword(pwd)

    def getHighScore(self) -> int:
        return self.highscore

    def getCurrentScore(self) -> int:
        return self.current_score

    def getName(self) -> str:
        return self.name

    def addToCurrentScore(self, amount) -> None:
        self.current_score += amount
        self.current_score = max(0, self.current_score)

    def updateHighscore(self) -> None:
        self.highscore = max(self.highscore, self.current_score)

    def resetCurrentScore(self) -> None:
        self.current_score = 0


class People(list): # a child of list (python data type) which stores a list of Person objects
    def __init__(self, filename: str):
        super().__init__()
        self.filename = filename
        self.file = PickleFile(filename)
        self.readFromFile()
        # self.extend(people)
        self.writeToFile()

    def addNewPerson(self, name, password, score=0) -> Person: # creates person from info taken in as parameters and adds it to list of people
        person = Person(name, password, score)
        self.append(person)
        return person

    def addPerson(self, person): # adds Person object to list of people
        self.append(person)
        self.writeToFile()

    def findNameAndPasswordMatch(self, name, password) -> Person: # check if someone matching name and password exists in object and returns the person if so
        for person in self:
            if person.compareNameAndPassword(name, password):
                return person
        return None

    def doesPersonExist(self, name: str) -> bool: # checks if person exists from name
        for person in self:
            if person.compareName(name):
                return True
        return False

    def readFromFile(self) -> None: # reads info from file into object
        self.clear()
        for person_record in self.file.getContentsList():
            self.append(person_record)

    def writeToFile(self) -> None: # writes list of people to file
        self.file.writeNewList(self)

    def getOrderedByScore(self) -> list:  # returns people list based on scores in descending order
        return sorted(self, key=lambda person:person.getHighScore(), reverse=True)

    def getTopFiveScorers(self) -> list:  # returns top 5 scorers in descending order of highscore
        ordered_list = self.getOrderedByScore()
        return ordered_list[0:max(5, len(ordered_list))]