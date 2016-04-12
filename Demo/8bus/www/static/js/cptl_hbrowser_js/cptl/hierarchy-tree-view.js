/*
  copyright (c) 2015, Gabriel A. Weaver

  This file is part of the Cyber-Physical Topology Language for the
    Power domain.

  This code is free software:  you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by the
    Free Software Foundation, either version 3 of the License, or 
    (at your option) any later version.

  The Cyber-Physical Topology Language (CPTL):  Electrical Power 
    is distributed in the hope that it will be useful, but 
    WITHOUT ANY WARRANTY; without even the implied warranty of 
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    General Public License for more details.

  You should have received a copy of the GNU General Public License
    along with this program.  If not, see http://www.gnu.org/licenses/    
*/
(function(f){if(typeof exports==="object"&&typeof module!=="undefined"){module.exports=f()}else if(typeof define==="function"&&define.amd){define([],f)}else{var g;if(typeof window!=="undefined"){g=window}else if(typeof global!=="undefined"){g=global}else if(typeof self!=="undefined"){g=self}else{g=this}g.HierarchyTreeView = f()}})(function(){var define,module,exports;return (function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=="function"&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);var f=new Error("Cannot find module '"+o+"'");throw f.code="MODULE_NOT_FOUND",f}var l=n[o]={exports:{}};t[o][0].call(l.exports,function(e){var n=t[o][1][e];return s(n?n:e)},l,l.exports,e,t,n,r)}return n[o].exports}var i=typeof require=="function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s})({1:[function(require,module,exports){

