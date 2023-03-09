/* 
  Open Close Side Nav Logic
*/
$(".sidebar-btn").click(function () {
  $(this).toggleClass("click");
  $(".sidebar").toggleClass("show");
});

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
  VisJS network on click functionality
   handles edge selector logic 
*/
network.on("click", function (event) {
  // get the div element and the network object
  const edgeBtnContainer = document.getElementById("edge-buttons");

  // clear previous data
  edgeBtnContainer.innerHTML = "";

  // the clicked node
  const fromNode = event.nodes[0];

  // if the node exists and has data
  if (fromNode) {
    const from_data = sub_nodes.get(fromNode);

    // get the edges connected to the clicked node
    const connectedNodes = network.getConnectedEdges(fromNode);

    // create a button for each edge and append it to the div element
    connectedNodes.forEach((edgeId) => {
      const connectedNodes = network.getConnectedNodes(edgeId);
      const toNode = connectedNodes.filter(node => node !== fromNode)[0];
      const to_data = sub_nodes.get(toNode);
      
      const button = document.createElement("button");
      button.classList.add("edge-button");
      button.innerHTML = `${from_data.subname}<br>to<br>${to_data.subname}`;
      edgeBtnContainer.appendChild(button);
    });

    /*
      Logic for auto open selector 
    */
    // Cache the selectors
    const autoOpenEdgeCheckbox = $("#auto-open-edge");
    const collapsibleDiv = $(".collapsible.item-show-edgeselect");
    const edgeButtonsDiv = $("#edge-buttons");

    // toggle show if auto show is enabled and buttons (edges) were added
    if ( autoOpenEdgeCheckbox.is(":checked") && !collapsibleDiv.hasClass("show") ) {
      
      edgeButtonsDiv.html().length > 0
        ? collapsibleDiv.addClass("show")
        : collapsibleDiv.removeClass("show");
    }
  }
});

/* 
  On Page Load functions
    - Move configuration item into correct tab
*/