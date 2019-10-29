from ortools.sat.python import cp_model


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
    sudoku_size = 9
    all_rows = range(sudoku_size)
    all_cols = range(sudoku_size)

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


def sudoku_solver(to_solve_sudoku):
    """ solve a sudoku

    Solve the sudoku given in parameter with the goold or-tools library
    """

    # -------------------------------------
    #       MODEL DEFINITION
    # -------------------------------------
    model = cp_model.CpModel()

    # -------------------------------------
    #       VARIABLES DEFINITION
    # -------------------------------------
    sudoku_size = 9
    all_rows = range(sudoku_size)
    all_cols = range(sudoku_size)

    sudoku = [[None for i in range(sudoku_size)] for i in range(sudoku_size)]
    for row in all_rows:
        for col in all_cols:
            sudoku[row][col] = model.NewIntVar(1, sudoku_size, 'sudoku_row%i_col%i' % (row, col))

    # -------------------------------------
    #       SUDOKU RULES DEFINITION
    # -------------------------------------
    # in each line, the numbers are all different
    for row in all_rows:
        all_var_in_row = []
        for col in all_cols:
            all_var_in_row.append(sudoku[row][col])

        model.AddAllDifferent(all_var_in_row)

    # in each column, the numbers are all different
    for col in all_cols:
        all_var_in_col = []
        for row in all_rows:
            all_var_in_col.append(sudoku[row][col])

        model.AddAllDifferent(all_var_in_col)

    # in each square, the number are all different
    for num_row_square in range(3):
        for num_col_square in range(3):
            square_start_row = num_row_square * 3
            square_start_col = num_col_square * 3

            square = []
            for row in range(square_start_row, square_start_row + 3):
                for col in range(square_start_col, square_start_col + 3):
                    square.append(sudoku[row][col])

            model.AddAllDifferent(square)

    # ---------------------------------------------
    #     SET THE CURRENT STATE OF THE SUDOKU
    # ---------------------------------------------
    for row in all_rows:
        for col in all_cols:
            if to_solve_sudoku[row][col] != 0:
                model.Add(sudoku[row][col] == to_solve_sudoku[row][col])

    # -------------------------------------
    #       SOLVE THE SUDOKU
    # -------------------------------------
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    # ---------------------------------------------
    #      MAKE AND RETURN RESULT OF THE SOLVE
    # ---------------------------------------------
    result = dict()
    result['status'] = status

    if status == cp_model.FEASIBLE:
        solved_sudoku = [[None for i in range(sudoku_size)] for i in range(sudoku_size)]
        for row in all_rows:
            for col in all_cols:
                solved_sudoku[row][col] = solver.Value(sudoku[row][col])

        result['sudoku'] = solved_sudoku

    return result

# if __name__ == '__main__':
#     sudoku = [
#         [0, 0, 3,   5, 7, 0,   9, 0, 0],
#         [0, 5, 0,   0, 0, 2,   0, 8, 0],
#         [7, 0, 0,   0, 0, 0,   5, 0, 1],
#
#         [3, 0, 0,   0, 0, 7,   0, 5, 0],
#         [2, 0, 0,   0, 0, 0,   0, 0, 6],
#         [0, 7, 0,   2, 0, 0,   0, 0, 8],
#
#         [6, 0, 4,   0, 0, 0,   0, 0, 2],
#         [0, 3, 0,   4, 0, 0,   0, 9, 0],
#         [0, 0, 7,   0, 6, 3,   4, 0, 0]
#     ]
#
#     print_sodoku(sudoku)
#
#     print("The sudoku is full :", end=" ")
#     print(is_sudoku_filled(sudoku))
#
#     print("The sudoku is correct :", end=' ')
#     print(is_sudoku_correct(sudoku))
#
#     solution = sudoku_solver(sudoku)
#
#     if solution['status'] == cp_model.FEASIBLE:
#         print('A solution has ben computed')
#         print_sodoku(solution['sudoku'])
#     else:
#         print("No solution found for this sudoku")
