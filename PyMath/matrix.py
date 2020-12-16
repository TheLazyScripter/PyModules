from __future__ import annotations

from random import randint
from typing import Union, Tuple, List

from PyMath.vector import Vector


class Matrix(Vector):
    """'Matrix' Base Class, subclass of 'Type[Vector]':

    Class used to perform matrix mathematics, translations, rotations
    transposes and matrix chains.
    """

    def __init__(self, dimensions=(3, 3), fill=1.0):

        self.__size = self.__rows, self.__columns = dimensions
        super(Matrix, self).__init__(*(Vector(*list(float(fill)
                                                    for _ in range(self.__columns)))
                                       for _ in range(self.__rows)))

    def rows(self):
        """Getter for rows"""
        return self.__rows

    def cols(self):
        """Getter for cols"""
        return self.__columns

    def size(self):
        """Getter for size"""
        return self.__size

    def __len__(self):
        """Total position size of 'Matrix'"""
        return self.__rows * self.__columns

    def __str__(self):
        res = ""
        for i in self:
            if i == self[-1]:
                res += str(i)
            else:
                res += str(i) + "\n"
        return res

    def __repr__(self):
        return repr(self._components)

    def __iter__(self):
        self.__pos = 0
        return self

    def __next__(self):
        if self.__pos < len(self._components):
            self.__pos += 1
            return self._components[self.__pos - 1]
        raise StopIteration

    def __add__(self, other: Union[Matrix, int, float]) -> Matrix:
        """Overload + operator to perform element-wise addition between 2 matrices or matrix and scalar"""

        new_matrix = Matrix(self.size())
        if isinstance(other, Matrix):
            if self.size() is other.size():
                for i in range(self.__rows):
                    for j in range(self.__columns):
                        new_matrix[i][j] = self[i][j] + other[i][j]
            else:
                raise Matrix.Exceptions.MatrixSizeError(self, other)

        elif isinstance(other, (float, int)):
            for i in range(self.__rows):
                for j in range(self.__columns):
                    new_matrix[i][j] = self[i][j] + other
        else:
            raise Matrix.Exceptions.MatrixMathError(other)
        return new_matrix

    def __sub__(self, other: Union[Matrix, int, float]) -> Matrix:
        """Overload - operator to perform element-wise subtraction between 2 matrices or matrix and scalar"""

        new_matrix = Matrix(self.size())
        if isinstance(other, Matrix):
            if self.size() is other.size():
                for i in range(self.__rows):
                    for j in range(self.__columns):
                        new_matrix[i][j] = self[i][j] - other[i][j]
            else:
                raise Matrix.Exceptions.MatrixSizeError(self, other)

        elif isinstance(other, (float, int)):
            for i in range(self.__rows):
                for j in range(self.__columns):
                    new_matrix[i][j] = self[i][j] - other
        else:
            raise Matrix.Exceptions.MatrixMathError(other)
        return new_matrix

    def __mul__(self, other: Union[Matrix, int, float]) -> Matrix:
        """Overload * operator to perform element-wise multiplication between 2 matrices or matrix and scalar"""

        new_matrix = Matrix(self.size())
        if isinstance(other, Matrix):
            if self.size() is other.size():
                for i in range(self.__rows):
                    for j in range(self.__columns):
                        new_matrix[i][j] = self[i][j] * other[i][j]
            else:
                raise Matrix.Exceptions.MatrixSizeError(self, other)

        elif isinstance(other, (float, int)):
            for i in range(self.__rows):
                for j in range(self.__columns):
                    new_matrix[i][j] = self[i][j] * other
        else:
            raise Matrix.Exceptions.MatrixMathError(other)
        return new_matrix

    def __truediv__(self, other: Union[Matrix, int, float]) -> Matrix:
        """Overload / operator to perform element-wise division between 2 matrices or matrix and scalar"""

        new_matrix = Matrix(self.size())
        if isinstance(other, Matrix):
            if self.size() is other.size():
                for i in range(self.__rows):
                    for j in range(self.__columns):
                        new_matrix[i][j] = self[i][j] / other[i][j]
            else:
                raise Matrix.Exceptions.MatrixSizeError(self, other)

        elif isinstance(other, (float, int)):
            for i in range(self.__rows):
                for j in range(self.__columns):
                    new_matrix[i][j] = self[i][j] / other
        else:
            raise Matrix.Exceptions.MatrixMathError(other)
        return new_matrix

    def __matmul__(self, other: Matrix) -> Matrix:
        """Overload @ operator to perform point-wise multiplication between 2 Matrices"""

        if isinstance(other, Matrix):
            if self.__columns == other.__rows:
                new_matrix = Matrix((self.__rows, other.__columns), 0)
                for i in range(self.__rows):
                    for j in range(other.__columns):
                        for k in range(other.__rows):
                            new_matrix[i][j] += self[i][k] * other[k][j]
                return new_matrix
            else:
                raise Matrix.Exceptions.MatrixSizeError(self, other)
        else:
            raise Matrix.Exceptions.MatrixMultiplicationError(other)

    def inverse(self):
        matrix_copy = Matrix.copy(self)
        for fd in range(len(self)):
            fd_scalar = 1.0 / self[fd][fd]
            for i in range(len(self)):
                matrix_copy[fd][i] *= fd_scalar
            for x in self[0:fd] + self[fd + 1:]:
                cr_scalar = self[x][fd]
                for j in range(len(self)):
                    matrix_copy[x][j] -= (matrix_copy[fd][j] * cr_scalar)
        return matrix_copy

    @staticmethod
    def matrix_from_list(matrix_list: Union[Tuple, List]) -> Matrix:
        """Return a new Matrix from a list of lists"""

        assert all(len(matrix_list[i]) == len(matrix_list[0]) for i in range(len(matrix_list)))
        r = len(matrix_list)
        c = len(matrix_list[0])
        new_matrix = Matrix((r, c))
        for i in range(r):
            for j in range(c):
                new_matrix[i][j] = matrix_list[i][j]
        return new_matrix

    @staticmethod
    def copy(matrix):
        """Return a new 'Matrix' from 'Matrix'"""

        return Matrix(matrix.size()) * matrix

    @staticmethod
    def identity(size: Union[int, float, Tuple[int, float], List[int, float]]) -> Matrix:
        """Return a new square matrix identity

        Calculate the 'Matrix' identity for a 'Matrix' with dimensions size.
        If size is a 'list' or 'tuple', size is the largest value found within.


        Fill the `Matrix` with 0, and set the main diagonal to 1

        Args:
            size (int, float, tuple, list): Size of the new 'Matrix'

        Returns:
            `Matrix`: New `Matrix` identity

        ___________________________________________________________

         :             [ 1 0 0 ]
         :m.identity = [ 0 1 0 ]
         :    3x3      [ 0 0 1 ]

        """

        if isinstance(size, (int, float)):
            new_matrix = Matrix((size, size), fill=0)
            for i in range(new_matrix.__rows):
                for x in range(new_matrix.__columns):
                    new_matrix[i][i] = 1
            return new_matrix
        else:
            raise Matrix.Exceptions.MatrixIdentityError(size)

    @staticmethod
    def random(size: Union[int, float, List[int, float], Tuple[int, float]],
               minimum: Union[int, float] = -5, maximum: Union[int, float] = 5) -> Matrix:
        """Return a new square matrix filled with random integers between min and max

        Create a new Matrix with dimensions size and fill it with random integers bound between
        minimum, and maximum. If size is list or tuple, dimensions are the largest value within.

        Args:
            size: (int, tuple, list): Size of the new Matrix
            minimum (int, float): Smallest random integer
            maximum (int, float): Largest random integer

        Returns:
            Matrix: New Random Matrix with dimensions=(size, size) and fill randint(minimum, maximum)
        """

        if isinstance(size, (int, tuple)):
            size = max(size)  # Grab largest value from size

        new_matrix = Matrix((size, size))
        [[new_matrix[i].__setitem__(x, randint(minimum, maximum))
          for x in range(new_matrix.cols())] for i in range(new_matrix.rows())]

        return new_matrix

    @staticmethod
    def add(m1: Matrix, m2: Matrix) -> Matrix:
        """Add a Matrix to another Matrix or a Number

        Perform element-wise addition between 2 Matrices or between a
        Matrix and a scalar. Matrix chaining notation is allowed.

        Args:
            m1 (Matrix): Matrix 1
            m2 (Matrix): Matrix 2

        Raises:
            MatrixSizeError: If other is Matrix and has a different
                size than the first
            MatrixMathError: If other is not a Matrix, int, or float

        Returns:
            Matrix: New Matrix of a + b
        """

        return m1 + m2

    @staticmethod
    def subtract(m1: Matrix, m2: Matrix) -> Matrix:
        """Subtract a Matrix by another Matrix or a Number

        Perform element-wise subtraction between 2 Matrices or between a
        Matrix and a scalar. Matrix chaining notation is allowed.

        Args:
            m1 (Matrix): Matrix 1
            m2 (Matrix): Matrix 2

        Raises:
            MatrixSizeError: If other is Matrix and has a different
                size than the first
            MatrixMathError: If other is not a Matrix, int, or float

        Returns:
            Matrix: New Matrix of a - b
        """

        return m1 - m2

    @staticmethod
    def multiply(m1: Matrix, m2: Matrix) -> Matrix:
        """Multiply a Matrix with another Matrix or a Scalar

        Perform 'element-wise' Multiplication between 2 Matrices or between a
        Matrix and a scalar. Matrix chaining notation is allowed.

        Args:
            m1 (Matrix): Matrix 1
            m2 (Matrix): Matrix 2

        Raises:
            MatrixSizeError: If other is Matrix and has a different
                size than the first
            MatrixMathError: If other is not a Matrix, int, or float

        Returns:
            Matrix: New Matrix of a * b

        See Also:
            (M1 @ M2) for Matrix Multiplication
        """

        return m1 * m2

    @staticmethod
    def divide(m1: Matrix, m2: Matrix) -> Matrix:
        """Divide a Matrix by another Matrix or a Scalar

        Perform 'element-wise' Division between 2 Matrices or between a
        Matrix and a scalar. Matrix chaining notation is allowed.

        Args:
            m1 (Matrix): Matrix 1
            m2 (Matrix): Matrix 2

        Raises:
            MatrixSizeError: If other is Matrix and has a different
                size than the first
            MatrixMathError: If other is not a Matrix, int, or float

        Returns:
            Matrix: New Matrix of a / b
        """

        return m1 / m2

    @staticmethod
    def matrix_multiply(m1: Matrix, m2: Matrix) -> Matrix:
        """Perform Matrix Multiplication on 2 Matrices

        Create a new Matrix from a and b using Matrix Multiplication.


        Args:
            m1 (Matrix): Matrix 1
            m2 (Matrix): Matrix 2

        Raises:
            MatrixSizeError: If other is Matrix and a.rows != other.cols
            MatrixMultiplicationError: If other is not a Matrix

        Returns:
            Matrix: A new Matrix of A @ B
        """

        return m1 @ m2

    class Exceptions:
        """Matrix Exception Struct to house relevant exceptions"""

        class MatrixMathError(Exception):
            def __init__(self, other: any):
                msg = f"'other' should be of type {Matrix.__name__, 'int', 'float'}. " \
                      f"Found '{type(other).__name__}' instead."

                super().__init__(msg)

        class MatrixMultiplicationError(Exception):
            def __init__(self, other: Matrix):
                msg = f"'other' should be of type {Matrix.__name__}. Found '{type(other).__name__}' instead."
                super().__init__(msg)

        class MatrixSizeError(Exception):
            def __init__(self, m1: Matrix, m2: Matrix):
                msg = f"Matrices dimension should be '{m1.cols()}x{m1.rows()}'. " \
                      f"Found '{m2.cols()}x{m2.rows()}' instead."
                super().__init__(msg)

        class MatrixIdentityError(Exception):
            def __init__(self, size: any):
                msg = f"Size should be int or float. Found {type(size).__name__} instead."
                super().__init__(msg)
