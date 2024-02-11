import pytest

from src.matrix import Matrix, PrintMatrix
from src.augmented_matrix import AugmentedMatrix

def test_sum_matrices():

    m1 = Matrix(3, 3, [1,2,3,4,5,6,7,8,9])
    m2 = Matrix(3, 3, [1,0,0,0,1,0,0,0,1])

    result = m1 + m2

    assert result == Matrix(3, 3, [2,2,3,4,6,6,7,8,10])


def test_sum_wrong_dim_matrices():
    m1 = Matrix(3, 3, [1,2,3,4,5,6,7,8,9])
    m2 = Matrix(2, 2, [1,0,0,1])

    with pytest.raises(AssertionError):
        result = m1 + m2


def test_mult_correct():
    m1 = Matrix(3, 3, [1,0,0,0,1,0,0,0,1])
    factor = 6

    result = factor * m1

    assert result == Matrix(3, 3, [6,0,0,0,6,0,0,0,6])


def test_mult_wrong_side():
    m1 = Matrix(3, 3, [1,0,0,0,1,0,0,0,1])
    factor = 6

    with pytest.raises(AssertionError):
        result = m1 * factor

def test_dot_product():

    vector_a = [1, 2]
    vector_b = [0, 4]

    assert Matrix.dot_product(vector_a, vector_b) == 8

def test_row():
    m1 = Matrix(3, 3, [1,0,0,0,1,0,0,0,1])

    assert m1.row(0) == [1, 0, 0]

def test_col():
    m1 = Matrix(3, 3, [1,0,0,2,1,0,3,0,1])

    assert m1.col(0) == [1, 2, 3]


def test_matrix_mult():
    m1 = Matrix(3, 3, [1,2,3,4,5,6,7,8,9])
    m2 = Matrix(3, 3, [1,0,0,0,1,0,0,0,1])

    assert m1 @ m2 == m1

def test_augmentation_matrix():
    augmentation1 = Matrix(2, 1, [-1, 3])
    a1 = AugmentedMatrix(2, 2, [1, -2, -3, 6], augmentation1)
    a1.print()

    a1.scale_and_add_to(0, 3, 1)
    a1.print()

    result_augmentation = Matrix(2, 1, [-1, 0])
    result_a = AugmentedMatrix(2, 2, [1, -2, 0, 0], result_augmentation)
    assert a1 == result_a

# def test_gauss():
#     augmentation1 = Matrix(2, 1, [-1, 3])
#     a1 = AugmentedMatrix(2, 2, [1, -2, -3, 6], augmentation1)
#     a1.print()

#     a1.gauss()
#     a1.print()

#     # assert False

# def test_printer():
    
#     m1 = PrintMatrix(3, 3, [1,2,3,4,5,6,7,8,9])
#     m2 = PrintMatrix(3, 3, [1,0,0,0,1,0,0,0,1])

#     result = m1 + m2
#     print(result.elements)

#     assert False

def test_adjugated():

    m1 = PrintMatrix(3, 3, [1,2,3,4,5,6,7,8,9])
    
    m1.expand_row_adjugated(0)

    assert False