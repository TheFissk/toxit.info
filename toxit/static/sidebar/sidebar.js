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
  Middle mouse fit network 
*/
document.querySelector(".content").addEventListener("mousedown", function(event) {
  if (event.button === 1) {
    // Middle mouse button clicked
    handleNetworkFit();
  }
});

document.querySelector(".fa-minimize").addEventListener("click", function(event) {
  if (event.button === 0) {
    // Left mouse button clicked
    handleNetworkFit();
  }
});

function handleNetworkFit() {
  network.fit({
    animation: {
      duration: 1000,  // 1 second
      easingFunction: "easeInOutQuad"  // easing function
    }
  });

  if ($(".sidebar").hasClass("show")) {
    toggleSideNav();
  }
}


/* 
  Collapse / Display nav modules 
*/
$(".main_side").on("click", ".item-text", function() {
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
  allows the user to change the edge weight displayed between moderators and commenters 
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

        // Update the node info when a new node is selected
        document.querySelector('.node-info-content').innerHTML = to_data.title; 
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

  // Only zoom to node if a node was clicked
  if (fromNode !== undefined) {
    // Move to the clicked node position with a new animation
    const toNodePosition = network.getPositions([fromNode])[fromNode];
    const moveToOptions = {
      position: toNodePosition,
      scale: 1.5,
      offset: { x: 0, y: 0 },
      animation: {
        duration: 1100, // New animation duration
        easingFunction: "easeInOutQuad", // New animation easing function
      },
    };
    network.moveTo(moveToOptions);

    populateEdgeButtons(fromNode); /* edge buttons and auto open */

    const clickedNode = sub_nodes.get(fromNode); // get the clicked node
    const nodeInfoContent = document.querySelector('.node-info-content'); // get the .node-info-content element
    nodeInfoContent.innerHTML = ""; // clear the contents of .node-info-content
    nodeInfoContent.innerHTML = clickedNode.title; // set the clicked node's title as the inner HTML of .node-info-content
  }
});


/*
  draggable test
  https://codepen.io/PJCHENder/pen/PKBVRO/
*/
let elementBeingDragged = null;
let draggables = document.querySelectorAll('.reorderable-list__item');
let dropzones = document.querySelectorAll('.dropzone');

/* Item-Being-Dragged Handlers */
let startDrag = (event) => {
  // console.log('dragging started', event.target.innerHTML);
  // event.target.style.backgroundColor = "rebeccapurple";
  event.dataTransfer.effectAllowed = 'move';
  event.dataTransfer.setData('text/html', event.target.innerHTML);
  elementBeingDragged = event.target;
};

let stopDrag = (event) => {
  event.preventDefault();
  elementBeingDragged = null;
};

/* Dropzone Handlers */
let dragInto = (event) => {
  event.preventDefault();
  event.target.classList.add('-dropzone');
  // console.log('dragInto');
};

let dragOver = (event) => {
  event.preventDefault();
  event.dataTransfer.dropEffect = 'move';
}

let dragOut = (event) => {
  event.preventDefault();
  // console.log('dragOut');
  event.target.classList.remove('-dropzone');
};

let drop = (event) => {
  event.preventDefault();
  event.stopPropagation();
  event.target.classList.remove('-dropzone');

  // Get the dropzone and item that is being dragged into
  let targetDropzone = event.target.closest('.dropzone');
  let itemBeingDragged = elementBeingDragged.closest('.reorderable-list__item');

  // Determine the new position of the item
  let newPosition = 0;
  let sibling = itemBeingDragged.previousElementSibling;
  while (sibling) {
    if (sibling.classList.contains('reorderable-list__item')) {
      newPosition++;
    }
    sibling = sibling.previousElementSibling;
  }

  // Move the item to its new position
  let list = itemBeingDragged.parentNode;
  list.insertBefore(itemBeingDragged, targetDropzone.closest('.reorderable-list__item'));
  for (let i = 0; i < newPosition; i++) {
    list.insertBefore(itemBeingDragged, itemBeingDragged.previousSibling);
  }

  // Reset the elementBeingDragged variable
  elementBeingDragged = null;
};

Array.prototype.forEach.call(dropzones, (dropzone => {
  dropzone.addEventListener('dragenter', dragInto);
  dropzone.addEventListener('dragover', dragOver);
  dropzone.addEventListener('dragleave', dragOut);
  dropzone.addEventListener('drop', drop);
}));
 
Array.prototype.forEach.call(draggables, (item => {
  item.addEventListener('dragstart', startDrag);
  item.addEventListener('dragend', stopDrag);
}));


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
//   cocnsole.log(menuState)

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