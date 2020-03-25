from django.shortcuts import render
from django.http import HttpResponseNotFound
import json
from .LIB.sudoku import is_sudoku_correct
from .AI.sudoku import solve

def index(request):
    if request.method == "GET":
        return input_sudoku(request)

    if request.method == "POST":
        return solve_sudoku(request)

    return HttpResponseNotFound('<h1>Page not found</h1>')

def input_sudoku(request):
    sudoku = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],

        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],

        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
    
    return render(request, 'sudoku_solver_app/sudoku_input_form.html', {
        'sudoku': sudoku
    })

def solve_sudoku(request):
    sudoku = json.loads(request.POST['sudoku'])
    solved_sudoku = None
    error = None

    if is_sudoku_correct(sudoku):
        solved_sudoku = solve(sudoku)
    else:
        error = "The sudoku is not correct"

    return render(request, 'sudoku_solver_app/sudoku_result.html', {
        'original_sudoku': sudoku,
        'solved_sudoku': solved_sudoku['sudoku'],
        'error': error
    })
