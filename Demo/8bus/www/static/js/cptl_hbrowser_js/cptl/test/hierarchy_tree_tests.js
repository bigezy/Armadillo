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

function setUp() {
    domains_tree_data_path = "http://localhost:8080/jsunit/cptl-js-data/substations.domain-names.test.json";
    domains_graph_data_path = "http://localhost:8080/jsunit/cptl-js-data/substations.graph.test.json";     
}

function testInitializeGraph() {
    d3.json( domains_graph_data_path, function(error, json_graph_data) {
	if (error) {
	    console.log("Failed to open JSON graph data at " + domains_graph_data_path + "\n");
	}
	ht = new HierarchyTree();
	ht.initialize_graph(json_graph_data);
	assertEquals( 179, ht.get_vertices().length )
    });
}

function testInitializeTree() {
    d3.json( domains_tree_data_path, function(error, json_tree_data) {
	if (error) {
	    console.log("Failed to open JSON tree data at " + ip_tree_data_path + "\n");
	}
	ht = new HierarchyTree();
	ht.initialize_tree(json_tree_data);
	
	nodeParis = ht.config.tree.first( function(node) {
	    return node.model.name === "paris";
	});

	path = nodeParis.getPath();
	path = path.slice(1);
	assertEquals( 2, path.length );
	assertEquals( "org.cptl-c.projects.cypsa.8sub", path[0].model.name );
	assertEquals( "paris", path[1].model.name );
    });
}

function testInitialize() {
    d3.json( domains_graph_data_path, function(error, json_graph_data) {
	if (error) {
	    console.log("Failed to open JSON graph data at " + domains_graph_data_path + "\n");
	}

	d3.json( domains_tree_data_path, function(error, json_tree_data) {
	    if (error) {
		console.log("Failed to open JSON tree data at " + domains_tree_data_path + "\n");
	    }
	    
	    ht = new HierarchyTree();
	    ht.initialize_tree(json_tree_data);
	    ht.initialize_graph(json_graph_data);
	    
	    assertEquals( 179, ht.config.graph.get_vertices().length )

	    idField = "path";
	    n1Path = "network.odgenville.8sub.cypsa.projects.cptl-c.org";
	    nodes = ht.get_nodes(idField, n1Path);
	    assertEquals( 1, nodes.length );
	    assertEquals( n1Path, nodes[0].model.path );
	});
    });
}

function testGetNodes() {
    d3.json( domains_tree_data_path, function(error, json_tree_data) {
	if (error) {
	    console.log("Failed to open JSON tree data at " + ip_tree_data_path + "\n");
	}

	idField = "path";   // should be enet:hasDomainNameValue

	ht = new HierarchyTree();
	ht.initialize_tree(json_tree_data);

	n1Path = "network.odgenville.8sub.cypsa.projects.cptl-c.org";
	nodes = ht.get_nodes(idField, n1Path);
	assertEquals( 1, nodes.length );
	assertEquals( n1Path, nodes[0].model.path );
    });
}

function testChildren() {
    d3.json( domains_tree_data_path, function(error, json_tree_data) {
	if (error) {
	    console.log("Failed to open JSON tree data at " + ip_tree_data_path + "\n");
	}
	idField = "path"   // should be enet:hasDomainNameValue

	ht = new HierarchyTree();
	ht.initialize_tree(json_tree_data);

	n1Path = "odgenville.8sub.cypsa.projects.cptl-c.org";
	nodes = ht.get_nodes(idField, n1Path);
	assertEquals( 1, nodes.length );
	n1 = nodes[0];
	n1Leaves = ht.children(n1);
	assertEquals(2, n1Leaves.length);	
    });
}

function testLeaves() {
    d3.json( domains_tree_data_path, function(error, json_tree_data) {
	if (error) {
	    console.log("Failed to open JSON tree data at " + ip_tree_data_path + "\n");
	}
	idField = "path"   // should be enet:hasDomainNameValue
	
	ht = new HierarchyTree();
	ht.initialize_tree(json_tree_data);

	n1Path = "network.odgenville.8sub.cypsa.projects.cptl-c.org";
	nodes = ht.get_nodes(idField, n1Path);
	assertEquals( 1, nodes.length );
	n1 = nodes[0];
	n1Leaves = ht.leaves(n1);
	assertEquals(6, n1Leaves.length);

	n2Path = "yard.odgenville.8sub.cypsa.projects.cptl-c.org";	
	nodes = ht.get_nodes(idField, n2Path);
	assertEquals( 1, nodes.length );
	n2 = nodes[0];
	n2Leaves = ht.leaves(n2);
	assertEquals(15, n2Leaves.length);

	n3Path = "odgenville.8sub.cypsa.projects.cptl-c.org";		
	nodes = ht.get_nodes(idField, n3Path);
	assertEquals( 1, nodes.length );
	n3 = nodes[0];
	n3Leaves = ht.leaves(n3);
	assertEquals(21, n3Leaves.length);	
    });
}

