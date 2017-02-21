function show_addDate() {
  document.getElementById('addDate').style.display = "inline";
  document.getElementById('comDate').style.display = "none";
}
function show_comDate() {
  document.getElementById('addDate').style.display = "none";
  document.getElementById('comDate').style.display = "inline";
}
function show_review() {
  var review_style = document.getElementById('review').style;
  if (review_style.display == "" || review_style.display == "none") {
    review_style.display = "inline"
  } else {
    review_style.display = "none"
  }
}
function load() {
  document.getElementById('addDate').children[0].valueAsDate = new Date();
  document.getElementById('comDate').children[0].valueAsDate = new Date();
}
window.onload = load;