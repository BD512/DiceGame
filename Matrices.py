import numpy as np


class Matrix(list): # a list class which stores the matrix as a list and allows operations to be performed on / using it
    def __init__(self, matrix:list):
        super().__init__(matrix)
        self.rows:int = len(matrix) # number of rows in matrix
        self.columns:int = len(matrix[0]) # number of columns in matrix

    def addTo(self, matrix_to_add) -> None: # adds the matrix to the matrix taken in and changes the matrix self to the result
        res = self.getAddTo(matrix_to_add)
        self.clear()
        self.extend(res)

    def getAddTo(self, matrix_to_add):  # returns the value of this matrix added to parameter, matrix_to_add
        if self.rows == matrix_to_add.getRows() and self.columns == matrix_to_add.getColumns():
            res = []  # [[0]*self.columns]*self.rows # np.full((self.rows, self.columns), 0)
            for row_index in range(self.rows):
                row = []
                for column_index in range(self.columns):
                    row.append(self[row_index][column_index] + matrix_to_add[row_index][column_index])
                res.append(row)
            return Matrix(res)
        else:
            raise Exception("Number of rows and columns of matrices must be equal to add")

    def subtractFrom(self, matrix_to_subtract): # sets this matrix to the result when the matrix taken in as a parameter is subtracted from it
        res = self.getSubtractFrom(matrix_to_subtract)
        self.clear()
        self.extend(res)

    def getSubtractFrom(self, matrix_to_subtract): # returns the result of this matrix subtract the matrix taken in as parameter
        if self.rows == matrix_to_subtract.getRows() and self.columns == matrix_to_subtract.getColumns():
            res = []  # [[0]*self.columns]*self.rows # np.full((self.rows, self.columns), 0)
            for row_index in range(self.rows):
                row = []
                for column_index in range(self.columns):
                    row.append(self[row_index][column_index] - matrix_to_subtract[row_index][column_index])
                res.append(row)
            return Matrix(res)
        else:
            raise Exception("Number of rows and columns of matrices must be equal to subtract")

    def transpose(self): # sets the matrix to itself transposed
        res = self.getTranspose()
        self.clear()
        self.extend(res)

    def getTranspose(self): # returns the transposed value of the matrix
        res = []
        for row_number in range(self.rows):
            current_row = []
            for column_number in range(self.columns):
                current_row.append(self[column_number][row_number])
            res.append(current_row)
        return Matrix(res)

    def getRows(self): # returns number of rows in the matrix
        return self.rows

    def getColumns(self): # returns number of columns in the matrix
        return self.columns

    def multiplyByMatrix(self, matrix_to_multiply): # sets matrix to itself multiplied by matrix taken in as parameter
        res = self.getMultiplyByMatrix(matrix_to_multiply)
        self.clear()
        self.extend(res)

    def getMultiplyByMatrix(self,
                            matrix_to_multiply):  # multiplies self by the matrix (self first in multiplication) Tested and works!
        if self.columns == matrix_to_multiply.getRows():
            res = []  # [[0]*matrix_to_multiply.getColumns()]*self.rows # np.full((self.rows, matrix_to_multiply.getColumns()), 0)
            for row_a in range(self.rows):
                row = []
                for column_b in range(matrix_to_multiply.getColumns()):
                    total = 0
                    for row_b in range(matrix_to_multiply.getRows()):
                        # print(self[row_a][row_b])
                        # print(matrix_to_multiply[row_b][column_b])
                        total += self[row_a][row_b] * matrix_to_multiply[row_b][column_b]
                    row.append(total)
                res.append(row)
            return Matrix(res)
        else:
            raise Exception("The number of columns of matrix A must be equal to the number of rows of matrix B")

    def multiplyByNumber(self, n): # changes the matrix to itself with all its values multiplied by parameter n
        res = self.getMultipliedByNumber(n)
        self.clear()
        self.extend(res)

    def getMultipliedByNumber(self, n): # returns matrix with all values multiplied by n
        res = []
        for row in self:
            current_row = []
            for column in row:
                current_row.append(column * n)
            res.append(current_row)
        return Matrix(res)


