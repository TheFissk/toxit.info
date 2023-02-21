// // create a network
// var container = document.getElementById("Toxit-SubredditGraph");

// var data = {
//     nodes: sub_nodes,
//     edges: mod_edges,
// };

// var options = {
//     nodes:{
//         shape: "box",
//         margin: 10,
//     }
// };

// var network = new vis.Network(container, data, options);



// Functions to add/remove edges/Nodes
//
//var button22 = document.getElementById('mybutton');
//button22.addEventListener('click', addNode);
//
//var button33 = document.getElementById('mybutton2');
//button33.addEventListener('click', removeAllEdges);
//
//      function addNode() {
//        var newId = (Math.random() * 1e7).toString(32);
//        nodes.add({ id: newId, label: "I'm new!" });
//        var edge = { from: newId, to: 1, id: (Math.random() * 1e7).toString(32)};
//        edges.add(edge);
//      }
//       function removeAllEdges() {
//            console.log("remove all");
//            edges.clear();
//      }
//
//function addEdge(edge) {
//        try {
//          edges.add({
//            id: edge.id.value,
//            from: edge.from.value,
//            to: edge.to.value,
//          });
//        } catch (err) {
//          alert(err);
//        }
//      }