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
    document.documentElement.setAttribute("data-theme", "light");
    moonIcon.classList.remove("fa-moon");
    moonIcon.classList.add("fa-sun");
  } else {
    // Dark mode
    document.documentElement.setAttribute("data-theme", "dark");
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