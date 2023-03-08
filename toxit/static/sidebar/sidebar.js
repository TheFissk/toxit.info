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


/* 
  edge selector logic 
*/
network.on('click', function(event) {
  // get the div element and the network object
  const edgeBtnContainer = document.getElementById("edge-buttons");

  // clear previous data
  edgeBtnContainer.innerHTML = "";

  // the clicked node
  var node = event.nodes[0];

  // if the node exists and has data
  if (node) {
    var data = sub_nodes.get(node);

    // get the edges connected to the clicked node
    const connectedEdges = network.getConnectedEdges(node);

    // create a button for each edge and append it to the div element
    connectedEdges.forEach((edgeId) => {
      const edge = network.body.edges[edgeId];
      const fromNode = sub_nodes.get(edge.from);
      const toNode = sub_nodes.get(edge.to);
      const fromLabel = fromNode.label;
      const toLabel = toNode.label;
      const button = document.createElement("button");
      button.classList.add("edge-button");
      button.textContent = fromLabel + " to " + toLabel;
      edgeBtnContainer.appendChild(button);
    });

    // toggle show if auto show is enabled and buttons (edges) were added
    // Cache the selectors
    const autoOpenEdgeCheckbox = $('#auto-open-edge');
    const collapsibleDiv = $('.collapsible.item-show-edgeselect');
    const edgeButtonsDiv = $('#edge-buttons');

    // toggle show if auto show is enabled and buttons (edges) were added
    if (autoOpenEdgeCheckbox.is(':checked') && !collapsibleDiv.hasClass('show')) {
      edgeButtonsDiv.html().length > 0 ? collapsibleDiv.addClass('show') : collapsibleDiv.removeClass('show');
    } 
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