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
//
//// create an array with nodes
//      var nodes = new vis.DataSet([
//        { id: 1, label: "Node 1" },
//        { id: 2, label: "Node 2" },
//        { id: 3, label: "Node 3" },
//        { id: 4, label: "Node 4" },
//        { id: 5, label: "Node 5" },
//      ]);
//
//      // create an array with edges
//      var edges = new vis.DataSet([
//        { from: 1, to: 3 },
//        { from: 1, to: 2 },
//        { from: 2, to: 4 },
//        { from: 2, to: 5 },
//        { from: 3, to: 3 },
//      ]);
//
//      // create a network
//      var container = document.getElementById("mynetwork");
//      var data = {
//        nodes: nodes,
//        edges: edges,
//      };
//      var options = {};
//      var network = new vis.Network(container, data, options);
//
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
//
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
//       function removeEdge(edge) {
//        try {
//          edges.remove({ id: edge.id.value });
//        } catch (err) {
//          alert(err);
//        }
//      }
////      function updateEdge() {
////        try {
////          edges.update({
////            id: document.getElementById("edge-id").value,
////            from: document.getElementById("edge-from").value,
////            to: document.getElementById("edge-to").value,
////          });
////        } catch (err) {
////          alert(err);
////        }
////      }
//
//      function handleButtonClick(){
//            //  test stuff
//     console.log("test");
//    var edges2 = data.edges.get();  // get an array of all edges in the graph
//    console.log(edges2[0]);
//    for (var i = 0; i < data.edges.length; i++) {
//
//      edges2[i].color = 'red';
//    }
//
//    network.setData({nodes: nodes, edges: edges2});  // update the graph with the modified edge data
////    network.redraw();
//      }

//let test = '<svg width="100" height="100">
//   <circle cx="50" cy="50" r="40" stroke="green" stroke-width="4" fill="yellow" />
//   <text x="50" y="50" font-size="16" text-anchor="middle">Hello, World!</text>
//   Sorry, your browser does not support inline SVG.
//</svg> '

//document.addEventListener('DOMContentLoaded', function() {
//
//  var container = document.getElementById("mynetwork");
//
//  var data = {
//    nodes: [
//{
//  id: 1,
//  shape: 'image',
//  image: 'https://lenguajehtml.com/img/html5-logo.png',
//  label: 'HTML5'
//},
//{
//  id: 2,
//  shape: 'image',
//  image: 'https://lenguajecss.com/img/css3-logo.png',
//  label: 'CSS3'
//},
//{
//  id: 3,
//  shape: 'image',
//  image: 'http://ryanchristiani.com/wp-content/uploads/2015/06/js-logo.png',
//  label: 'JS'
//},
//{
//  id: 4,
//  shape: 'image',
//  image: 'http://www.freeiconspng.com/uploads/less-icon-17.png',
//  label: 'LESS'
//},
//{
//  id: 5,
//  shape: 'image',
//  image: 'https://static.raymondcamden.com/images/2016/11/pug.png',
//  label: 'PUG'
//},
//{
//  id: 6,
//  shape: 'image',
//  image: 'https://cdn-images-1.medium.com/max/529/1*XmHUL5DeySv_dGmvbPqdDQ.png',
//  label: 'Babel'
//},
//{
//  id: 7,
//  shape: 'image',
//  image: 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/bc/PostCSS_Logo.svg/2000px-PostCSS_Logo.svg.png',
//  label: 'PostCSS'
//},
//{
//  id: 8,
//  shape: 'image',
//  image: 'http://www.unixstickers.com/image/cache/data/stickers/bootstrap/xbootstrap.sh-340x340.png.pagespeed.ic.rjul6vd1jk.png',
//  label: 'Bootstrap'
//}
//    ],
//    edges: [
//      {from: 1, to: 2},
//      {from: 1, to: 3},
//      {from: 2, to: 4},
//      {from: 1, to: 5},
//      {from: 3, to: 6},
//      {from: 2, to: 7},
//      {from: 2, to: 8}
//    ]
//  }
//
//  var options = {
//    nodes: {
//      borderWidth:0,
//      size:42,
//      color: {
//        border: '#222',
//        background: 'transparent'
//      },
//      font: {
//        color: '#111',
//        face: 'Walter Turncoat',
//        size: 16,
//        strokeWidth: 1,
//        strokeColor: '#222'
//      }
//    },
//    edges: {
//      color: {
//        color: '#CCC',
//        highlight: '#A22'
//      },
//      width: 3,
//      length: 275,
//      hoverWidth: .05
//    }
//  }
//
//  var network = new vis.Network(container, data, options);
//
//});



document.addEventListener('DOMContentLoaded', function() {
     var nodes = null;
      var edges = null;
      var network = null;

      var DIR = 'img/refresh-cl/';
        var thisName = "CUSTOM";
        var toxicity = 0.725;
      var svg = '<svg xmlns="http://www.w3.org/2000/svg" width="250" height="65">' +
          '<rect x="0" y="0" width="100%" height="100%" fill="hsl(' +(60 - 60 * toxicity)+', 100%, 50%)" stroke-width="2" stroke="black" ></rect>' +
          '<foreignObject x="0" y="20%" width="100%" height="100%">' +
              '<div xmlns="http://www.w3.org/1999/xhtml" style="font-family:Arial; font-size:30px; text-align: center; ">' +
              "Toxicity: " + toxicity +
              '</div>' +
          '</foreignObject>' +
          '</svg>';


      var url = "data:image/svg+xml;charset=utf-8,"+ encodeURIComponent(svg);

// Create a data table with nodes.
            nodes = [];

            // Create a data table with links.
            edges = [];

            nodes.push({id: 1, label: 'Get HTML', image: url, shape: 'image'});
            nodes.push({id: 2, label: 'Using SVG', image: url, shape: 'image'});
            edges.push({from: 1, to: 2, length: 300});

            // create a network
//            var container = this.svgNetworkContainer.nativeElement;

            var container = document.getElementById('mynetwork');
            var data = {
                nodes: nodes,
                edges: edges
            };
            var options = {
                physics: {stabilization: false},
                edges: {smooth: false}
            };
            //network = new vis.Network(container, data, options);
            this.network = new vis.Network(container, data, options);
  }
 )