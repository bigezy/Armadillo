/*
  copyright (c) 2015, Gabriel A. Weaver, Information Trust Institute
    at the University of Illinois, Urbana-Champaign.

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
(function(f){if(typeof exports==="object"&&typeof module!=="undefined"){module.exports=f()}else if(typeof define==="function"&&define.amd){define([],f)}else{var g;if(typeof window!=="undefined"){g=window}else if(typeof global!=="undefined"){g=global}else if(typeof self!=="undefined"){g=self}else{g=this}g.ForceDirectedGraph = f()}})(function(){var define,module,exports;return (function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=="function"&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);var f=new Error("Cannot find module '"+o+"'");throw f.code="MODULE_NOT_FOUND",f}var l=n[o]={exports:{}};t[o][0].call(l.exports,function(e){var n=t[o][1][e];return s(n?n:e)},l,l.exports,e,t,n,r)}return n[o].exports}var i=typeof require=="function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s})({1:[function(require,module,exports){

module.exports = (function () {
  'use strict';

    function ForceDirectedGraph(config) {
	config = config || {};
	this.config = config;
	this.config.links = [];
	this.config.nodes = [];
    }

    /*
      Relabel a CPTL Graph with d3js compliant ids
     */
    ForceDirectedGraph.prototype.update_d3_ids = function(json_graph_data, node_id_field) {
	// A mapping from an identifier field to an integer id for d3js
	var id_2_d3id = {};
	var nodes = json_graph_data["nodes"];
	var links = json_graph_data["links"];
	var link_source_id_field = "source" + "-" + node_id_field;
	var link_target_id_field = "target" + "-" + node_id_field;
	
	for (var i=0; i < nodes.length; i++) {
	    var node = nodes[i];
	    var node_id = node[node_id_field];
	    nodes[i]["id"] = i;
	    id_2_d3id[node_id] = i;
	}

	for (var i=0; i < links.length; i++) {
	    var link = links[i];

	    /* When we load a new link, relabel source/target since
	        those fields used by d3js */
	    if ( !(link_source_id_field in link) ) {
		link[link_source_id_field] = link["source"];
	    }
	    if ( !(link_target_id_field in link) ) {
		link[link_target_id_field] = link["target"];
	    }

	    /* Use the non-d3js link id to assign d3js link ids */	    
	    var source_id = link[link_source_id_field];
            var target_id = link[link_target_id_field];

	    links[i]["source"] = id_2_d3id[source_id];
	    links[i]["target"] = id_2_d3id[target_id];
	}
    };

    ForceDirectedGraph.prototype.update_graph = function(json_graph_data, node_id_field) {
	var json_graph_data_nodes = json_graph_data["nodes"];
	var json_graph_data_links = json_graph_data["links"];
	var link_source_id_field = "source" + "-" + node_id_field;
	var link_target_id_field = "target" + "-" + node_id_field;
	
	// Get nodes from the current graph
	var current_node_ids = [];
	this.config.nodes.forEach( function(d) {
	    current_node_ids.push(d[node_id_field]);
	});

	// Add new nodes to the current graph
	for (var i=0; i < json_graph_data_nodes.length; i++) {
	    var node = json_graph_data_nodes[i];
	    var node_id = node[node_id_field];
	    if ( current_node_ids.indexOf(node_id) == -1 ) {
		this.config.nodes.push(node);
	    }
	}

	// Get links from the current graph
	var current_link_ids = [];
	this.config.links.forEach( function(d) {
	    var link_id = d[link_source_id_field] + "-" + d[link_target_id_field];
	    current_link_ids.push(link_id);
	});

	// Add new links to the current graph
	for (var i=0; i < json_graph_data_links.length; i++) {
	    var link = json_graph_data_links[i];
	    var link_id = link[link_source_id_field] + "-" + link[link_target_id_field];
	    if ( current_link_ids.indexOf(link_id) == -1 ) {
		this.config.links.push(link);
	    }
	}

    };

    return ForceDirectedGraph;
})();

},{}]},{},[1])(1)
});
    
