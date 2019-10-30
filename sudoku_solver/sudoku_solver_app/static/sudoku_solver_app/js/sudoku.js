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

function get_sudoku_json() {
    sudoku = get_sudoku_obj();
    return JSON.stringify(sudoku);
}

$(document).ready(function () {
    $("#sudoku_txt_value").attr("value", get_sudoku_json());

    $("#sudoku tr td").on('change', function () {
        $("#sudoku_txt_value").attr("value", get_sudoku_json());
        console.log( $("#sudoku_txt_value").attr("value"));
    });


    //----------------------------------------

    // fill the sudoku grid
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
                number = "";
                break;
            default:
        }

        if (selected_box != null && number != null) {
            selected_box.text(number);

            // update json string representation of the grid
             $("#sudoku_txt_value").attr("value", get_sudoku_json());
        }

    });
});