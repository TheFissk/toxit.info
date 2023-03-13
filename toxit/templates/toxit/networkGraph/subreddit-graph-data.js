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
  // Define the appearance and behavior of the nodes
  nodes: {
    shape: "circle",
    margin: 10,
    size: 16,
    borderWidth: 3,
    // shapeProperties: {
    //   interpolation: false    // 'true' for intensive zooming
    // },
  },
  // Define the appearance and behavior of the edges
  edges: {
    font: {
      size: 24,
      align: 'middle'
    },
    hoverWidth: 1,
    selectionWidth: 1,
    width: 0.5,

  },
  // Define the physics properties of the network graph
  physics: {
    stabilization: {
      iterations: 2500,  // maximum number of iteration to stabilize the graph
      fit: true  // fit the graph to the viewport
    },
    forceAtlas2Based: {
      gravitationalConstant: -200,
      centralGravity: 0.01,
      springLength: 200,
      springConstant: 0.03,
      damping: 0.4,
      avoidOverlap: 1  // prevents node overlap, may make nodes more spread out
    },
    maxVelocity: 50,  // the maximum velocity of nodes during physics simulation
    minVelocity: 0.1,  // the minimum velocity of nodes during physics simulation
    solver: 'forceAtlas2Based'  // which solver to use for the physics simulation
  },
  configure: {
    enabled: true,
    filter: true,
    container: document.getElementById('vis-config'),
    showButton: true
  },
};

// Create the VisJs network with the data retrieved from the 
var network = new vis.Network(container, data, options);

// rudimentry function to start with for coloring nodes based on toxicity
function getColorForScore(score) {
  var red = Math.max(0, Math.min(255, Math.round((1 - score) * 100)));
  var green = Math.max(0, Math.min(255, Math.round((score + 1) * 200)));
  return 'rgb(' + red + ',' + green + ',0)';
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
const updateGraphData = (snapshot_id) => {
  // Construct the URL for the data endpoint based on the selected snapshot
  var url = '/update_data/' + snapshot_id + '/';
  var $loader = $('#loader');

  // Show the loader while the data is being fetched
  $loader.show();

  // Use fetch() to get the data and handle it with Promises
  fetch(url)
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
          color: { background: getColorForScore(node.score) }
        };
      }));

      mod_edges.add(data.mod_edges_context);
      author_edges.add(data.author_edges_context);

    })
    .catch(error => {
      $loader.hide(); // Hide the loader in case of an error

      console.log('Error:', error);
    });
};

// text background code