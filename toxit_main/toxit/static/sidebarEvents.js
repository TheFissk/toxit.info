let currentX;
let sidebar = document.getElementsByClassName("sidebar");
let handle = document.getElementsByClassName("resizeHandle");
let button = document.getElementsByClassName("btn");
let isResizing = false;

handle[0].addEventListener("mousedown", function(e) {
  isResizing = true;
  currentX = e.clientX;
  button[0].style.transition = "none";
  sidebar[0].style.transition = "none";
});

document.addEventListener("mouseup", function(e) {
  isResizing = false;
  button[0].style.transition = "left 0.4s ease";
  sidebar[0].style.transition = "left 0.4s ease";
});

document.addEventListener("mousemove", function(e) {
  if (!isResizing) return;
  let dx = e.clientX - currentX;
  let newSize = parseFloat(sidebar[0].offsetWidth) + dx;
  let minSize = document.documentElement.clientWidth * 0.18;
  currentX = e.clientX;
  if (newSize > minSize)
    document.documentElement.style.setProperty("--menuSize", newSize + "px");
  else
    document.documentElement.style.setProperty("--menuSize", minSize + "px");
});

sidebar[0].addEventListener("scroll", function() {
  // Calculate the new position of the handle
  let handleTop = sidebar[0].scrollTop + (sidebar[0].offsetHeight - handle[0].offsetHeight) / 2;

  // Update the top position of the handle
  handle[0].style.top = handleTop + "px";
});



//    document.getElementById("radio_sim").addEventListener("click", setEdgeArcWeight);
//    document.getElementById("radio_count").addEventListener("click", setEdgeArcWeight);