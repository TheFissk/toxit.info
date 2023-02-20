console.log("networkGraph.js loaded!");

// dyanmic javascript portion for networkGraph.s that requires the template engine

// create an array with nodes
var nodes = new vis.DataSet([
    // Use an empty string as the default value for `sub.edges` if it is not defined or empty
    // Replace 'old_text' with 'new_text' in the `sub.edges` value
    {% for sub in subs %}
        { id: "{{ sub.subreddit }}", label: "{{ sub.subreddit|default:'failed to load.'|safe }}" },
    {% endfor %}
]);

// create an array with edges
var m_edges = new vis.DataSet([
    {% for edge in edge_m %}
        { from: "{{ edge.from_Sub }}", to: "{{ edge.to_Sub }}", width: "{{ edge.label }}"},
    {% endfor %}
]);

var a_edges = new vis.DataSet([
    {% for edge in edge_a %}
        { from: "{{ edge.from_Sub }}", to: "{{ edge.to_Sub }}", width: "{{ edge.label }}"},
    {% endfor %}
]);

// var test0 = nodes_;
// var test1 = edges_m;
// var test2 = edges_a;