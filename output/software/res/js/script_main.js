var oldColor = "";

$(document).ready(function() {
  changeBackground();
  setInterval(changeBackground, 2000);
});

var changeBackground = function() {
  var newColor;
  do {
    var colorIndex = Math.floor(Math.random() * colorPalette.length);
    newColor = colorPalette[colorIndex];
  }
  while (newColor === oldColor)

  $("body").css("background-color", newColor);

  oldColor = newColor;
}
