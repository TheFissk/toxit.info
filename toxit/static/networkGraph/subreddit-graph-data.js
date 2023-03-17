/*
  This JavaScript file provides functionality for a VisJS network graph of subreddits, 
  displaying relationships between them based on shared moderators and comment authors. 
  The graph is populated with data retrieved through an AJAX call using the fetch() method.
  The file defines variables for the subreddits as nodes and shared moderators/comment 
  authors as edges, and initializes an observable VisJS network with customizable options 
  for node/edge appearance and physics simulation. The file also includes an observer 
  pattern implementation for edge button and node information tab updates. The updateGraphData 
  function updates the graph with new data when called, and clears the side menu tabs that 
  need to be reset. Finally, the function also includes functionality for showing a loader 
  while the data is being fetched and handling aborted requests.
*/

// define variables to be populated with updateGraphData ajax call 
var sub_nodes = new vis.DataSet();    /* all subreddits as nodes */
var mod_edges = new vis.DataSet();    /* all shared moderators between sub_nodes as edges */
var author_edges = new vis.DataSet(); /* all shared comment authors between sub_nodes as edges */

// Create the VisJs network with the data retrieved from the 
// const network = new vis.Network(container, data, options);
const network = InitilaizeObservableNetwork();





/*
  This code block creates instances of the EdgeButtonObserver and NodeInfoTabObserver 
  classes, which are defined in the observer.js file. These observers are designed to 
  listen for specific events within the network and update themselves accordingly.
*/
const edgeButtonObserver = new EdgeButtonObserver();
const nodeInfoTabObserver = new NodeInfoTabObserver();
/*
  The code block then adds these observers to the network object's list of observers, 
  allowing them to receive updates from the network. This design pattern follows the 
  observer pattern, in which objects (observers) are notified of changes in another 
  object (the network) and update themselves accordingly.
*/
network.addObserver(edgeButtonObserver);
network.addObserver(nodeInfoTabObserver);





/*
  This function initializes the VisJS network graph by defining the container element, 
  data for the graph, and options for nodes and edges. The ObservableNetwork method is 
  used instead of the standard Network method to enable proper update functionality with 
  the Observer Pattern.
*/
function InitilaizeObservableNetwork() {
  // Get the container element for the network graph
  var container = document.getElementById("Toxit-SubredditGraph");

  // define data for network graph; default edge weight is moderators
  var data = {
    nodes: sub_nodes,
    edges: mod_edges,
  };

  var options = {
    nodes: {
      borderWidth: 2,
      borderWidthSelected: 3,
      margin: 25,
      color: {
        border: "rgba(233,103,36,1)",
        background: "rgba(40,36,34,1)",
        highlight: {
          border: "rgba(233,83,46,1)",
          background: "rgba(94,76,64,1)",
        },
        hover: {
          border: "rgba(233,206,0,1)",
          background: "rgba(107,99,93,1)",
        }
      },
      font: {
        color: "rgba(255,255,255,1)",
        size: 15,
        strokeWidth: 3,
        strokeColor: "rgba(0,0,0,1)",
        face: "verdana",
        align: "center",
        vadjust: 15,
      },
      scaling: {
        min: 15,
        max: 30,
      },
      shape: "circle",
      shapeProperties: {
        borderRadius: 5,
      },
      size: 25
    },
    edges: {
      smooth: {
        forceDirection: "none",
      },
      font: {
        color: "rgba(255,255,255,1)",
        size: 20,
        strokeWidth: 3,
        strokeColor: "rgba(0,0,0,1)",
        face: "verdana",
      },
    },
    interaction: {
      hover: true,
    },
    layout: {
      randomSeed: 69420, /* nice */
      improvedLayout:true,
      clusterThreshold: 150,
    },
    physics: {
      stabilization: {
        iterations: 2500,
        fit: true,
      },
      forceAtlas2Based: {
        gravitationalConstant: -200,
        centralGravity: 0.01,
        springLength: 200,
        springConstant: 0.03,
        damping: 0.4,
        avoidOverlap: 1,
      },
      maxVelocity: 50,
      minVelocity: 0.1,
      solver: "forceAtlas2Based",
    },
    configure: {
      enabled: true,
      // unpckg updated and broke color picker for nodes and edges
      // filter: 'nodes,edges,physics',
      filter: 'physics',
      container: document.getElementById('vis-config'),
      showButton: false,
    },  
  };

  /*    
    Using ObservableNetwork instead of the standard Network method enables the Observer 
    Pattern to be used with VisJS, allowing for proper update functionality of each 
    observer. This is because ObservableNetwork is designed to work specifically with the 
    Observer Pattern, whereas Network is not.
  */
  return new ObservableNetwork(container, data, options);
}



