from django import template

register = template.Library()

@register.simple_tag
def get_sudoku_box(sudoku, row, col):
    return sudoku[row][col]
