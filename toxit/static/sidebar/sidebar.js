/* 
  Open Close Side Nav Logic
*/
$(".sidebar-btn").click(function () {
  toggleSideNav();
});

// function to toggle the side nav
const sidebarBtn = $(".sidebar-btn");
const sidebar = $(".sidebar");

function toggleSideNav() {
  sidebarBtn.toggleClass("click");
  sidebar.toggleClass("show");
}

/* 
  Collapse / Display nav modules 
*/
$(".item-text").click(function () {
  var id = $(this).attr("id");
  $(".collapsible.item-show-" + id).toggleClass("show");
  $(".main_side li #" + id + " span").toggleClass("rotate");
});

/* 
  Logic to handle toggling dark mode and light mode
*/
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
  Function that creates a button for each edge showing from to node pair
  and handles
    + select to node
    + move to animation for to node
    + repop buttons with to node
    + Logic for auto open selector 
*/
function populateEdgeButtons(fromNode) {
  // get the div element and the network object
  const edgeBtnContainer = document.getElementById("edge-buttons");

  // clear previous data
  edgeBtnContainer.innerHTML = "";

  // if the node exists and has data
  if (fromNode) {
    const from_data = sub_nodes.get(fromNode);

    // get the edges connected to the clicked node
    const connectedNodes = network.getConnectedEdges(fromNode);

    // create a button for each edge and append it to the div element
    connectedNodes.forEach((edgeId) => {
      const connectedNodes = network.getConnectedNodes(edgeId);
      const toNode = connectedNodes.filter((node) => node !== fromNode)[0];
      const to_data = sub_nodes.get(toNode);

      const button = document.createElement("button");
      button.classList.add("edge-button");
      button.innerHTML = `${from_data.subname}<br>to<br>${to_data.subname}`;
      button.addEventListener("click", () => {
        const toNodePosition = network.getPositions([toNode])[toNode];
        const moveToOptions = {
          position: toNodePosition,
          scale: 1.0,
          offset: { x: 0, y: 0 },
          animation: {
            duration: 1000,
            easingFunction: "easeInOutQuad",
          },
        };
        network.moveTo(moveToOptions);
        network.selectNodes([toNode]);
        populateEdgeButtons(toNode);
      });
      edgeBtnContainer.appendChild(button);
    });

    /*
      Logic for auto open selector 
    */
    const sidebarBtn = $(".sidebar-btn");
    const sidebar = $(".sidebar");

    // Cache the selectors
    const autoOpenEdgeCheckbox = $("#auto-open-edge");
    const collapsibleDiv = $(".collapsible.item-show-edgeselect");
    const edgeButtonsDiv = $("#edge-buttons");

    // Hide the edge buttons container if no edge buttons are present
    if (connectedNodes.length === 0) {
      collapsibleDiv.removeClass("show");
    }

    // Check if auto open is enabled
    if (autoOpenEdgeCheckbox.is(":checked")) {
      // Toggle the classes if edge buttons were added
      if (connectedNodes.length > 0) {
        sidebarBtn.addClass("click");
        sidebar.addClass("show");
        collapsibleDiv.addClass("show");
      }
    }
  }
}


/* 
  VisJS network on click functionality
*/
network.on("click", function (event) {
  const fromNode = event.nodes[0];

  // Move to the clicked node position with a new animation
  const toNodePosition = network.getPositions([fromNode])[fromNode];
  const moveToOptions = {
    position: toNodePosition,
    scale: 1.0,
    offset: { x: 0, y: 0 },
    animation: {
      duration: 1500, // New animation duration
      easingFunction: "easeInOutCubic", // New animation easing function
    },
  };
  network.moveTo(moveToOptions);

  populateEdgeButtons(fromNode); /* edge buttons and auto open */
});


/* 
  menu-ize visjs config - planned
*/
$(document).ready(function() {
  // Hide all items that do not have the class "vis-config-s0"
  $('.vis-config-item:not(.vis-config-s0)').addClass('hidden');
  
  $('.vis-config-header').click(function() {
    var $parent = $(this).parent(); // Get the parent element of the clicked header
    var $siblings = $parent.nextUntil('.vis-config-s0'); // Get all the siblings until the next header
    $siblings.toggle(); // Toggle the visibility of the siblings
  });
});