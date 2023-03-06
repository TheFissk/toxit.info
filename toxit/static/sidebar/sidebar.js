$('.sidebar-btn').click(function () {
  $(this).toggleClass("click");
  $('.sidebar').toggleClass("show");
});


$('.item-text').click(function () {
  var id = $(this).attr('id');
  $('.collapsible.item-show-' + id).toggleClass("show");
  $('.main_side li #' + id + ' span').toggleClass("rotate");  
});


$('.main_side li').click(function () {
  $(this).addClass("active").siblings().removeClass("active");
});