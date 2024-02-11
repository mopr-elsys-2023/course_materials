from src.matrix import Matrix

class AugmentedMatrix(Matrix):
    
    def __init__(self, rows_count, cols_count, elements, augmentation):
        super().__init__(rows_count, cols_count, elements)
        self.augmentation = augmentation

    def swap_rows(self, row_i, row_j):
        super().swap_rows(row_i, row_j)
        self.augmentation.swap_rows(row_i, row_j)

    def scale_row(self, row_idx, factor):
        super().scale_row(row_idx, factor)
        self.augmentation.scale_row(row_idx, factor)

    def scale_and_add_to(self, row_i, factor, row_j):
        super().scale_and_add_to(row_i, factor, row_j)
        self.augmentation.scale_and_add_to(row_i, factor, row_j)

    def __eq__(self, other):
        return isinstance(other, AugmentedMatrix) and super().__eq__(other) and self.augmentation == other.augmentation

    # def __validate(self):
    #     super().__validate()
    #     self.augmentation.__validate()
    #     assert self.rows_count == self.augmentation.rows_count

    def print(self):
        for row_idx in range(self.rows_count):
            print(self.row(row_idx))
            print(self.augmentation.row(row_idx))

    def gauss(self):
        # self.__validate()

        # nullate below primary diagonal
        for col_idx, col in enumerate(self.cols):
            pivot = col[col_idx]
            for nullate_idx in range(col_idx + 1, self.rows_count):
                self.scale_and_add_to(col_idx, -1 * col[nullate_idx] / pivot, nullate_idx)

        # If should continue

        # TODO: not reversible
        for col_idx, col in reversed(enumerate(self.cols)):
            pivot = col[col_idx]
            for nullate_idx in range(col_idx + 1, 0, -1):
                self.scale_and_add_to(col_idx, -1 * col[nullate_idx] / pivot, nullate_idx)

        # HW по желание
