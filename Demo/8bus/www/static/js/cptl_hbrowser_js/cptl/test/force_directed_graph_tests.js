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
    domains_graph_data_path = "http://localhost:8080/jsunit/cptl-js-data/substations.graph.test.json";
    domains_tree_data_path = "http://localhost:8080/jsunit/cptl-js-data/substations.domain-names.test.json";
    icon_dict_data_path = "http://localhost:8080/jsunit/cptl-js-data/icon_dict.json";
    namespaces_data_path = "http://localhost:8080/jsunit/cptl-js-data/namespaces.json";

    charge = -500;
    height = 1100;
    link_distance = 100;
    width = 1800;
    svg_element = d3.select("body").append("svg").attr("width", width).attr("height", height);
}

function testInitialize() {

    d3.json( domains_graph_data_path, function(error, json_graph_data) {
	if (error) {
	    console.log("Failed to open JSON graph data at " + domains_graph_data_path + "\n");
	}
	fdg = new ForceDirectedGraph();
	fdg.initialize(svg_element, charge, height, link_distance, width, json_graph_data);
	assertTrue( null != fdg.config.color );
	assertTrue( null != fdg.config.force );
	assertTrue( null != fdg.config.nodes );
	assertTrue( null != fdg.config.links );
	assertTrue( null != d3.select("svg") );
    });
}

function testAddIconDefs() {

    d3.json( domains_graph_data_path, function(error, json_graph_data) {
	if (error) {
	    console.log("Failed to open JSON graph data at " + domains_graph_data_path + "\n");
	}

	// Load the icon dictionary
	icon_dict = null;
	d3.json( icon_dict_data_path, function(error, icon_dict) {
	    if (error) {
		console.log("Failed to open icon dictionary at " + icon_dict_data_path + "\n");
	    }

	    var icon_dir = "../../../cptl-js-data";

	    fdg = new ForceDirectedGraph();
	    fdg.initialize(svg_element, charge, height, link_distance, width, json_graph_data);
	    var defs_element = svg_element.append("defs");		    
	    fdg.add_icon_defs(defs_element, icon_dir, icon_dict);

	    assertTrue( null != svg_element );
	    var defs_element = svg_element.select("defs");
	    assertTrue( null != defs_element );
	    var filters_elements = defs_element.selectAll("filter")[0];
	    assertEquals(11, filters_elements.length);
	    
	});	
    });
}

function testUpdateD3Ids() {

    d3.json( domains_graph_data_path, function(error, json_graph_data) {
	if (error) {
	    console.log("Failed to open JSON graph data at " + domains_graph_data_path + "\n");
	}
	fdg = new ForceDirectedGraph();
	fdg.initialize(charge, height, link_distance, width, json_graph_data);

	// There are no ids d3js ids before
	for ( node in fdg.config.nodes ) {
	    assertFalse( "id" in node && null != node[id] );
	}

	for ( link in fdg.config.links ) {
	    assertEquals( "string", typeof link["source"] );
	    assertEquals( "string", typeof link["target"] );
	}

	var node_id_field = "name";

	fdg.update_d3_ids(json_graph_data, node_id_field);

	var json_graph_data_nodes = json_graph_data["nodes"];
	for (var i=0; i < json_graph_data_nodes.length; i++) {
	    var node = json_graph_data_nodes[i];
	    assertTrue( "id" in node && null != node["id"] );
	}

	var json_graph_data_links = json_graph_data["links"];
	for (var i=0; i < json_graph_data_links.length; i++ ) {
	    var link = json_graph_data_links[i];
	    assertEquals( "number", typeof link["source"] );
	    assertEquals( "number", typeof link["target"] );
	    assertEquals( "string", typeof link["source-name"] );
	    assertEquals( "string", typeof link["target-name"] );
	}
	
    });
}

function testUpdateGraph() {
    d3.json( domains_graph_data_path, function(error, json_graph_data) {
	if (error) {
	    console.log("Failed to open JSON graph data at " + domains_graph_data_path + "\n");
	}

	var new_json_graph_data = { "nodes":[], "links":[] };

	// Push new nodes and nodes already in the original graph
	new_json_graph_data["nodes"].push( {"name":"new1"} );
	new_json_graph_data["nodes"].push( {"name":"new2"} );
	new_json_graph_data["nodes"].push(
	    {"name": "odgenville-yard:Odgenville$BRK$62", 
             "rdfs:type": "syard:Breaker"});  
	new_json_graph_data["nodes"].push(
	    {"name": "odgenville-yard:Odgenville$ND$6", 
             "rdfs:type": "syard:Node"});  

	// Push new links and links already in the original graph
	new_json_graph_data["links"].push( {"source":"new1",
					    "target":"new2",
					    "relation":"cptlc:hasLink"} );
	new_json_graph_data["links"].push( {"source":"odgenville-yard:Odgenville$BRK$62", "target":"new1", "relation":"cptlc:hasLink"} );
	new_json_graph_data["links"].push( {"source":"odgenville-yard:Odgenville$ND$6",
					    "target":"odgenville-yard:Odgenville$BRK$62", "relation":"cptlc:hasLink"} );	

	assertEquals( 179, json_graph_data["nodes"].length );
	assertEquals( 273, json_graph_data["links"].length );

	fdg = new ForceDirectedGraph();
	fdg.initialize(charge, height, link_distance, width, json_graph_data);

	var node_id_field = "name";
	fdg.update_d3_ids( json_graph_data, node_id_field );
	fdg.update_graph( json_graph_data, node_id_field );
	assertEquals( 179, fdg.config.nodes.length );
	assertEquals( 273, fdg.config.links.length );

	// Perform the update and get new graph
	fdg.update_d3_ids( new_json_graph_data, node_id_field );
	fdg.update_graph( new_json_graph_data, node_id_field );
	assertEquals( 181, fdg.config.nodes.length );
	assertEquals( 275, fdg.config.links.length );
	
    });
}
