/*
  This file hosts all the static information related to the side menu functionality
  it handles, opening the menu, iteractions with the menu, and interactions with the
  menu that interact with visjs. 
*/



// factory design pattern javascript handler 

/*
  export factory javascript and ajax
    allows only one file of each type to be downloaded at a time
    utilizes factory design pattern to handle filetype and data conversion
    
    all data begins as a python dict object when pulled from models.py and is
    assembled in views.py for deliver to the factory which then finializes the
    data into the correct datatype before naming and exporting it to the user
*/ 
// variable to track what is exporting 
let isExporting = {};

function exportData(exportType) {
  // check if exporting is already in progress for this type
  if (isExporting[exportType]) {
    console.log(`Export of ${exportType} is already in progress.`);
    return;
  }

  // mark exporting as in progress for this type
  isExporting[exportType] = true; 

  // Show spinner
  let spinner = document.querySelector(`span.generic-button[onclick="exportData('${exportType}')"] i.fa-spinner`);
  spinner.style.display = 'inline-block';

  // initialize snapshotId and Url variables for later use
  const snapshotId = document.querySelector('#export-data-select').value; // collect the id of the dataset we want to download 
  const url = `/export_data/${snapshotId}/${exportType}`; // construct the appropriate url for export factory 

  // handle ajax fetch request
  fetch(url)
    .then(response => {
      if (!response.ok) {
        throw new Error('Export failed');
      }
      return response.blob();
    })
    .then(blob => {
      // set up the filename and download link 
      const filename = `Snapshot_${snapshotId}.${exportType}`;
      // create a fake link element to trigger the download
      const link = document.createElement('a');
      // bind the data to contructed link element 
      link.href = window.URL.createObjectURL(blob);
      // assign filename
      link.download = filename;
      // trigger downloading the file from the artificial element we built
      link.click();
    })
    .catch(error => {
      // log the error
      console.error(error);
    })
    .finally(() => {
      // hide export spinner 
      isExporting[exportType] = false; // mark exporting as complete for this type
      spinner.style.display = ''; // hide spinner on completion 
    });
}



// basic side nav functionaity 

/* 
  Open Close Side Nav Logic
    handles toggling the side nav with the side nav toggle button
*/
// function to toggle the side nav
const sidebarBtn = $(".sidebar-btn");
const sidebar = $(".sidebar");

sidebarBtn.click(function () {
  toggleSideNav();
});

function toggleSideNav() {
  sidebarBtn.toggleClass("click");
  sidebar.toggleClass("show");
}

/* 
  Collapse / Display nav modules 
    this is what makes the side nav submenus able to collapse and open on click
*/
$(".main_side").on("click", ".item-text", function() {
  var id = $(this).attr("id");
  $(".collapsible.item-show-" + id).toggleClass("show");
  if(id != 'export-factory') $(".main_side li #" + id + " span").toggleClass("rotate");
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



// minimize animation

/*
  Middle mouse and minimize button fit network 
*/

// animation function for fitting the current visjs network content on screen
// used by middle mouse and minimize button
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

// Middle mouse
$(".content").on("mousedown", function(event) {
  // Middle mouse button clicked
  if (event.which === 2) {
    handleNetworkFit();
  }
});

// Minimize button
$(".fa-minimize").on("click", function(event) {
  // Left mouse button clicked
  if (event.button === 0) {
    handleNetworkFit();
  }
});



// data manipulation

/*
  Snapshot selection drop down logic
    Calls ajax to grab new data and handles initial loading of first snapshot
    ajax for updating the graph is in the visjs javascript static file: toxit\static\networkGraph\subreddit-graph-data.js
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
  Edge Weigh selector radio button code
    alter the visjs edge data between the two different edge weight data
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



// drag and drop side menu items

/*
  draggable item code modified from https://codepen.io/PJCHENder/pen/PKBVRO/
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





// Originially we planned to have more configuration options but the visjs service provider has been exerpiencing issues
// The remaining code was left in place to show the jquery that hijacked visjs's default config code to add even more functionality
// specifically it converted poorly made html into nice and oragnized drop down lists as well as added icons and made everything prettier

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