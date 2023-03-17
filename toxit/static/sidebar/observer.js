/*
    This is the functional component to our Observer Design Pattern.
    It acts like a .cpp file for a C++ class, we define the observers with the
    VisJS network as we define and construct the network itself. From there the
    observers are able to reference this file when the necessary implementation
    for the respecitive observe update functions is needed. 
*/

/*
    Here we define our observer class that extends the VisJS Network library to 
    instill our own custom observer for onclick functionality. Practically this
    makes zero sense, because you can just register event listeners to onclick events.
    However this is necessary for the project and to an extent, still improves maintainability.

    It simply contains the basic functionality that an observer design pattern expects. 
    This must be done in javascript because of how it interfaces with out front end, thus
    we cannot create a python file to handle this. 

    ObservableNetwork is effectively our subject, we have no interface for the subject 
    due to the nature of javascript and that there exists no built in interface keyword 
    or conept of interface. We do recreate an abstract / interface object later to 
    better immitate the design patter for observer. 
*/
class ObservableNetwork extends vis.Network {
    // concrete subject
    constructor(container, data, options) {
        super(container, data, options);
        // create an empty array to store observers
        this.observers = [];
    }

    addObserver(observer) {
        // add an observer to the array of observers
        this.observers.push(observer);
    }

    removeObserver(observer) {
        // remove an observer from the array of observers
        this.observers = this.observers.filter((obs) => obs !== observer);
    }

    notifyObservers(event) {
        // loop through observers and trigger an update event
        this.observers.forEach((obs) => obs.update(event));
    }
}



/*
    Abstract and interface both do not exist in javascript, but this
    replicates the behaviour of an interface for observer, specifically
    it creates an onlcick interace observer 
*/
class NodeClickObserver {
    update(node) { 
        // this is what makes this an interface / abstract 
        throw new Error('Cannot instansiate an interface.');
    }
}

// concrete observer 1
class EdgeButtonObserver extends NodeClickObserver {
    update(node) {
        populateEdgeButtons(node);
    }
}

// concrete observer 2
class NodeInfoTabObserver extends NodeClickObserver {
    update(node) {
        populateNodeInfoTab(node);
    }
}



/*
    This is a javascript event object used to construct node objects
    to be used inside of the observer and pass data to the concrete observers.

    this is another biproduct of using javascript, because this is a web app,
    instead of having a getState function that the subject pulls the states in from
    the update passes the state.

    The observer diagram we looked at in class represented more of an "active filter" 
    behaviour from the getState() function that pulls the data in from the observers.
    In our case, we had to build it in reverse (b/c javascript) and our system is more
    of a "passive filter" setup where the observers send their data to the subject.
*/
class NodeClickEvent {
    constructor(node) {
        this.fromNode = node;
    }
}



// VisJs OnClick (& deselect / unclick fucntionality)
// these are the function defintions for the observers established in toxit\static\networkGraph\subreddit-graph-data.js

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
    // unpackage the data sent from subject
    const fromNode = nodeObject.fromNode;

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

                // build toNode into nodeObject with fromnode item because observers are dumb
                // we rebuild the data into a format that replicates the format of the subject
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
    // unpackage the data sent from subject
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