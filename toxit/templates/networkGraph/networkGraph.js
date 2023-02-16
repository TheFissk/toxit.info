{% load static %}

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
// var edgeTable = {{ edgeTable|safe }};

// create an array with edges
var edges = new vis.DataSet([
    {% for edge in edge_data %}
        { from: "{{ edge.from_Sub }}", to: "{{ edge.to_Sub }}", width: "{{ edge.label }}"},
    {% endfor %}
]);

// load static component of networkGraph.js
async src="{% static 'networkGraph/networkGraph.js' %}"