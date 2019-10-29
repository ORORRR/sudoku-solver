from django.shortcuts import render
import json
from .AI.sudoku_AI import is_sudoku_correct, sudoku_solver


def index(request):
    sudoku = None

    if request.method == "POST":
        sudoku = request.POST['sudoku']

    if sudoku is None:
        sudoku = [
            [0, 0, 3, 5, 7, 0, 9, 0, 0],
            [0, 5, 0, 0, 0, 2, 0, 8, 0],
            [7, 0, 0, 0, 0, 0, 5, 0, 1],

            [3, 0, 0, 0, 0, 7, 0, 5, 0],
            [2, 0, 0, 0, 0, 0, 0, 0, 6],
            [0, 7, 0, 2, 0, 0, 0, 0, 8],

            [6, 0, 4, 0, 0, 0, 0, 0, 2],
            [0, 3, 0, 4, 0, 0, 0, 9, 0],
            [0, 0, 7, 0, 6, 3, 4, 0, 0]
        ]

        return render(request, 'sudoku_solver_app/sudoku_input_form.html', {
            'sudoku': sudoku,
            'sudoku_txt': json.dumps(sudoku),
            'sudoku_size_range': range(len(sudoku))
        })

    sudoku = json.loads(sudoku)

    error = None

    # check that the sudoku is correct
    if not is_sudoku_correct(sudoku):
        error = "The sudoku is not correct"

    # solve the sudoku

    solved_sudoku = sudoku_solver(sudoku)

    return render(request, 'sudoku_solver_app/sudoku_result.html', {
        'original_sudoku': sudoku,
        'solved_sudoku': solved_sudoku['sudoku'],
        'error': error,
        'sudoku_txt': json.dumps(solved_sudoku['sudoku']),
        'sudoku_size_range': range(len(sudoku))
    })
