let wall_l = 1;
let wall_w = 1;
// initialize SVG.js
let draw = SVG().addTo("#drawing");
let text_svg =
  '<svg xmlns="http://www.w3.org/2000/svg" version="1.1" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:svgjs="http://svgjs.com/svgjs" height="81" width="81">';
let maze = null;

const downloadToFile = (content, filename, contentType) => {
  const a = document.createElement("a");
  const file = new Blob([content], { type: contentType });

  a.href = URL.createObjectURL(file);
  a.download = filename;
  a.click();

  URL.revokeObjectURL(a.href);
};

// Load maze
$(document).ready(function () {
  $.ajax({
    type: "GET",
    url: "maze-huge.csv",
    dataType: "text",
    success: function (data) {
      processData(data);
    },
  });
  wall_l = parseInt($("#wall_l").val());
  console.log(wall_l);
  wall_w = parseInt($("#wall_w").val());
  console.log(wall_w);

  $("#wall_l").change(function () {
    wall_l = parseInt($(this).val());
    console.log(wall_l);
    draw_maze();
  });
  $("#wall_w").change(function () {
    wall_w = parseInt($(this).val());
    console.log(wall_w);
    draw_maze();
  });
  $("#draw_maze").on("click", function () {
    draw_maze();
  });
  $("#generate_svg").on("click", function () {
    generate_svg_file();
  });
});

function draw_maze() {
  draw.clear();
  if (!maze) {
    return;
  }
  console.log("Draw maze");
  console.log("wall_l: " + wall_l, "wall_w: " + wall_w);
  draw.height(
    (wall_l * (maze.length - (maze.length % 2))) / 2 +
      (wall_w * (maze.length - (maze.length % 2))) / 2 +
      wall_w
  );
  draw.width(
    (wall_l * (maze[0].length - (maze[0].length % 2))) / 2 +
      (wall_w * (maze[0].length - (maze[0].length % 2))) / 2 +
      wall_w
  );
  let w = wall_w;
  let h = wall_w;

  let curr_x = 0;
  let curr_y = 0;

  for (let r = 0; r < maze.length; r++) {
    text_svg += "<!-- " + r + " -->\n";
    row = maze[r];
    console.log("Row: " + r);
    if (r % 2 == 0) h = wall_w;
    else h = wall_l;

    for (let c = 0; c < maze[0].length; c++) {
      char = row[c];

      if (c % 2 == 0) w = wall_w;
      else w = wall_l;
      let rect = null;
      svg_add = "";
      if (char == "O") {
        // draw.rect(w / 2, h / 2).move(curr_x + w / 4, curr_y + w / 4).fill("#F00");
        rect = draw.rect(w, h).move(curr_x, curr_y).fill("#ff002b");
        // var rect = new Rect().size(w, h).move(curr_x, curr_y).fill("#ff002b").addTo(draw)
        svg_add = rect.svg();
      } else if (char == "X") {
        // rect = draw.rect(w / 2, h / 2).move(curr_x + w / 4, curr_y + w / 4).fill("#0A0");
        rect = draw.rect(w, h).move(curr_x, curr_y).fill("#1a43c9");
        // rect.addTo(draw);
        svg_add = rect.svg();
      } else if (char == "#") {
        // rect = draw.rect(w / 2, h / 2).move(curr_x + w / 4, curr_y + w / 4).fill("#A00");

        rect = draw.rect(w, h).move(curr_x, curr_y).fill("#ff002b");
        // rect.addTo(draw);
        svg_add = rect.svg();
      } else if (char != " ") {
        // draw wall
        rect = draw.rect(w, h).move(curr_x, curr_y).fill("#555");
        // rect.addTo(draw);
        svg_add = rect.svg();
      }
      if (svg_add) {
        text_svg += svg_add;
        text_svg += "\n";
      }
      curr_x += w;
    }
    curr_y += h;

    curr_x = 0;
  }
  console.log("Done drawing");
}

function generate_svg_file() {
  text_svg += "</svg>";
  downloadToFile(text_svg, "svg.svg", "text/plain");
}

function processData(allText) {
  // Process CSV
  let allTextLines = allText.split(/\r\n|\n/); // Split CSV in lines
  let loaded_maze = []; // Array containing

  for (let i = 0; i < allTextLines.length; i++) {
    // Split every line into characters
    let row = allTextLines[i].split(",");
    if (row != "") loaded_maze.push(row); // Add array with characters to maze as a row
  }
  //   console.log(loaded_maze);
  console.log("Maze loaded");
  maze = loaded_maze;
}
