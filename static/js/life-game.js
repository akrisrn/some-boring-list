var row_count = 100;
var col_count = 100;
var board = [];
var p, min, max, inc, sh;
var gen;

function randint(min, max) {
  return parseInt(function (min, max) {
      max = max || 1;
      min = min || 0;
      Math.seed = (Math.seed * 9301 + 49297) % 233280;
      var rnd = Math.seed / 233280.0;
      return min + rnd * (max - min);
    }() * (max - min + 1));
}

function init() {
  for (var i = 0; i < row_count; i++) {
    board[i] = [];
    for (var j = 0; j < col_count; j++) {
      board[i][j] = 0;
    }
  }
  var life_count = parseInt(row_count * col_count * p);
  for (var k = 0; k < life_count; k++) {
    while (true) {
      var rand_row = randint(0, self.row_count - 1);
      var rand_col = randint(0, self.col_count - 1);
      if (board[rand_row][rand_col] == 0) {
        board[rand_row][rand_col] = 1;
        break
      }
    }
  }
  gen = 0;
  $("#gen").text("Gen " + gen);
  return board;
}

function check_around(x, y) {
  var alive_count = 0;
  for (var i = -1; i <= 1; i++) {
    for (var j = -1; j <= 1; j++) {
      var x_n = x + i;
      var y_n = y + j;
      if (x_n < 0) {
        x_n = col_count - 1
      }
      if (x_n >= col_count) {
        x_n = 0
      }
      if (y_n < 0) {
        y_n = row_count - 1
      }
      if (y_n >= row_count) {
        y_n = 0
      }
      if (i == 0 && j == 0) {
        continue
      }
      if (board[y_n][x_n] == 1) {
        alive_count += 1
      }
    }
  }
  return alive_count
}

function update() {
  var new_board = [];
  for (var i = 0; i < row_count; i++) {
    new_board[i] = [];
    for (var j = 0; j < col_count; j++) {
      new_board[i][j] = board[i][j];
      var alive_count = check_around(j, i);
      if (board[i][j] == 1) {
        if (alive_count < min || alive_count > max) {
          new_board[i][j] = 0
        }
      } else {
        if (alive_count == inc) {
          new_board[i][j] = 1
        }
      }
    }
  }
  $("#gen").text("Gen " + ++gen);
  board = new_board;
  return board
}

function render(board) {
  var i = 0, j = 0;
  $("td").each(function () {
    if (board[i][j] == 1) {
      $(this).css("background", "gray")
    } else {
      $(this).css("background", "white")
    }
    j++;
    if (j >= col_count) {
      j = 0;
      i++;
    }
  });
}

function init_val() {
  p = parseInt($("#p").val()) / 100.0;
  min = parseInt($("#min").val());
  max = parseInt($("#max").val());
  inc = parseInt($("#inc").val());
  var seed = $("#seed").val();
  if (seed == "") {
    seed = parseInt(Math.random() * 100000000) + "";
    $("#seed").attr("placeholder", seed);
  }
  Math.seed = parseInt(encodeURIComponent(seed.replace(/[a-z|A-Z]/g, function ($1) {
    return $1.charCodeAt(0);
  })).replace(/%/g, ''), 16);
}

$(function () {
  init_val();
  var table = $("<table></table>");
  for (var i = 0; i < row_count; i++) {
    var tr = $("<tr></tr>");
    for (var j = 0; j < col_count; j++) {
      tr.append($("<td></td>"))
    }
    table.append(tr)
  }
  $("#life-game").append(table);
  render(init());
  var start = $("#start");
  var pause = $("#pause");
  var reset = $("#reset");
  pause.attr({"disabled": "disabled"});
  start.bind("click", function () {
    sh = setInterval('render(update())', 100);
    start.attr({"disabled": "disabled"});
    pause.removeAttr("disabled")
  });
  pause.bind("click", function () {
    clearInterval(sh);
    start.removeAttr("disabled");
    pause.attr({"disabled": "disabled"})
  });
  reset.bind("click", function () {
    clearInterval(sh);
    start.removeAttr("disabled");
    pause.attr({"disabled": "disabled"});
    init_val();
    render(init());
  })
});
