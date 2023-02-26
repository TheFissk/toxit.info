let currentX;
let sidebar = document.getElementsByClassName("sidebar");
let handle = document.getElementsByClassName("resizeHandle");
let button = document.getElementsByClassName("btn");
let isResizing = false;
//Initialize --menuSize
document.documentElement.style.setProperty("--menuSize", "20vw");

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


//Sidebar Hamburger Button
$('.btn').click(function(){
           $(this).toggleClass("click");
           $('.sidebar').toggleClass("show");
         });

//Sidebar Tab Title
$('.sidebar ul li a').click(function(){
    var id = $(this).attr('id');
    $('nav ul li ul.item-show-'+id).toggleClass("show");
    $('nav ul li #'+id+' span').toggleClass("rotate");

});

$('nav ul li').click(function(){
 $(this).addClass("active").siblings().removeClass("active");
});
