// create a network
var container = document.getElementById("mynetwork");

var data = {
    nodes: nodes,
    edges: edges,
};

var options = {
    nodes:{
        shape: "box",
        margin: 10,
    }
};

var network = new vis.Network(container, data, options);