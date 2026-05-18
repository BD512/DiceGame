from Matrices import *
from tkinter import *
import random
import math

# some vector maths I used
# D(C(B(A(V)))) = V'
# V = A^-1(B^-1(C^-1(D^-1(V))))
class DiceFace: # stores the information about the face of a dice including the vectors which make the corners and dots up
    def __init__(self, canvas, corner1: Vector3D, corner2: Vector3D, corner3: Vector3D, corner4: Vector3D, number: int,
                 face_colour="white", dot_colour="black", size=20):
        self.canvas = canvas # the tkinter canvas object which this face lies in
        self.overall_transformation_matrix = IdentityMatrix(3) # for storing the overall matrix which the dice has been transformed by as it is rotated so this can be used to rotate dice back to the start
        self.transformations = [] # creates a list of all the matrix transformations done by the dice so can be used to move dice back to the start
        self.corner1 = corner1  # an object of Vector3D representing corner 1
        self.corner2 = corner2  # an object of Vector3D representing corner 2
        self.corner3 = corner3  # an object of Vector3D representing corner 3
        self.corner4 = corner4  # an object of Vector3D representing corner 4
        self.number = number    # the number the dice will show
        self.dots = self.__getInitialDotPositions(number) # gets a list of the vector representing dot positions on the dice
        self.face_colour = face_colour # the colour of the dice face
        self.dot_colour = dot_colour   # the colour of the dots on the dice
        self.size = size # the size of the dice (integer)

    def __getInitialDotPositions(self, n) -> list[Vector3D]:
        ## positions of all the dots which could occur on the dice as Vector3D object
        dot1 = Vector3D(
            [[((self.corner1.getX() + self.corner2.getX() + self.corner3.getX() + self.corner4.getX()) / 4)],
             [((self.corner1.getY() + self.corner2.getY() + self.corner3.getY() + self.corner4.getY()) / 4)],
             [((self.corner1.getZ() + self.corner2.getZ() + self.corner3.getZ() + self.corner4.getZ()) / 4)]])
        dot2 = Vector3D(
            [[((self.corner1.getX() + dot1.getX()) / 2)],
             [((self.corner1.getY() + dot1.getY()) / 2)],
             [((self.corner1.getZ() + dot1.getZ()) / 2)]]
        )
        dot3 = Vector3D(
            [[((self.corner2.getX() + dot1.getX()) / 2)],
             [((self.corner2.getY() + dot1.getY()) / 2)],
             [((self.corner2.getZ() + dot1.getZ()) / 2)]]
        )
        dot4 = Vector3D(
            [[((self.corner3.getX() + dot1.getX()) / 2)],
             [((self.corner3.getY() + dot1.getY()) / 2)],
             [((self.corner3.getZ() + dot1.getZ()) / 2)]]
        )
        dot5 = Vector3D(
            [[((self.corner4.getX() + dot1.getX()) / 2)],
             [((self.corner4.getY() + dot1.getY()) / 2)],
             [((self.corner4.getZ() + dot1.getZ()) / 2)]]
        )
        dot6 = Vector3D(
            [[((dot2.getX() + dot3.getX()) / 2)],
             [((dot2.getY() + dot3.getY()) / 2)],
             [((dot2.getZ() + dot3.getZ()) / 2)]]
        )
        dot7 = Vector3D(
            [[((dot4.getX() + dot5.getX()) / 2)],
             [((dot4.getY() + dot5.getY()) / 2)],
             [((dot4.getZ() + dot5.getZ()) / 2)]]
        )
        ## the dots needed to be used to represent each number:
        numbers_options = {1: [dot1], 2: [dot2, dot4], 3: [dot1, dot2, dot4], 4: [dot2, dot3, dot4, dot5],
                           5: [dot1, dot2, dot3, dot4, dot5], 6: [dot2, dot3, dot4, dot5, dot6, dot7]}
        return numbers_options[n] # returns a list of all the Vector3D dot objects

    def returnToStartPos(self) -> None: # transforms the dice back to the starting position
        for matrix in self.transformations[::-1]:
            self.transformSideByMatrix(matrix)
        self.transformations = []

    def rotateX(self, degrees) -> None: # rotates the dice face by number of degrees taken is as a parameter around X axis
        self.transformations.append(self.corner1.getXRotationMatrix(degrees).getInverse()) # adds the inverse of this transformation to transformations so dice can be returned to starting position
        ## transforming the Vector3D objects making up the corners
        self.corner1 = self.corner1.getRotatedAboutX(degrees)
        self.corner2 = self.corner2.getRotatedAboutX(degrees)
        self.corner3 = self.corner3.getRotatedAboutX(degrees)
        self.corner4 = self.corner4.getRotatedAboutX(degrees)
        ## transforming the vector 3D objects making up the dots
        new_dots = []
        for dot in self.dots:
            new_dots.append(dot.getRotatedAboutX(degrees))
        self.dots = new_dots

    def rotateY(self, degrees) -> None: # rotates the dice face by number of degrees taken is as a parameter around Y axis
        ## transforming the Vector3D objects making up the corners
        self.transformations.append(self.corner1.getYRotationMatrix(degrees).getInverse())
        self.corner1 = self.corner1.getRotatedAboutY(degrees)
        self.corner2 = self.corner2.getRotatedAboutY(degrees)
        self.corner3 = self.corner3.getRotatedAboutY(degrees)
        self.corner4 = self.corner4.getRotatedAboutY(degrees)
        ## transforming the vector 3D objects making up the dots
        new_dots = []
        for dot in self.dots:
            new_dots.append(dot.getRotatedAboutY(degrees))
        self.dots = new_dots


    def rotateZ(self, degrees) -> None:  # rotates the dice face by number of degrees taken is as a parameter around Z axis
        ## transforming the Vector3D objects making up the corners
        self.transformations.append(self.corner1.getZRotationMatrix(degrees).getInverse())
        self.corner1 = self.corner1.getRotatedAboutZ(degrees)
        self.corner2 = self.corner2.getRotatedAboutZ(degrees)
        self.corner3 = self.corner3.getRotatedAboutZ(degrees)
        self.corner4 = self.corner4.getRotatedAboutZ(degrees)
        ## transforming the vector 3D objects making up the dots
        new_dots = []
        for dot in self.dots:
            new_dots.append(dot.getRotatedAboutZ(degrees))
        self.dots = new_dots


    def transformSideByMatrix(self, matrix) -> None: # multiplies all the vectors making up the sides by the matrix taken in by it to transform by it
        ## transforming the Vector3D objects making up the corners
        self.corner1 = Vector3D(matrix.getMultiplyByMatrix(self.corner1))
        self.corner2 = Vector3D(matrix.getMultiplyByMatrix(self.corner2))
        self.corner3 = Vector3D(matrix.getMultiplyByMatrix(self.corner3))
        self.corner4 = Vector3D(matrix.getMultiplyByMatrix(self.corner4))
        new_dots = []
        ## transforming the vector 3D objects making up the dots
        for dot in self.dots:
            new_dots.append(Vector3D(matrix.getMultiplyByMatrix(dot)))
        self.dots = new_dots

    def plot(self) -> None: # draws the sides and dots on the canvas using the vectors
        self.canvas.create_polygon(
            [self.corner1.getX(), self.corner1.getY(), self.corner2.getX(), self.corner2.getY(), self.corner3.getX(),
             self.corner3.getY(), self.corner4.getX(), self.corner4.getY()], outline=self.dot_colour,
            fill=self.face_colour, width=1)
        for dot in self.dots:
            self.canvas.create_oval(dot.getX(), dot.getY(), dot.getX(), dot.getY(), fill=self.dot_colour,
                                    outline=self.dot_colour, width=4)

    def rotateXYZ(self, x_degrees, y_degrees, z_degrees) -> None: # side around X by x degrees, Y by y degrees and Z by z degrees
        self.rotateX(x_degrees)
        self.rotateY(y_degrees)
        self.rotateZ(z_degrees)

    def getCorner1(self) -> Vector3D: # returns the Vector3D object corner 1
        return self.corner1

    def getCorner2(self) -> Vector3D: # returns the Vector3D object corner 2
        return self.corner2

    def getCorner3(self) -> Vector3D: # returns the Vector3D object corner 3
        return self.corner3

    def getCorner4(self) -> Vector3D: # returns the Vector3D object corner 4
        return self.corner4

    def getAverageDistanceToPoint(self, point) -> float: # gets the average distance to a point on the face of a dice so it can be decided what order to plot the faces in
        total = 0
        for corner in [self.corner1, self.corner2, self.corner3, self.corner4]:
            total += math.sqrt(
                (corner.getX() - point[0]) ** 2 + (corner.getY() - point[1]) ** 2 + (corner.getZ() - point[2]) ** 2)
        return total / 4

    def getValue(self): # returns the number the dice shows
        return self.number