class SquareMatrix(Matrix): # a class which inherits Matrix and is a matrix but nxn instead of nxm
    def __init__(self, matrix):
        super().__init__(matrix)
        if self.columns != self.rows: raise Exception(
            f"Number of columns must be equal to rows for matrix to be square. \nThe matrix is {matrix}")

    def getAddTo(self, matrix_to_add): # gets the value of matrices added together but as a SquareMatrix object
        return SquareMatrix(Matrix.getAddTo(self, matrix_to_add))

    def getSubtractFrom(self, matrix_to_subtract): # gets the value of matrix parameter subtracted from self matrix but as a SquareMatrix object
        return SquareMatrix(Matrix.getSubtractFrom(self, matrix_to_subtract))

    def getTranspose(self): # gets the transpose of the matrix but as a square matrix object
        return SquareMatrix(Matrix.getTranspose(self))

    def getMultipliedByNumber(self, n): # returns the matrix with each element multiplied by n but as a square matrix
        return SquareMatrix(Matrix.getMultipliedByNumber(self, n))

    def toMatrixOfMinors(self): # makes matrix its matrix of minors
        res = self.getMatrixOfMinors()
        self.clear()
        self.extend(res)

    def getMatrixOfMinors(self): # returns the matrix of minors of the matrix
        res = []
        for det_row_num in range(self.rows):
            res_row = []
            for det_column_num in range(self.columns):
                temp_mini_matrix = []
                for row_num in range(self.columns):
                    current_row = []
                    for column_num in range(self.columns):
                        if column_num != det_column_num and row_num != det_row_num:
                            current_row.append(self[row_num][column_num])
                    if current_row:
                        temp_mini_matrix.append(current_row)
                res_row.append(SquareMatrix(temp_mini_matrix).getDeterminant())
            res.append(res_row)
        return SquareMatrix(res)

    def toMatrixOfCofactors(self): # changes the matrix to its matrix of cofactors
        res = self.getMatrixOfCofactors()
        self.clear()
        self.extend(res)

    def getMatrixOfCofactors(self): # returns the matrix of cofactors of the matrix
        res = []
        for row in range(self.rows):
            current_row = []
            for column in range(self.columns):
                if (row + column) % 2 == 1:
                    current_row.append((self[row][column] * -1))
                else:
                    current_row.append(self[row][column])
            res.append(current_row)
        return SquareMatrix(res)

    def getDeterminant(self) -> float: # returns the determinant of the matrix
        if self.getRows() == self.getColumns() == 1:
            return self[0]
        elif self.getRows() == self.getColumns() == 2:
            return self[0][0] * self[1][1] - self[1][0] * self[0][1]
        else:
            total = 0
            add = True
            for top_col_pos in range(self.columns):
                current_mini_matrix = []
                for row_index in range(1, self.rows):
                    current_row = []
                    for column_index in range(self.columns):
                        if column_index != top_col_pos:
                            current_row.append(self[row_index][column_index])
                    current_mini_matrix.append(current_row)
                if add:
                    val = SquareMatrix(current_mini_matrix).getDeterminant() * self[0][top_col_pos]
                    total += val
                    add = False
                else:
                    val = SquareMatrix(current_mini_matrix).getDeterminant() * self[0][top_col_pos]
                    total -= val
                    add = True
            return total

    def toInverse(self): # changes the matrix to its inverse
        res = self.getInverse()
        self.clear()
        self.extend(res)

    def getInverse(self): # returns the inverse of the matrix if not singular
        det = self.getDeterminant()
        if det == 0:
            raise ValueError("Cannot get the inverse of a matrix which is singular (has a determinant of zero)")
        res = []
        for row in (((self.getMatrixOfMinors()).getMatrixOfCofactors()).getTranspose()):
            current_row = []
            for element in row:
                current_row.append(element * (1 / det))
            res.append(current_row)
        return SquareMatrix(res)


class IdentityMatrix(SquareMatrix): # a child of SquareMatrix to store an identity matrix of specific dimension
    def __init__(self, dimensions):
        super().__init__(self.__createMatrix(dimensions))

    @staticmethod
    def __createMatrix(dimensions):
        res = []
        for row in range(dimensions):
            final_row = []
            for col in range(dimensions):
                if row == col:
                    final_row.append(1)
                else:
                    final_row.append(0)
            res.append(final_row)
        return res


