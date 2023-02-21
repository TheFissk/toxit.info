// console.log("networkGraph.js loaded!");

var sub_nodes = new vis.DataSet();
var mod_edges = new vis.DataSet();
var author_edges = new vis.DataSet();

var container = document.getElementById("Toxit-SubredditGraph");

var data = {
  nodes: sub_nodes,
  edges: mod_edges,
};

var options = {
    nodes: {
      shape: "circle",
      margin: 10,
      size: 16,
    },
    layout: {
      randomSeed: 69,
    },
    physics: {
      solver: "forceAtlas2Based",
      maxVelocity: 50,
      timestep: 0.35,
      stabilization: {
        enabled: true,
        iterations: 1000,
        updateInterval: 25,
      },
      forceAtlas2Based: {
        gravitationalConstant: -30,
        centralGravity: 0.01,
        springLength: 250,
        springConstant: 0.05,
      },
    },
    clustering: {
      enabled: true,
      clusterNodeProperties: {
        borderWidth: 2,
        shape: "box",
        font: { size: 20 },
      },
    },
  };  

var network = new vis.Network(container, data, options);

// Define a function to update the graph data
function updateGraphData(snapshot_id) {
  var url = '/update_data/' + snapshot_id + '/';
  $.ajax({
    url: url,
    type: 'GET',
    dataType: 'json',
    success: function(data) {
      // Clear the existing data
      sub_nodes.clear();
      mod_edges.clear();
      author_edges.clear();

      // Add the new data
      sub_nodes.add(data.sub_nodes_context);
      mod_edges.add(data.mod_edges_context);
      author_edges.add(data.author_edges_context);
    },
    error: function(xhr, status, error) {
      console.log('Error:', error);
    }
  });
}

// Call the function to update the graph data for the first choice on page load
var firstChoiceValue = $('#snapshot-select option:first').val();
updateGraphData(firstChoiceValue);

// Add event listener to snapshot-select select tag
document.getElementById('snapshot-select').addEventListener('change', function() {
  var snapshot_id = this.value;
  updateGraphData(snapshot_id);
});