let currentX;
let sidebar = document.getElementsByClassName("sidebar");
let handle = document.getElementsByClassName("resizeHandle");
let button = document.getElementsByClassName("btn");

handle[0].addEventListener("mousedown", function(e) {
  isResizing = true;
  currentX = e.clientX;
});

document.addEventListener("mouseup", function(e) {
  isResizing = false;
});

document.addEventListener("mousemove", function(e) {
  if (!isResizing) return;
  let dx = e.clientX - currentX;
  sidebar[0].style.width = (sidebar[0].offsetWidth + dx) + "px";
  currentX = e.clientX;
  if (parseFloat(sidebar[0].style.width) < (document.documentElement.clientWidth * 0.18))
    sidebar[0].style.width = (document.documentElement.clientWidth * 0.18) + "px";
  button[0].style.width = (parseFloat(sidebar[0].style.width) +
});

    document.getElementById("radio_sim").addEventListener("click", setEdgeArcWeight);
    document.getElementById("radio_count").addEventListener("click", setEdgeArcWeight);