/*
  Ajax function using fetch to update the data shown on the graph.

  This is called on load using the snapshot selector to get the default edge weight choice.

  views.py defines a function that packages the nodes in a data json object 
  
  clears the current variable data before loading in the new 'snapshot'
  data into each respective variable, this function updates the VisJS
  network automatically without needing to call an update to the canvas
  or graph or network (the displayed nodes).
*/
var lastSuccessfulSnapshot = $('#snapshot-select').val(); // store the current value of the dropdown before making the AJAX request

const updateGraphData = (snapshot_id) => {
  // start by clearing data of side menu tabs that need to be cleared

  // check if the edge selector exists and clear it too if it does
  $("#edge-buttons").html() ? $("#edge-buttons").html('') : null;

  // grab node info items and reset them if they exist 
  const nodeInfoContent = document.querySelector('.node-info-content'); // get the .node-info-content element
  nodeInfoContent.innerHTML = ""; // clear the contents of .node-info-content
  const link2reddit = document.querySelector('#link2reddit'); // get the link element
  link2reddit.innerHTML = ""; // clear previous link

  // Construct the URL for the data endpoint based on the selected snapshot
  var url = '/get_network_data/' + snapshot_id + '/';
  var $loader = $('#loader');

  // Initialize controller variable
  var controller = new AbortController();

  // Show the loader while the data is being fetched
  $loader.show();

  // clear the contents of .node-info-content
  document.querySelector('.node-info-content').innerHTML = ""; 

  // Use fetch() to get the data and handle it with Promises
  fetch(url, { signal: controller.signal })
    .then(response => response.json())
    .then(data => {
      // Hide the loader once the data has been loaded
      $loader.hide();

      // Clear the existing data
      sub_nodes.clear();
      mod_edges.clear();
      author_edges.clear();

      // Add the new data
      sub_nodes.add(data.sub_nodes_context.map(node => {
        return {
          id: node.id,
          label: node.label,
          title: node.title,
          subname: node.subname,
          score: node.score,
        };
      }));

      mod_edges.add(data.mod_edges_context);
      author_edges.add(data.author_edges_context);

      lastSuccessfulSnapshot = $('#snapshot-select').val(); // update variable for loader cancel 

      // Call the function to set the data after a delay
      delaySetData(data);
    })
    .catch(error => {
      $loader.hide(); // Hide the loader in case of an error

      console.log('Error:', error);

      $('#snapshot-select').val(lastSuccessfulSnapshot); // set the value of the snapshot dropdown to the last successful snapshot
    });

    // Cancel the request if the loader is clicked
    $loader.click(function() {
    controller.abort();
    $loader.hide();
  });
};

/*
  The "afterDrawing" function of VisJS is slightly flawed and sometimes fires
  off just a bit too fast before data loads, adding a quarter second delay resolves
  the issue with negligable impact to user experience.
*/
function delaySetData(data) {
  setTimeout(function() {
    network.once("afterDrawing", function() {
      network.fit({
        animation: {
          duration: 1000,  // 1 second
          easingFunction: "easeInOutQuad"  // easing function
        }
      });
    });
  }, 250); // 250 milliseconds = 0.25 seconds
}



/*
  Here, the Observer pattern is used to attach the observer objects to the VisJS network 
  object created to render the network graph. Therefore, this file is placed in 
  the toxit\static\networkGraph directory, as it is required for the proper functioning 
  of the network graph's interactive features.
*/

/*
  When a node is deselected this function clears the edge buttons panel and resets the 
  node info tab as there is no longer a selected node and data should not persist.
*/
network.on("deselectNode", () => {
  // clear edge buttons panel 
  const edgeBtnContainer = document.getElementById("edge-buttons");
  edgeBtnContainer.innerHTML = "";

  // clear the info node tab too 
  resetNodeInfoTab();
});

/*
  click function description and how it works with teh observer design pattern
*/
network.on("click", function (event) {
  const fromNode = event.nodes[0];

  if (fromNode !== undefined) {
      const toNodePosition = network.getPositions([fromNode])[fromNode];
      const moveToOptions = {
          position: toNodePosition,
          scale: 1.5,
          offset: { x: 0, y: 0 },
          animation: {
              duration: 1100,
              easingFunction: "easeInOutQuad",
          },
      };

      network.moveTo(moveToOptions);

      const nodeClickEvent = new NodeClickEvent(fromNode);
      network.notifyObservers(nodeClickEvent);
  }
});