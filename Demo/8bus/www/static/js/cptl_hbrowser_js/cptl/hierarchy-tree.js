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
(function(f){if(typeof exports==="object"&&typeof module!=="undefined"){module.exports=f()}else if(typeof define==="function"&&define.amd){define([],f)}else{var g;if(typeof window!=="undefined"){g=window}else if(typeof global!=="undefined"){g=global}else if(typeof self!=="undefined"){g=self}else{g=this}g.HierarchyTree = f()}})(function(){var define,module,exports;return (function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=="function"&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);var f=new Error("Cannot find module '"+o+"'");throw f.code="MODULE_NOT_FOUND",f}var l=n[o]={exports:{}};t[o][0].call(l.exports,function(e){var n=t[o][1][e];return s(n?n:e)},l,l.exports,e,t,n,r)}return n[o].exports}var i=typeof require=="function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s})({1:[function(require,module,exports){

module.exports = (function () {
  'use strict';

    function HierarchyTree(config) {
	config = config || {};
	this.config = config;
	this.config.tree = null;
	this.config.graph = null;
    }

    // GRAPH METHODS
    HierarchyTree.prototype.initialize_graph = function(json_graph_data) {
	this.config.graph = new Graph();
	this.config.graph.set_graph(json_graph_data);
    };

    HierarchyTree.prototype.get_vertices = function() {
	return this.config.graph.get_vertices();
    }

    HierarchyTree.prototype.get_edges = function() {
	return this.config.graph.get_edges();
    }
 
    // TREE METHODS
    HierarchyTree.prototype.initialize_tree = function(json_tree_data) {
	var tree = new TreeModel();
	// Parse the tree
	this.config.tree = tree.parse( json_tree_data );
    };

    HierarchyTree.prototype.get_nodes = function(key, value) {
	var nodes = this.config.tree.all( function(n) {
	    if (key == "path") {
		if (typeof n.model.path != 'undefined') {
		    return n.model.path === value;
		}
	    } else {
		console.log("Support to get node by " + key + " currently not supported.");
	    }
	});
	return nodes;
    };
    
    HierarchyTree.prototype.children = function(node) {
	return node.model.children;
    }
    
    HierarchyTree.prototype.leaves = function(node) {
	var leaves = node.all(function (n) {
	    if (typeof n.model.children != 'undefined') {
		return false;
	    } else {
		return true;
	    }
	});
	return leaves;
    };

    return HierarchyTree;
})();

},{}]},{},[1])(1)
});
