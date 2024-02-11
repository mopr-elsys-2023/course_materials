import functools
import itertools

def prod(iterable):
    return functools.reduce(lambda acc, el: acc*el, iterable, 1) 

class Matrix:

    def __init__(self, rows_count, cols_count, elements):
        self.rows_count = rows_count
        self.cols_count = cols_count
        self.elements = elements

    def __validate(self):
        assert 0 <= self.rows_count
        assert 0 <= self.cols_count
        assert len(self.elements) == self.rows_count * self.cols_count

    def __add__(self, other):
        self.__validate()
        other.__validate()
        assert self.rows_count == other.rows_count
        assert self.cols_count == other.cols_count

        result_elements = [ my_el + other_el for my_el, other_el in zip(self.elements, other.elements) ]
        return Matrix(self.rows_count, self.cols_count, result_elements)

    def __mul__(self, factor):
        assert False

    def __rmul__(self, factor):
        self.__validate()
        assert isinstance(factor, (int, float, complex))

        result_elements = [ factor * my_el for my_el in self.elements ]
        return Matrix(self.rows_count, self.cols_count, result_elements)

    def __eq__(self, other):
        return isinstance(other, Matrix) and self.rows_count == other.rows_count and self.cols_count == other.cols_count and self.elements == other.elements

    def __matmul__(self, other):
        self.__validate()
        other.__validate()
        assert self.cols_count == other.rows_count

        result_elements = [ Matrix.dot_product(my_row, other_col) for my_row in self.rows for other_col in other.cols ]
        return Matrix(self.rows_count, other.cols_count, result_elements)

    @property
    def rows(self):
        return [ self.row(i) for i in range(self.rows_count) ]

    @property
    def cols(self):
        return [ self.col(i) for i in range(self.cols_count) ]

    @staticmethod
    def dot_product(vector_a, vector_b):
        assert isinstance(vector_a, list)
        assert isinstance(vector_b, list)
        assert len(vector_a) == len(vector_b)

        return sum( el_a * el_b for el_a, el_b in zip(vector_a, vector_b) )

    def row(self, row_idx):
        self.__validate()
        assert 0 <= row_idx < self.rows_count

        slice_start = self.cols_count * row_idx
        slice_end = self.cols_count * (row_idx + 1)

        return self.elements[slice_start:slice_end]

    def col(self, col_idx):
        self.__validate()
        assert 0 <= col_idx < self.cols_count

        slice_start = col_idx
        slice_step = self.cols_count

        return self.elements[slice_start::slice_step]

    # TODO: Use matrix multiplication for elementary transformations
    def swap_rows(self, row_i, row_j):
        self.__validate()
        assert 0 <= row_i < self.rows_count
        assert 0 <= row_j < self.rows_count

        row_i_start = self.cols_count * row_i
        row_i_end = self.cols_count * (row_i + 1)

        row_j_start = self.cols_count * row_j
        row_j_end = self.cols_count * (row_j + 1)

        # a, b = b, a
        self.elements[row_i_start:row_i_end], self.elements[row_j_start:row_j_end] = self.elements[row_j_start:row_j_end], self.elements[row_i_start:row_i_end]

    def scale_row(self, row_idx, factor):
        self.__validate()
        assert isinstance(factor, (int, float, complex)) 
        assert 0 <= row_idx < self.rows_count

        slice_start = self.cols_count * row_idx
        slice_end = self.cols_count * (row_idx + 1)

        self.elements[slice_start:slice_end] = [ factor * my_el for my_el in self.row(row_idx) ]

    def scale_and_add_to(self, row_i, factor, row_j):
        self.__validate()
        assert 0 <= row_i < self.rows_count
        assert 0 <= row_j < self.rows_count
        assert isinstance(factor, (int, float, complex)) 

        row_j_start = self.cols_count * row_j
        row_j_end = self.cols_count * (row_j + 1)

        row_i_scaled = [ factor * i_el for i_el in self.row(row_i) ]
        self.elements[row_j_start:row_j_end] = [ el_j + el_i for el_j, el_i in zip(self.row(row_j), row_i_scaled)]

    @staticmethod
    def count_inversions(perm):
        inversions_count = 0
        for idx, el in enumerate(perm):
            inversions_count += sum( 1 if prev > el else 0 for prev in perm[:idx] )
        return inversions_count

    def common_formula_determinants(self):
        self.__validate()
        assert self.rows_count == self.cols_count

        # return sum( (-1)**(Matrix.count_inversions(perm))*  )

        determinant = 0
        for perm in itertools.permutations(range(1, self.rows_count+1)):
            inversions_count = Matrix.count_inversions(perm)

            current_sum_member = [ row(i)[perm_el] for i, perm_el in enumerate(perm) ]
            determinant += (-1)**(inversions_count) * prod(current_sum_member)

        return determinant




    def subdeterminant(self, row_i, col_j):
        self.__validate()
        assert 0 <= row_i < self.rows_count
        assert 0 <= col_j < self.cols_count


        # [  permutations(...) if i == p and j == q ]



class PrintMatrix(Matrix):

    def __init__(self, rows_count, cols_count, elements,  *args, **kwargs):
        super(PrintMatrix, self).__init__(rows_count, cols_count, elements)
        pass

    def __validate(self):
        super().__validate()
        pass

    def __add__(self, other):
        print('Summing matrices with elements')
        self.print()
        print('and')
        other.print()
        print('to sum them, we add each element together as such:')

        print('result[i][j] = A[i][j] + B[i][j]')
    
        return self.__class__().__add__(other)

    def expand_row_adjugated(self, row_idx):
        print('to find determinant using adjugated quantities, we find all adjugated quantities:')

        print('p=', row_idx)

        determinant = 0
        for col_idx in range(self.cols_count):
            print(f'a[p][{col_idx}] = ')
            print( self.row(row_idx)[col_idx] )
            print(f'A[p][{col_idx}] = SUM( j_p = q ) a[1][j_1] ... a[p-1][jp - 1] . a[p+1][jp + 1]... ')
            
            adjugated_quantity = 0
            for perm in itertools.permutations(range(self.rows_count)):
                inversions_count = Matrix.count_inversions(perm)


                current_sum_member = [ self.row(i)[perm_el] for i, perm_el in enumerate(perm) if perm[row_idx] == col_idx and ( i != row_idx ) ]
                # current_sum_member = [ (self.row(i)[perm_el], i, perm_el) for i, perm_el in enumerate(perm) if perm[row_idx] == col_idx and ( i != row_idx ) ]
                # current_sum_member = [ row(i)[perm_el] for i, perm_el in enumerate(perm) if i == row_idx and perm_el == col_idx ]
                
                print('Elements, that will partake in adjugated quantity: ', current_sum_member)
                print('adjugated_quantity: ')
                adjugated_quantity += (-1)**(inversions_count) * prod(current_sum_member) 
                # print( (-1)**(inversions_count) * prod(current_sum_member) )

            print(adjugated_quantity)
            determinant += self.row(row_idx)[col_idx] * adjugated_quantity

        print('final value of determinant:')
        print(determinant)

    def print(self):
        for row_idx in range(self.rows_count):
            print(self.row(row_idx))