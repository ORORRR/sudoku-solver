$(document).ready(function () {
    update_json_representation_of_sudoku();

    //--------------------------------------
    //     set/unset the selected box
    //--------------------------------------
    let selected_box = null;

    $("#sudoku tr td").on('click', function (event) {
        if (selected_box != null) {
            selected_box.toggleClass('selected-box');
        }
        selected_box = $(event.target);
        selected_box.toggleClass('selected-box');
    });

    $("body").on('click', function (event) {
        if (!$(event.target).parents().is("#sudoku")) {
            if (selected_box != null) {
                selected_box.toggleClass('selected-box');
                selected_box = null;
            }
        }
    });

    //--------------------------------------
    //     user input in a box
    //--------------------------------------
    $(document).keyup(function (event) {

        let key = event.key || event.keyCode;

        let number = null;

        switch (key) {
            case '1':
            case 49:
                number = 1;
                break;
            case '2':
            case 50:
                number = 2;
                break;
            case '3':
            case 51:
                number = 3;
                break;
            case '4':
            case 52:
                number = 4;
                break;
            case '5':
            case 53:
                number = 5;
                break;
            case '6':
            case 54:
                number = 6;
                break;
            case '7':
            case 55:
                number = 7;
                break;
            case '8':
            case 56:
                number = 8;
                break;
            case '9':
            case 57:
                number = 9;
                break;
            case ' ':
            case 32:
            case "Backspace":
            case 8:
            case 48:
            case '0':
                number = "";
                break;
            default:
        }

        if (selected_box != null && number != null) {
            selected_box.text(number);
            update_json_representation_of_sudoku();
        }
    });

    //--------------------------------------
    //     user moves selected box
    //--------------------------------------
    $(document).keyup(function (event) {

        let key = event.key || event.keyCode;

        let direction = null;

        switch (key) {
            case 'ArrowLeft':
            case 37:
                direction = 'left';
                break;
            case 'ArrowUp':
            case 38:
                direction = 'up';
                break;
            case 'ArrowRight':
            case 39:
                direction = 'right';
                break;
            case 'ArrowDown':
            case 40:
                direction = 'down';
                break;
            default:
        }

        if (selected_box != null && direction != null) {
            next_box = next_selected_box(direction, selected_box);

            if (next_box != null) {
                selected_box.toggleClass('selected-box');
                selected_box = next_box;
                selected_box.toggleClass('selected-box');
            }
        }
    })
});

function get_sudoku_obj() {
    let sudoku = [];

    for (let row = 0; row < 9; row++) {
        sudoku.push([]);
        for (let col = 0; col < 9; col++) {
            let box = $(`#sudoku tr:nth-child(${row + 1}) td:nth-child(${col + 1})`).first();

            if (box.text().trim() !== "") {
                sudoku[row].push(parseInt(box.text(), 10));
            } else {
                sudoku[row].push(0);
            }
        }
    }

    return sudoku;
}

function get_sudoku_box(row, col) {
    return null;
}

function get_sudoku_json() {
    sudoku = get_sudoku_obj();
    return JSON.stringify(sudoku);
}

function update_json_representation_of_sudoku() {
    sudoku_validation();
    $("#sudoku_txt_value").attr("value", get_sudoku_json());
}

function sudoku_validation() {
    remove_errors();

    let incorrect = false;
    let sudoku = get_sudoku_obj();

    //check that the sudoku only contains values between 1 and 9
    for (let row = 0; row < 9; row++) {
        for (let col = 0; col < 9; col++) {
            if (sudoku[row][col] < 0 || sudoku[row][col] > 9) {
                set_sudoku_box_as_faulty(row, col);
                incorrect = true;
            }
        }
    }

    //check that in each line, the numbers are all different
    for (let row = 0; row < 9; row++) {
        for (let col1 = 0; col1 < 9; col1++) {
            for (let col2 = 0; col2 < 9; col2++) {
                if (col1 != col2 && sudoku[row][col1] != 0 && sudoku[row][col1] == sudoku[row][col2]) {
                    set_sudoku_line_as_faulty(row);
                    incorrect = true;
                }
            }
        }
    }

    //check that in each column, the numbers are all different
    for (let col = 0; col < 9; col++) {
        for (let row1 = 0; row1 < 9; row1++) {
            for (let row2 = 0; row2 < 9; row2++) {
                if (row1 != row2 && sudoku[row1][col] != 0 && sudoku[row1][col] == sudoku[row2][col]) {
                    set_sudoku_column_as_faulty(col);
                    incorrect = true;
                }
            }
        }
    }

    //check that in each square, the numbers are all different
    for (let num_row_square = 0; num_row_square < 3; num_row_square++) {
        for (let num_col_square = 0; num_col_square < 3; num_col_square++) {
            let square_start_row = num_row_square * 3;
            let square_start_col = num_col_square * 3;

            square = []
            for (let row = square_start_row; row < square_start_row + 3; row++) {
                for (let col = square_start_col; col < square_start_col + 3; col++) {
                    square.push(sudoku[row][col])
                }
            }

            for (let box1 = 0; box1 < 9; box1++) {
                for (let box2 = 0; box2 < 9; box2++) {
                    if (box1 != box2 && square[box1] != 0 && square[box1] == square[box2]) {
                        set_sudoku_square_as_faulty(num_row_square, num_col_square);
                        incorrect = true;
                    }
                }
            }
        }
    }

    if (incorrect) {
        show_error_message();
    }
}

function remove_errors() {
    $(`#sudoku tr td`).removeClass('error-box');
    $('#error_message').hide();
}

function show_error_message() {
    $('#error_message').show();
}

function set_sudoku_line_as_faulty(row) {
    for (let col = 0; col < 9; col++) {
        set_sudoku_box_as_faulty(row, col);
    }
}

function set_sudoku_column_as_faulty(col) {
    for (let row = 0; row < 9; row++) {
        set_sudoku_box_as_faulty(row, col);
    }
}

function set_sudoku_square_as_faulty(row_sqaure, col_square) {
    let square_start_row = row_sqaure * 3;
    let square_start_col = col_square * 3;

    for (let row = square_start_row; row < square_start_row + 3; row++) {
        for (let col = square_start_col; col < square_start_col + 3; col++) {
            set_sudoku_box_as_faulty(row, col);
        }
    }
}

function set_sudoku_box_as_faulty(row, col) {
    $(`#sudoku tr:eq(${row}) td:eq(${col})`).addClass('error-box');
}

function next_selected_box(direction, selected_box) {
    row = selected_box.parent();
    current_row = row.index();
    current_col = selected_box.index();

    switch (direction) {
        case 'left':
            if (current_col > 0) {
                return row.find(`td:eq(${current_col - 1})`);
            }
            break;
        case 'up':
            if (current_row > 0) {
                return $(`#sudoku tr:eq(${current_row - 1}) td:eq(${current_col})`);
            }
            break;
        case 'right':
            if (current_col < 8) {
                return row.find(`td:eq(${current_col + 1})`);
            }
            break;
        case 'down':
            if (current_row < 8) {
                return $(`#sudoku tr:eq(${current_row + 1}) td:eq(${current_col})`);
            }
            break;
        default:
    }

    return null;
}