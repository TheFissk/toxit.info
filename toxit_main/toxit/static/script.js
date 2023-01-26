
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
function dataTab(){

}
