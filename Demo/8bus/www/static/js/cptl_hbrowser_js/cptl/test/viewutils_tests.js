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


function setUp() {
    cptl_data_path = "http://localhost:8080/jsunit/cptl-js-data/substations.graph.test.json";
}

function testAssert() {
    assert("true should be true", true);
    assert(true);
}

function testAttachIds() {
    d3.json( cptl_data_path, function(error, json_graph_data) {
	if (error) {
	    console.log("Failed to open JSON graph data at " + cptl_data_path + "\n");
	}

	result_graph_data = attach_ids( json_graph_data );
	assert( "id" in result_graph_data.nodes[0] );
    });    
}

