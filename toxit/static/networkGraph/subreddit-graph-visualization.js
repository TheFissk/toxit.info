// create a network
var container = document.getElementById("mynetwork");

var data = {
    nodes: sub_nodes,
    edges: mod_edges,
};

var options = {
    nodes:{
        shape: "box",
        margin: 10,
    }
};

var network = new vis.Network(container, data, options);