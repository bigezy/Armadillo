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
function attach_ids( json_graph_data ) {
    var name2id = {};

    for (var i=0; i < json_graph_data.nodes.length; i++) {
	var node = json_graph_data.nodes[i];
	var node_name = node["name"];
	json_graph_data.nodes[i]["id"] = i;
	name2id[node_name] = i;
    }

    for (var i=0; i < json_graph_data.links.length; i++) {
	var link = json_graph_data.links[i];
	var source_name = link["source"];
	var target_name = link["target"];

	if ( !(source_name in name2id) ) {
	    console.log("Source name: " + source_name + " not in dictionary");
	}

	if ( !(target_name in name2id) ) {
	    console.log("Source name: " + source_name + " not in dictionary");
	}
	json_graph_data.links[i]["source"] = name2id[source_name];
	json_graph_data.links[i]["target"] = name2id[target_name];
    }
    return json_graph_data;
}


