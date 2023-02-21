//// create a network
//var container = document.getElementById("mynetwork");
//
//var data = {
//    nodes: nodes,
//    edges: edges,
//};
//
//var options = {
//    nodes:{
//        shape: "box",
//        margin: 10,
//    }
//};
//
//var network = new vis.Network(container, data, options);

// create an array with nodes
      var nodes = new vis.DataSet([
        { id: 1, label: "Node 1" },
        { id: 2, label: "Node 2" },
        { id: 3, label: "Node 3" },
        { id: 4, label: "Node 4" },
        { id: 5, label: "Node 5" },
      ]);

      // create an array with edges
      var edges = new vis.DataSet([
        { from: 1, to: 3 },
        { from: 1, to: 2 },
        { from: 2, to: 4 },
        { from: 2, to: 5 },
        { from: 3, to: 3 },
      ]);

      // create a network
      var container = document.getElementById("mynetwork");
      var data = {
        nodes: nodes,
        edges: edges,
      };
      var options = {};
      var network = new vis.Network(container, data, options);


var button22 = document.getElementById('mybutton');
button22.addEventListener('click', addNode);

var button33 = document.getElementById('mybutton2');
button33.addEventListener('click', removeAllEdges);

      function addNode() {
        var newId = (Math.random() * 1e7).toString(32);
        nodes.add({ id: newId, label: "I'm new!" });
        var edge = { from: newId, to: 1, id: (Math.random() * 1e7).toString(32)};
        edges.add(edge);
      }
       function removeAllEdges() {
            console.log("remove all");
            edges.clear();
      }



function addEdge(edge) {
        try {
          edges.add({
            id: edge.id.value,
            from: edge.from.value,
            to: edge.to.value,
          });
        } catch (err) {
          alert(err);
        }
      }
       function removeEdge(edge) {
        try {
          edges.remove({ id: edge.id.value });
        } catch (err) {
          alert(err);
        }
      }
//      function updateEdge() {
//        try {
//          edges.update({
//            id: document.getElementById("edge-id").value,
//            from: document.getElementById("edge-from").value,
//            to: document.getElementById("edge-to").value,
//          });
//        } catch (err) {
//          alert(err);
//        }
//      }

      function handleButtonClick(){
            //  test stuff
     console.log("test");
    var edges2 = data.edges.get();  // get an array of all edges in the graph
    console.log(edges2[0]);
    for (var i = 0; i < data.edges.length; i++) {

      edges2[i].color = 'red';
    }

    network.setData({nodes: nodes, edges: edges2});  // update the graph with the modified edge data
//    network.redraw();
      }