module.exports = (function () {
  'use strict';

    function HierarchyTreeView(config) {
	config = config || {};
	this.config = config;
	this.config.ht = new HierarchyTree();
    }

    HierarchyTreeView.prototype.initialize = function(json_graph_data, json_tree_data) {
	this.config.ht.initialize_graph(json_graph_data);
	this.config.ht.initialize_tree(json_tree_data);
    }

    HierarchyTreeView.prototype.get_vertices_for_leaf = function(self, leaf) {
	var leaf_id = leaf.model.path;
	var vertices = self.config.ht.get_vertices();
	var result_vertices = [];
	
	for (var i=0; i < vertices.length; i++) {
	    var vertex = vertices[i];
	    if ( ("enet:hasDomainNameValue" in vertex) && 
	         (vertex["enet:hasDomainNameValue"] == leaf_id) ) {
		result_vertices.push(vertex);
	    }
	}
	return result_vertices;
    }

    HierarchyTreeView.prototype.get_type_for_node = function( path_value ) {
	var type = null;
	var nodes = this.config.ht.get_nodes( "path", path_value );
	var node = nodes[0];
	type = node.model["rdfs:type"];
	return type;
    };

    HierarchyTreeView.prototype.get_node = function( path_value ) {
	var nodes = this.config.ht.get_nodes("path", path_value );
	var node = nodes[0];
	var node_result = {};

	for (var property_key in node.model) {
	    if ("children" != property_key) {
		node_result[property_key] = node.model[property_key];
	    }
	}
	return node_result;
    };
    
    HierarchyTreeView.prototype.is_hierarchy_tree = function( mapping ) {
	var leaves = this.config.ht.leaves(this.config.ht.config.tree);
	var vertices = this.config.ht.get_vertices();

	var vertex_in_range = {};
	
	// Every leaf is mapped to exactly one vertex
	var leaf_image_cardinality = {};
	for (var i=0; i < leaves.length; i++) {
	    var leaf = leaves[i];
	    if ( mapping(this,leaf).length != 1 ) {
		return false;   // Then the cardinality is greater than one
	    } else {
		var vertex = mapping(leaf)[0];
		if ( !(vertex in vertex_in_range) ) {
		    vertex_in_range[vertex] = 1;
		}
	    }
	}

	// Every vertex is mapped to once
	if ( vertex_in_range.length != vertices.length ) {
	    return false;
	}
	return true;
    };

    function node_to_string(node) {
	return node.model.path;
    }
    
    HierarchyTreeView.prototype.view_partitions_graph = function( view ) {
	var view_array = view.toArray();
	var leaves = new buckets.Set(node_to_string);
	    
	for (var i=0; i < view_array.length; i++) {
	    var node_id = view_array[i];
	    var nodes = this.config.ht.get_nodes( "path", node_id );
	    var node = nodes[0];
	    var node_leaves = this.config.ht.leaves(node);
	    var node_leaves_set = new buckets.Set(node_to_string)
	    for (var j=0; j < node_leaves.length; j++) {
		node_leaves_set.add(node_leaves[j]);
	    }
	    if ( node_leaves_set.intersection(leaves).size() != 0 ) {
		return false;
	    }
	    leaves.union(node_leaves_set);
	}

	var vertices = this.config.ht.get_vertices();
	if (vertices.length != leaves.size()) { return false; }
	return true;
    };

    
    HierarchyTreeView.prototype.view_expand = function(view, x) {
	var nodes = this.config.ht.get_nodes( "path", x );
	var node = nodes[0];
	var children = this.config.ht.children(node);
	for (var i=0; i < children.length; i++) {
	    var child = children[i];
	    var child_id = child.path;
	    view.add(child_id);
	}
	view.remove(x);
	return view;
    };
    
    HierarchyTreeView.prototype.view_contract = function(view, x) {
	var nodes = this.config.ht.get_nodes( "path", x );
	var node = nodes[0];
	var children = this.config.ht.children(node);
	for (var i=0; i < children.length; i++) {
	    var child = children[i];
	    var child_id = child.path;
	    view.remove(child_id);
	}
	view.add(x);
	return view;
    };

    // is u an ancestor of v
    HierarchyTreeView.prototype.is_ancestor = function(u, v) {
	if (v.length < u.length) { return false; }
	var u_rev = u.split(".").reverse().join(".");
	var v_rev = v.split(".").reverse().join(".");
	return v_rev.slice( 0, u_rev.length ) == u_rev;
    }

    HierarchyTreeView.prototype.compute_graph_edges = function() {
	var graph_edges = {};
	var edges = this.config.ht.get_edges();

	for(var i=0; i < edges.length; i++ ) {
	    var edge = edges[i];
	    var source_id = edge["source"];
	    var target_id = edge["target"];
	    if (! (source_id in graph_edges) ) {
		graph_edges[source_id] = [];
	    }
	    graph_edges[source_id].push( target_id );
	}
	return graph_edges;
    }
    
    // E(u,v)
    HierarchyTreeView.prototype.has_pairwise_edges = function(u, v, graph_edges) {
	var has_pairwise_edges = false;

	// Neither u nor v should be an ancestor of the other
	if ( this.is_ancestor(u, v) || this.is_ancestor(v, u) ) {
	    return false;
	}
	
	var u_nodes = this.config.ht.get_nodes( "path", u );
	var v_nodes = this.config.ht.get_nodes( "path", v );
	var u_node = u_nodes[0];
	var v_node = v_nodes[0];
	
	var u_leaves = this.config.ht.leaves( u_node );
	var v_leaves = this.config.ht.leaves( v_node );

	for(var i=0; i < u_leaves.length; i++) {
	    for(var j=0; j < v_leaves.length; j++) {
		var u_leaf_id = u_leaves[i].model.path;
		var v_leaf_id = v_leaves[j].model.path;
		if ( ( (u_leaf_id in graph_edges) &&
		       (graph_edges[u_leaf_id].indexOf(v_leaf_id) > -1 ) ) ||
		     ( (v_leaf_id in graph_edges) &&
		       (graph_edges[v_leaf_id].indexOf(u_leaf_id) > -1 ) ) ) {
		    has_pairwise_edges = true;
		    return has_pairwise_edges;
		}
	    }
	}
	return has_pairwise_edges;
    };

    // I(T,G)
    HierarchyTreeView.prototype.compute_induced_edges = function(view) {
	var u_s = view.toArray();
	var v_s = view.toArray();
	var graph_edges = this.compute_graph_edges();  // Get the dictionary

	var induced_edges = [];
	for( var i=0; i< u_s.length; i++ ) {
	    for( var j=1; j < v_s.length; j++ ) {
		if ( i >= j ) { continue; }
		var u = u_s[i];
		var v = v_s[j];
		if ( this.has_pairwise_edges(u, v, graph_edges) ||
		     this.has_pairwise_edges(v, u, graph_edges) ) {
		    // This is lazy in terms of relation type
		    var edge = { "relation":"cptlc:hasLink",
			     "source":u,
			     "target":v };
		    induced_edges.push(edge);
		}
	    }
	}
	return induced_edges;
    };

    HierarchyTreeView.prototype.compute_induced_graph = function(view) {
	var induced_graph = { "nodes":[], "links":[] };
	var view_array = view.toArray();
	    
	for (var i=0; i < view_array.length; i++) {
	    var name = view_array[i];
	    var path = view_array[i];

	    //var type = this.get_type_for_node(path);
	    //var node = { "name": name, "path":path, "rdfs:type":type };
	    var node = this.get_node(path);
	    induced_graph["nodes"].push(node);
	}
	induced_graph["links"] = this.compute_induced_edges(view);
	return induced_graph;
    };
    
    return HierarchyTreeView;
})();

},{}]},{},[1])(1)
});
    
