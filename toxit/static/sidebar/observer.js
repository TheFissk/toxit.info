// VisJs OnClick (& deselect / unclick fucntionality)

/*
  Function that creates a button for each edge showing from to node pair
  and handles
    + select to node
    + move to animation for to node
    + repop buttons with to node
    + Logic for auto open selector 
    + before and after tag manipulation of edge buttons
*/
function populateEdgeButtons(nodeObject) {
    const fromNode = nodeObject.fromNode;

    // get the div element and the network object
    const edgeBtnContainer = document.getElementById("edge-buttons");

    // clear previous data
    edgeBtnContainer.innerHTML = "";

    // if the node exists and has data
    if (fromNode) {
        const from_data = sub_nodes.get(fromNode);
        // console.log(fromNode);
        // console.log(from_data);

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

                // build toNode into nodeObject with fromnode item because observers are dumb
                const toNodeObject = new NodeClickEvent(toNode);

                populateEdgeButtons(toNodeObject);

                // Clear then update the node info when a new node is selected
                resetNodeInfoTab();
                populateNodeInfoTab(toNodeObject);
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
const populateNodeInfoTab = (nodeObject) => {
    const fromNode = nodeObject.fromNode;

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







class ObservableNetwork extends vis.Network {
    subscribe(events, callback, id) {
        // call the subscribe method of the superclass
        super.subscribe(events, callback, id);

        // add your own observer to the array of observers
        const observer = {
            callback: callback,
            eventType: events,
            id: id
        };

        this.observers.push(observer);
    }

    constructor(container, data, options) {
        super(container, data, options);
        this.observers = [];
    }

    addObserver(observer) {
        this.observers.push(observer);
    }

    removeObserver(observer) {
        this.observers = this.observers.filter((obs) => obs !== observer);
    }

    notifyObservers(event) {
        this.observers.forEach((obs) => obs.update(event));
    }
}


class NodeClickObserver {
    update(node) { }
}

class EdgeButtonObserver extends NodeClickObserver {
    update(node) {
        populateEdgeButtons(node);
    }
}

class NodeInfoTabObserver extends NodeClickObserver {
    update(node) {
        populateNodeInfoTab(node);
    }
}


class NodeClickEvent {
    constructor(node) {
        this.fromNode = node;
    }
}