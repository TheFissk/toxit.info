var displayMods = Boolean(true); 

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
    shapeProperties: {
      interpolation: false    // 'true' for intensive zooming
    },
  },
  edges: {
    font: {
      size: 24,
      align: 'middle'
    },
    hoverWidth: 0.5,
    selectionWidth: 1,
    width: 0.15,
    smooth: {
      type: 'continuous'
    },
  },
  layout: {
    improvedLayout:false
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
      gravitationalConstant: -69, /* nice */
      centralGravity: 0.01,
      springLength: 42069,
      springConstant: 0.001,
    },
  },
};

var network = new vis.Network(container, data, options);

// Define a function to update the graph data
var updateGraphData = (function() {
  var controller = new AbortController();

  return function(snapshot_id) {
    var url = '/update_data/' + snapshot_id + '/';
    var $loader = $('#loader'); // the loader element, replace with your own

    // cancel previous request if it hasn't already been completed
    controller.abort();
    controller = new AbortController();

     // add event listener to loader element to cancel fetch request
     $loader.click(function() {
      controller.abort();
      $loader.hide();
    });

    // show the loader while the data is being fetched
    $loader.show();

    fetch(url, {
      method: 'GET',
      signal: controller.signal,
    })
      .then(function(response) {
        return response.json();
      })
      .then(function(data) {
        // hide the loader once the data has been loaded
        $loader.hide();

        // Clear the existing data
        sub_nodes.clear();
        mod_edges.clear();
        author_edges.clear();

        // Add the new data
        sub_nodes.add(data.sub_nodes_context);
        mod_edges.add(data.mod_edges_context);
        author_edges.add(data.author_edges_context);
      })
      .catch(function(error) {
        // hide the loader in case of an error
        $loader.hide();

        console.log('Error:', error);
      });
  }
})();

// Call the function to update the graph data for the first choice on page load
var firstChoiceValue = $('#snapshot-select option:first').val();
updateGraphData(firstChoiceValue);

// Add event listener to snapshot-select select tag
document.getElementById('snapshot-select').addEventListener('change', function() {
  var snapshot_id = this.value;
  updateGraphData(snapshot_id);
});

// radio button edge selector logic
$('input[type=radio][name=edge-weight]').change(function() {
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
});

network.on('click', function(event) {
  var node = event.nodes[0];
  if (node) {
    var data = sub_nodes.get(node);
    alert('Subreddit: ' + data.label + '\nDescription: ' + data.title);
  }
});
