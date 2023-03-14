/*
  subreddit-graph-data.js

  Holds all the javascript logic for the VisJs network
    - Event listener for changing inference task
    - Ajax for loading subreddit nodes and moderator + commentor edge weights
    - loading icon and cancel logic
*/

// define variables to be populated with updateGraphData ajax call 
var sub_nodes = new vis.DataSet();    /* all subreddits as nodes */
var mod_edges = new vis.DataSet();    /* all shared moderators between sub_nodes as edges */
var author_edges = new vis.DataSet(); /* all shared comment authors between sub_nodes as edges */

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
      // customScalingFunction: function (min, max, total, value) {
      //   var length = value.label.length;
      //   var fontSize = Math.max(10, Math.min(30, 60 / length)); // calculate font size based on length of label
      //   var nodeWidth = length * (fontSize / 2);
      //   return nodeWidth / total;
      // },
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
    filter: true,
    container: document.getElementById('vis-config'),
    showButton: true,
  },
};

// Create the VisJs network with the data retrieved from the 
var network = new vis.Network(container, data, options);

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
  // Construct the URL for the data endpoint based on the selected snapshot
  var url = '/update_data/' + snapshot_id + '/';
  var $loader = $('#loader');

  // Initialize controller variable
  var controller = new AbortController();

  // Show the loader while the data is being fetched
  $loader.show();

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

      // check if the edge selector exists and clear it too if it does
      $("#edge-buttons").html() ? $("#edge-buttons").html('') : null;

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


// Function to set the data with a delay
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