class Vector(Matrix): # a child of matrix to store a vector (a matrix of 1 by n dimension)
    def __init__(self, vector):
        super().__init__(vector)
        self.dimensions = len(vector)

    def getMultiplyByMatrix(self, matrix_to_multiply): # returns a Vector object of a matrix multiplied by a vector
        return Vector(Matrix.getMultiplyByMatrix(self, matrix_to_multiply))

    def getAddTo(self, matrix_to_add): # returns a Vector object of two vectors added together
        return Vector(Matrix.getAddTo(self, matrix_to_add))

    def getSubtractFrom(self, matrix_to_subtract): # returns a Vector object oof vector subtract the parameter vector
        return Vector(Matrix.getSubtractFrom(self, matrix_to_subtract))

    def getTranspose(self): # returns Vector object of the transpose of the vector
        return Vector(Matrix.getTranspose(self))

    def getMultipliedByNumber(self, n): # get the Vector object with all element multiplied by n
        return Vector(Matrix.getMultipliedByNumber(self, n))

    def getDimensions(self): # returns the dimension of the vector
        return self.dimensions


class Vector3D(Vector): # child of Vector for storing 3D vectors only
    def __init__(self, vector):
        super().__init__(vector)

    def getMultiplyByMatrix(self, matrix_to_multiply): # same as for parent but returns as Vector3D object
        return Vector3D(Vector.getMultiplyByMatrix(self, matrix_to_multiply))

    def getAddTo(self, matrix_to_add): # same as for parent but returns as Vector3D object
        return Vector3D(Vector.getAddTo(self, matrix_to_add))

    def getSubtractFrom(self, matrix_to_subtract): # same as for parent but returns as Vector3D object
        return Vector3D(Vector.getSubtractFrom(self, matrix_to_subtract))

    def getTranspose(self): # same as for parent but returns as Vector3D object
        return Vector3D(Vector.getTranspose(self))

    def getMultipliedByNumber(self, n): # same as for parent but returns as Vector3D object
        return Vector3D(Vector.getMultipliedByNumber(self, n))

    def getRotatedAboutX(self, angle):  # returns the vector transformed by a matrix to rotate about X axis number of degrees taken in as angle parameter
        rotation_matrix = self.getXRotationMatrix(angle)
        return Vector3D(rotation_matrix.getMultiplyByMatrix(self))

    @staticmethod
    def getXRotationMatrix(degrees): # returns the transformation matrix which the vector can be multiplied by to rotate it around the X axis by degrees taken in as parameter
        return SquareMatrix([[1, 0, 0],
                             [0, np.cos(degrees * np.pi / 180), -np.sin(degrees * np.pi / 180)],
                             [0, np.sin(degrees * np.pi / 180), np.cos(degrees * np.pi / 180)]])

    def getRotatedAboutY(self, angle): # returns the vector transformed by a matrix to rotate about Y axis number of degrees taken in as angle parameter
        rotation_matrix = self.getYRotationMatrix(angle)
        return Vector3D(rotation_matrix.getMultiplyByMatrix(self))


    @staticmethod
    def getYRotationMatrix(degrees):  # returns the transformation matrix which the vector can be multiplied by to rotate it around the Y axis by degrees taken in as parameter
        return SquareMatrix([[np.cos(degrees * np.pi / 180), 0, np.sin(degrees * np.pi / 180)],
                             [0, 1, 0],
                             [-np.sin(degrees * np.pi / 180), 0, np.cos(degrees * np.pi / 180)]])


    def getRotatedAboutZ(self, angle): # returns the vector transformed by a matrix to rotate about Z axis number of degrees taken in as angle parameter
        rotation_matrix = self.getZRotationMatrix(angle)
        return Vector3D(rotation_matrix.getMultiplyByMatrix(self))

    @staticmethod
    def getZRotationMatrix(degrees): # returns the transformation matrix which the vector can be multiplied by to rotate it around the Z axis by degrees taken in as parameter
        return SquareMatrix([[np.cos(degrees * np.pi / 180), -np.sin(degrees * np.pi / 180), 0],
                             [np.sin(degrees * np.pi / 180), np.cos(degrees * np.pi / 180), 0],
                             [0, 0, 1]])

    def getX(self): # returns the X value of the vector
        return self[0][0]

    def getY(self): # returns the Y value of the vector
        return self[1][0]

    def getZ(self): # returns the Z value of the vector
        return self[2][0]