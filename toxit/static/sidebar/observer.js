// VisJs OnClick (& deselect / unclick fucntionality)

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

        populateNodeInfoTab(fromNode);
    }
});

/*
add event listener to network object for deselectNode event
*/
network.on("deselectNode", () => {
    // clear edge buttons panel 
    const edgeBtnContainer = document.getElementById("edge-buttons");
    edgeBtnContainer.innerHTML = "";

    // clear the info node tab too 
    resetNodeInfoTab();
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
            button.innerHTML = `r/${from_data.subname} [ ${from_data.score} ]<br> to <br>r/${to_data.subname} [ ${to_data.score} ]`;

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

                // Clear then update the node info when a new node is selected
                resetNodeInfoTab();
                populateNodeInfoTab(toNode);
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

        // Toggle show if auto show is enabled and buttons (edges) were added
        if (autoOpenEdgeCheckbox.is(":checked") && edgeBtnContainer.hasChildNodes()) {
            collapsibleDiv.addClass("show");
            sidebarBtn.addClass("click");
            sidebar.addClass("show");
        }
    }
}


/*
  populate node info tab module code
    when a node is clicked fill info panel tab with node information
    also create a link so the user is able to go to the subreddit
*/
const populateNodeInfoTab = (fromNode) => {
    const clickedNode = sub_nodes.get(fromNode); // get the clicked node
    const nodeInfoContent = document.querySelector('.node-info-content'); // get the .node-info-content element
    nodeInfoContent.innerHTML = ""; // clear the contents of .node-info-content
    nodeInfoContent.innerHTML = clickedNode.title; // set the clicked node's title as the inner HTML of .node-info-content

    const link2reddit = document.querySelector('#link2reddit'); // get the link element
    link2reddit.innerHTML = ""; // clear previous link
    link2reddit.innerHTML = "www.reddit.com/r/" + clickedNode.subname + "/"; // set the innerHTML to the link
    link2reddit.href = "https://" + link2reddit.innerHTML; // set the href attribute to the new link and finish it
}

// helper function to simplify reseting nodeinfo panel dynamic content
const resetNodeInfoTab = () => {
    const nodeInfoContent = document.querySelector('.node-info-content'); // get the .node-info-content element
    nodeInfoContent.innerHTML = ""; // clear the contents of .node-info-content
    const link2reddit = document.querySelector('#link2reddit'); // get the link element
    link2reddit.innerHTML = ""; // clear previous link
}