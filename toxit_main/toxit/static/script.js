
//function myFunction(event) {
//  alert("Hello from a static file!");
//  document.getElementById("test").style.fontSize = "10px";
//}
let menuIsOpen = false

function toggleMenu(){
//alert("clicked menu");
    if (menuIsOpen)
    {
        menuIsOpen = false
        document.getElementById("sidebar").style.width = "0px"
    }else
    {
        menuIsOpen = true
        document.getElementById("sidebar").style.width = "250px"
    }
}
function openTab(event, tabName)
    {
//    update content
    var content = document.getElementsByClassName("content");
    var i;
    for (i = 0; i < content.length; i++)
    {
        content[i].style.display = "none";
    }
    document.getElementById(tabName).style.display = "block";
// highlight tab
    tabs = document.getElementsByClassName("tab");
    for (i = 0; i < tabs.length; i++)
    {
        tabs[i].className = tabs[i].className.replace(" active", "");
    }
    evt.currentTarget.className += " active";
}
