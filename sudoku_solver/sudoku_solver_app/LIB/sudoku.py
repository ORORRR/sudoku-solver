def is_sudoku_correct(sudoku):
    # check that the sudoku is a 9*9 square
    if len(sudoku) != 9:
        return False
    for row in sudoku:
        if len(row) != 9:
            return False

    # check that the sudoku only contains values between 1 and 9
    # (and 0 for the undefined boxs)
    for row in sudoku:
        for col in row:
            if col < 0 or col > 9:
                return False

    # check that in each line, the numbers are all different
    for row in sudoku:
        for i in range(len(row)):
            row_without_zero = list(filter((0).__ne__, row))
            row_as_set_without_zero = set(row_without_zero)

            if len(row_as_set_without_zero) != len(row_without_zero):
                return False

    # check that in each column, the numbers are all different
    for num_col in range(len(sudoku)):
        col = []
        for num_row in range(len(sudoku)):
            col.append(sudoku[num_row][num_col])

        col_without_zero = list(filter((0).__ne__, col))
        col_as_set_without_zero = set(col_without_zero)

        if len(col_as_set_without_zero) != len(col_without_zero):
            return False

    # check that in each square, the numbers are all different
    for num_row_square in range(3):
        for num_col_square in range(3):
            square_start_row = num_row_square * 3
            square_start_col = num_col_square * 3

            square = []
            for row in range(square_start_row, square_start_row + 3):
                for col in range(square_start_col, square_start_col + 3):
                    square.append(sudoku[row][col])

            square_without_zero = list(filter((0).__ne__, square))
            square_as_set_without_zero = set(square_without_zero)

            if len(square_as_set_without_zero) != len(square_without_zero):
                return False

    return True


def is_sudoku_filled(sudoku):
    # check that each box is filled with a value between 1 and 9
    for row in sudoku:
        for col in row:
            if col < 1 or col > 9:
                return False
    return True


def print_sodoku(sudoku):
    all_rows = range(9)
    all_cols = range(9)

    for row in all_rows:
        for col in all_cols:
            if sudoku[row][col] == 0:
                print('*', end=' ')
            else:
                print(sudoku[row][col], end=' ')
            if col == 2 or col == 5:
                print('|', end=' ')
        print()
        if row == 2 or row == 5:
            for col in all_cols:
                print('--', end='')
                if col == 2 or col == 5:
                    print('+', end='-')
            print()
