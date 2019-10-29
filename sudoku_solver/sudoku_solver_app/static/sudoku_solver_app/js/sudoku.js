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
    });
});