class Dice(Canvas): # class to store the information about a dice (e.g. the sides). Inherits tkinter canvas as this is where the dice is plotted
    def __init__(self, master, dice_id, size=40, face_colour="white", background_colour="black"): # constructor for initally creating dice and dice related attributes
        super().__init__(master, width=size*4, height=size*4, scrollregion=(-size*2, -size*2, size*2, size*2),
                         bg=background_colour, borderwidth=0,highlightthickness=0) # calls constructor of inherited class canvas to initialise the canvas, creating the inherited object
        self.dice_id = dice_id # stores a number which can be used to identify a dice object (e.g. to identify which one has finished spinning)
        self.size = size # the size of the dice
        self.sides = [] # a list of the sides making up the dice
        ### creates all the corners of the dice as Vector3D objects
        vector_a = Vector3D([[size], [size], [size]])
        vector_b = Vector3D([[-size], [size], [size]])
        vector_c = Vector3D([[size], [-size], [size]])
        vector_d = Vector3D([[size], [size], [-size]])
        vector_e = Vector3D([[-size], [-size], [size]])
        vector_f = Vector3D([[size], [-size], [-size]])
        vector_g = Vector3D([[-size], [size], [-size]])
        vector_h = Vector3D([[-size], [-size],
                             [-size]])
        ## creates all the faces of the dice as DiceFace objects
        face1 = DiceFace(self, vector_a, vector_b, vector_e, vector_c, 1, face_colour=face_colour, dot_colour=background_colour)
        self.addSide(face1)
        face2 = DiceFace(self, vector_d, vector_f, vector_h, vector_g, 2, face_colour=face_colour, dot_colour=background_colour)
        self.addSide(face2)
        face3 = DiceFace(self, vector_b, vector_e, vector_h, vector_g, 3, face_colour=face_colour, dot_colour=background_colour)
        self.addSide(face3)
        face4 = DiceFace(self, vector_a, vector_c, vector_f, vector_d, 4, face_colour=face_colour, dot_colour=background_colour)
        self.addSide(face4)
        face5 = DiceFace(self, vector_a, vector_b, vector_g, vector_d, 5, face_colour=face_colour, dot_colour=background_colour)
        self.addSide(face5)
        face6 = DiceFace(self, vector_c, vector_f, vector_h, vector_e, 6, face_colour=face_colour, dot_colour=background_colour)
        self.addSide(face6)
        self.plotSides()

    def addSide(self, side:DiceFace) -> None: # adds a side to the list of sides making up the dice
        self.sides.append(side)

    def getSidesToFrontOrder(self) -> list[DiceFace]: # returns the order which the sides should be drawn so that the ones at the back aren't drawn over the ones at the front
        return sorted(self.sides, key=lambda x: x.getAverageDistanceToPoint([0, 0, 100]))

    def getNearestSideToFront(self) -> DiceFace: # gets the front side
        return self.getSidesToFrontOrder()[0]

    def returnToStart(self): # returns the dice to the starting position with the front face flat
        for side in self.sides: side.returnToStartPos()
        self.plotSides()

    def plotSides(self): # plots all the sides of the dice
        self.clearCanvas() # first clears the canvas of any previous things (e.g. previous dice faces)
        self.sides = self.getSidesToFrontOrder()
        for side in self.sides:
            side.plot()

    def clearCanvas(self): # clears to the tkinter canvas the dice is drawn in
        self.delete("all")

    def rotateX(self, degrees): # rotates the dice in the X axis by degrees
        for side in self.sides: side.rotateX(degrees) # rotates side by side, iterating through all dice sides and rotating them individually
        self.plotSides()

    def rotateY(self, degrees): # rotates the dice in the Y axis by degrees
        for side in self.sides: side.rotateY(degrees) # rotates side by side, iterating through all dice sides and rotating them individually
        self.plotSides()

    def rotateZ(self, degrees): # rotates the dice in the Y axis by degrees
        for side in self.sides: side.rotateZ(degrees) # rotates side by side, iterating through all dice sides and rotating them individually
        self.plotSides()

    def rotateXYZ(self, x_degrees, y_degrees, z_degrees): # rotates the dice in the X, Y and Z axis by specified number of degrees degrees
        for side in self.sides: side.rotateXYZ(x_degrees, y_degrees, z_degrees) # rotates side by side, iterating through all dice sides and rotating them individually
        self.plotSides()

    def rotateRandomlyToNumber(self, final_number, finished_function, rotations=random.randint(5, 15)): # rotated randomly rotation number of times to the final number then calls finished function to say it has finished
        if rotations > 0:
            time = int(75 / rotations)
            x_rotation = random.choice([random.randint(10, 25), -random.randint(10, 25)]) # 10 to 25
            y_rotation = random.choice([random.randint(10, 25), -random.randint(10, 25)])
            z_rotation = random.choice([random.randint(10, 25), -random.randint(10, 25)])
            sub_rotations = random.randint(3, 5)
            self.rotateAngle(x_rotation, y_rotation, z_rotation, time, sub_rotations)
            # noinspection PyTypeChecker
            self.after(time * sub_rotations, lambda: self.rotateRandomlyToNumber(final_number, finished_function, rotations - 1))
        else:
            self.returnToStart()
            finished_function()
            self.turnToNumberedSide(final_number)

    def rotateAngle(self, x_degrees, y_degrees, z_degrees, time, rotations=random.randint(20, 60)): # rotates rotations number of times in X, Y and Z direction by specified number of degrees, pausing between each rotation
        if rotations > 0:
            self.rotateXYZ(x_degrees, y_degrees, z_degrees)
            rotations -= 1
            # noinspection PyTypeChecker
            self.after(time, lambda: self.rotateAngle(x_degrees, y_degrees, z_degrees, time, rotations))

    def turnToNumberedSide(self, n): # rotates from starting position (2) to side showing number taken in as parameter, n
        options = {1:(180, 0, 0), 2:(0, 0, 0), 3:(0, 270, 0), 4:(0, 90, 0), 5:(90, 180, 0), 6:(90, 0, 0)}
        angles = options[n]
        self.rotateXYZ(angles[0], angles[1], angles[2])
