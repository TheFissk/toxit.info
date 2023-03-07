$('.sidebar-btn').click(function () {
  $(this).toggleClass("click");
  $('.sidebar').toggleClass("show");
});

$('.item-text').click(function () {
  var id = $(this).attr('id');
  $('.collapsible.item-show-' + id).toggleClass("show");
  $('.main_side li #' + id + ' span').toggleClass("rotate");  
});

const darkLightMode = document.getElementById("dark-light-mode");
const moonIcon = document.getElementById("moon-icon");

// Set the default icon to fa-moon
moonIcon.classList.add("fa-moon");

darkLightMode.addEventListener("change", () => {
  if (darkLightMode.checked) {
    // Light mode
    moonIcon.classList.remove("fa-moon");
    moonIcon.classList.add("fa-sun");
  } else {
    // Dark mode
    moonIcon.classList.remove("fa-sun");
    moonIcon.classList.add("fa-moon");
  }
});

// $(document).ready(function() {
//   $('#bg-pic-select').hide();

//   $('input[name="themestyle-radio"]').change(function() {
//       if ($('#bg-pic').is(':checked')) {
//           $('#bg-pic-select').show();
//       } else {
//           $('#bg-pic-select').hide();
//       }
//   });
// });

// $('.main_side li').click(function () {
//   var isActive = $(this).hasClass("active");
//   var hasShow = $(this).children('div').hasClass("show");

//   // Remove active class from all li elements if no child has the class show
//   if (!hasShow) {
//     $('.main_side li').removeClass("active");
//     return;
//   }
  
//   // Add or remove active class based on current state
//   if (!isActive) {
//     $(this).addClass("active").siblings().removeClass("active");
//   } else {
//     $(this).removeClass("active");
//   }
// });