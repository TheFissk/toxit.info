console.log("networkGraph.js loaded!");

// dyanmic javascript portion for networkGraph.s that requires the template engine

// create an array with nodes
var sub_nodes = new vis.DataSet([
    // Use an empty string as the default value for `sub.edges` if it is not defined or empty
    // Replace 'old_text' with 'new_text' in the `sub.edges` value
    {% for sub in sub_nodes_context %}
        { id: "{{ sub.subreddit }}", label: "{{ sub.subreddit|default:'failed to load.'|safe }}" },
    {% endfor %}
]);

// create an array with edges
var mod_edges = new vis.DataSet([
    {% for edge in mod_edges_context %}
        { to: {{ sub.to_sub }}, from: {{ sub.from_sub }} },
    {% endfor %}
]);

var author_edges = new vis.DataSet([
    {% for edge in autor_edges_context %}
        { to: {{ sub.to_sub }}, from: {{ sub.from_sub }} },
    {% endfor %}
]);