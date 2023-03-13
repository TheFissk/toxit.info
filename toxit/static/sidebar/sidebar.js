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
  Snapshot selection drop down logic
*/
// Call the function to update the graph data for the first choice on page load
var firstChoiceValue = $('#snapshot-select option:first').val();
updateGraphData(firstChoiceValue); // defined in toxit/templates/toxit/networkGraph/subreddit-graph-data.js

// Add event listener to snapshot-select select tag
document.getElementById('snapshot-select').addEventListener('change', function() {
  var snapshot_id = this.value;
  updateGraphData(snapshot_id);
});

/*
  Radio button code
  -descriton here-
*/
$('input[type=radio][name=edge-weight]').change(function() {

  // Store the ID of the currently selected node, if any
  var selectedNode = network.getSelectedNodes()[0];

  if (this.value == 'mods') {
      document.getElementById("mods-radio").checked = true;
      document.getElementById("auth-radio").checked = false;

      data.edges = mod_edges;
  }
  else if (this.value == 'auth') {
    document.getElementById("mods-radio").checked = false;
    document.getElementById("auth-radio").checked = true;

    data.edges = author_edges;
  }

  // Update the network with the new edges
  network.setData(data);

  if(selectedNode) {
    network.selectNodes([selectedNode]);

    selectedNode = network.getSelectedNodes()[0];

    populateEdgeButtons(selectedNode);

    // afterDrawing is what makes this work, waits for edge swap to finish
    network.once("afterDrawing", function() {
      const toNodePosition = network.getPosition([selectedNode]);
      const moveToOptions = {
        position: toNodePosition,
        scale: 1.25,
        offset: { x: 0, y: 0 },
        animation: {
          duration: 1100, // New animation duration
          easingFunction: "easeInOutQuad", // New animation easing function
        },
      };  
      network.moveTo(moveToOptions);
    });
  }
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
    + before and after tag manipulation of edge buttons
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

      // Determine which edge weight radio button is selected
      const edgeWeightRadios = document.getElementsByName("edge-weight");
      let edgeWeight = "mods";
      for (let i = 0; i < edgeWeightRadios.length; i++) {
        if (edgeWeightRadios[i].checked) {
          edgeWeight = edgeWeightRadios[i].value;
          break;
        }
      }
      
      // Set the button text 
      button.innerHTML = `${from_data.subname} [ ${from_data.score} ]<br> to <br>${to_data.subname} [ ${to_data.score} ]`;

      // Set button :before pseudo-element content based on the edge weight and label
      // Get the edge label based on the edge weight
      const edges = (edgeWeight === "mods") ? mod_edges : author_edges;
      const edge = edges.get(edgeId);

      if (edgeWeight === "mods") {
        button.style.setProperty("--before-content", `\'Moderator(s): ${edge.label}\'`);
      } else if (edgeWeight === "auth") {
        button.style.setProperty("--before-content", `\'Comentor(s): ${edge.label}\'`);
      }

      button.addEventListener("click", () => {
        const toNodePosition = network.getPositions([toNode])[toNode];
        const moveToOptions = {
          position: toNodePosition,
          scale: 1.25,
          offset: { x: 0, y: 0 },
          animation: {
            duration: 1100, // New animation duration
            easingFunction: "easeInOutQuad", // New animation easing function
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

    // Toggle show if auto show is enabled and buttons (edges) were added
    if (autoOpenEdgeCheckbox.is(":checked") && edgeBtnContainer.hasChildNodes()) {
      collapsibleDiv.addClass("show");
      sidebarBtn.addClass("click");
      sidebar.addClass("show");
    }
  }
}


/* 
  VisJS network on click functionality
*/
network.on("click", function (event) {
  const fromNode = event.nodes[0];

  if (event.event.button === 1) {
    // Middle mouse button clicked
    console.log("do something");
    network.fit();
  } else {
    // Move to the clicked node position with a new animation
    const toNodePosition = network.getPositions([fromNode])[fromNode];
    const moveToOptions = {
      position: toNodePosition,
      scale: 1.5,
      offset: { x: 0, y: 0 },
      animation: {
        duration: 1100, // New animation duration
        easingFunction: "easeOutCubic", // New animation easing function
      },
    };  
    network.moveTo(moveToOptions);

    populateEdgeButtons(fromNode); /* edge buttons and auto open */
  }
});


/* 
  menu-ize visjs config - unfinished

  this works except for visjs regenerating the html inside,
  I think an array can be used to track what displays and what doesn't
  Any s0 clas item that has a header inside of it is a drop down menu header
  So when the content gets refreshed just check the array to see if the items for the header were open or close
  if clicking make sure to update the array then update from the array to the menu items
*/
// $(document).ready(function() {
//   var menuState =  Array($('.vis-config-s0 .vis-config-header').length).fill(false); // Array to track menu state for each s0 item
//   console.log(menuState)

//   // Click handler for .vis-config-s0 items
//   $(document).on('click', '.vis-config-s0', function() {
//     var index = $('.vis-config-s0').index(this); // Get the index of the clicked s0 item
//     var $next = $(this).next(); // Get the next element after the clicked element
//     while ($next.length > 0 && !$next.hasClass('vis-config-s0')) { // Iterate until the next s0 element is found
//       if (index >= 0 && menuState[index]) { // If menu state is true for the clicked s0 item, show the element
//         $next.removeAttr('style');
//       } else { // Otherwise, hide the element
//         $next.attr('style', 'display:none !important');
//       }
//       $next = $next.next(); // Move to the next element
//     }
//     menuState[index] = !menuState[index]; // Toggle the menu state for the clicked s0 item
//   });

//   // Trigger a click event on .vis-config-s0 to hide all the elements on load
//   $('.vis-config-s0').trigger('click');

//   // Add Font Awesome icon to .vis-config-header elements that are children of .vis-config-s0 elements
//   $('.vis-config-s0 .vis-config-header').addClass('fas fa-solid fa-sliders');
// });

