Pace.on("done", function () {
  document.getElementById("frame").style.opacity = "1";
  document.getElementById("frame").style.top = "0";
});

window.onbeforeunload = function () {
  document.getElementById("frame").style.opacity = "0";
  document.getElementById("frame").style.top = "30px";
};