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
    namespaces_data_path = "http://localhost:8080/jsunit/cptl-js-data/namespaces.json";
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
	    htv = new HierarchyTreeView();
	    htv.initialize(json_graph_data, json_tree_data);

	    // Test graph initialization
	    assertEquals( 179, htv.config.ht.get_vertices().length );

	    // Test tree initialization
	    idField = "path";
	    n1Path = "network.odgenville.8sub.cypsa.projects.cptl-c.org";
	    nodes = htv.config.ht.get_nodes(idField, n1Path);
	    assertEquals( 1, nodes.length );
	    assertEquals( n1Path, nodes[0].model.path );
	});
    });
}

function testIsHierarchyTree() {
    d3.json( domains_graph_data_path, function(error, json_graph_data) {
	if (error) {
	    console.log("Failed to open JSON graph data at " + domains_graph_data_path + "\n");
	}
	d3.json( domains_tree_data_path, function(error, json_tree_data) {
	    if (error) {
		console.log("Failed to open JSON tree data at " + domains_tree_data_path + "\n");
	    }

	    htv = new HierarchyTreeView();
	    htv.initialize(json_graph_data, json_tree_data);
	    //assertTrue( htv.is_hierarchy_tree( htv.get_vertices_for_leaf ) );

	});
    });
}

function testViewPartitionsGraph() {
    d3.json( domains_graph_data_path, function(error, json_graph_data) {
	if (error) {
	    console.log("Failed to open JSON graph data at " + domains_graph_data_path + "\n");
	}
	d3.json(domains_tree_data_path, function(error, json_tree_data) {
	    if (error) {
		console.log("Failed to open JSON tree data at " + domains_tree_data_path + "\n");
	    }

	    htv = new HierarchyTreeView();
	    htv.initialize(json_graph_data, json_tree_data);	    	    
	    domain_suffix = "8sub.cypsa.projects.cptl-c.org";
	    
	    // Generate a substation-level view
	    var view1 = new buckets.Set();
	    view1.add( "springfield." + domain_suffix );
	    view1.add( "shelbyville." + domain_suffix );
	    view1.add( "cypress-creek." + domain_suffix );
	    view1.add( "capital-city." + domain_suffix );
	    view1.add( "haverbrook." + domain_suffix );
	    view1.add( "north-haverbrook." + domain_suffix );
	    view1.add( "paris." + domain_suffix );
	    view1.add( "odgenville." + domain_suffix );
	    //assertTrue( htv.view_partitions_graph(view1) );

	    view1.remove( "springfield." + domain_suffix );	    
	    //assertFalse( htv.view_partitions_graph(View1) );
	});
    });
}
function testGetTypeForNode() {
    d3.json( domains_graph_data_path, function(error, json_graph_data) {
	if (error) {
	    console.log("Failed to open JSON graph data at " + domains_graph_data_path + "\n");
	}
	d3.json(domains_tree_data_path, function(error, json_tree_data) {
	    if (error) {
		console.log("Failed to open JSON tree data at " + domains_tree_data_path + "\n");
	    }
	    d3.json(namespaces_data_path, function(error, namespaces) {
		if (error) {
		    console.log("Failed to open JSON namespaces at " + namespaces_data_path + "\n");
		}
		
		htv = new HierarchyTreeView();
		htv.initialize(json_graph_data, json_tree_data);
		htv.config.namespaces = namespaces;

		path1 = "SEL_451_1.network.odgenville." + domain_suffix;
		type1 = htv.get_type_for_node(path1);
		assertEquals( "snet:OvercurrentRelay", type1);

		path2 = "network.odgenville." + domain_suffix;
		type2 = htv.get_type_for_node(path2);
		assertEquals( "snet:SubstationNetwork", type2);

		path3 = "yard.odgenville." + domain_suffix;
		type3 = htv.get_type_for_node(path3);
		assertEquals( "syard:SubstationYard", type3);

		path4 = "odgenville." + domain_suffix;
		type4 = htv.get_type_for_node(path4);
		assertEquals( "cptlc:Substation", type4);
		
	    }); // namespaces
	}); // tree
    }); // graph
}

function testViewExpand() {
    d3.json( domains_graph_data_path, function(error, json_graph_data) {
	if (error) {
	    console.log("Failed to open JSON graph data at " + domains_graph_data_path + "\n");
	}
	d3.json(domains_tree_data_path, function(error, json_tree_data) {
	    if (error) {
		console.log("Failed to open JSON tree data at " + domains_tree_data_path + "\n");
	    }

	    htv = new HierarchyTreeView();
	    htv.initialize(json_graph_data, json_tree_data);
	    domain_suffix = "8sub.cypsa.projects.cptl-c.org";	    

	    var view1 = new buckets.Set();
	    view1.add( "springfield." + domain_suffix );
	    view1.add( "shelbyville." + domain_suffix );
	    view1.add( "cypress-creek." + domain_suffix );
	    view1.add( "capital-city." + domain_suffix );
	    view1.add( "haverbrook." + domain_suffix );
	    view1.add( "north-haverbrook." + domain_suffix );
	    view1.add( "paris." + domain_suffix );
	    view1.add( "odgenville." + domain_suffix );
	    //assertTrue( htv.view_partitions_graph(view1) );
	    
	    var x = "odgenville." + domain_suffix;
	    view1 = htv.view_expand(view1, x);
	    //assertTrue( htv.view_partitions_graph(view1) );
	    assertFalse( view1.contains(x) );
	    assertEquals( 9, view1.size() );
	    assertTrue( view1.contains( "yard.odgenville." + domain_suffix ) );
	    assertTrue( view1.contains( "network.odgenville." + domain_suffix ) );
	});
    });
}

function testViewContract() {
    d3.json( domains_graph_data_path, function(error, json_graph_data) {
	if (error) {
	    console.log("Failed to open JSON graph data at " + domains_graph_data_path + "\n");
	}
	d3.json(domains_tree_data_path, function(error, json_tree_data) {
	    if (error) {
		console.log("Failed to open JSON tree data at " + domains_tree_data_path + "\n");
	    }

	    htv = new HierarchyTreeView();
	    htv.initialize(json_graph_data, json_tree_data);
	    domain_suffix = "8sub.cypsa.projects.cptl-c.org";
	    
	    // Generate a substation-level view
	    var view1 = new buckets.Set();
	    view1.add( "springfield." + domain_suffix );
	    view1.add( "shelbyville." + domain_suffix );
	    view1.add( "cypress-creek." + domain_suffix );
	    view1.add( "capital-city." + domain_suffix );
	    view1.add( "haverbrook." + domain_suffix );
	    view1.add( "north-haverbrook." + domain_suffix );
	    view1.add( "paris." + domain_suffix );
	    view1.add( "odgenville." + domain_suffix );
	    //assertTrue( htv.view_partitions_graph(view1) );
	    
	    var x = "odgenville." + domain_suffix;
	    view1 = htv.view_contract(view1, x);
	    //assertTrue( htv.view_partitions_graph(view1) );
	    assertTrue( view1.contains(x) );
	    assertEquals( 8, view1.size() );
	    assertFalse( view1.contains( "yard.odgenville." + domain_suffix ) );
	    assertFalse( view1.contains( "network.odgenville." + domain_suffix ) );
	});
    });
}

function testIsAncestor() {
    d3.json( domains_graph_data_path, function(error, json_graph_data) {
	if (error) {
	    console.log("Failed to open JSON graph data at " + domains_graph_data_path + "\n");
	}
	d3.json(domains_tree_data_path, function(error, json_tree_data) {
	    if (error) {
		console.log("Failed to open JSON tree data at " + domains_tree_data_path + "\n");
	    }
	    htv = new HierarchyTreeView();
	    htv.initialize(json_graph_data, json_tree_data);

	    domain_suffix = "8sub.cypsa.projects.cptl-c.org";
	    // Test two nodes that are not ancestors
	    x1 = "network.odgenville." + domain_suffix;
	    x2 = "yard.odgenville." + domain_suffix;
	    assertFalse( htv.is_ancestor(x1, x2) );
	    assertFalse( htv.is_ancestor(x2, x1) );
	    
	    // Test two nodes that are ancestors
	    x3 = "odgenville." + domain_suffix;
	    assertFalse( htv.is_ancestor(x2, x3) );
	    assertTrue( htv.is_ancestor(x3, x2) );
	});
    });
}

function testComputeGraphEdges() {
    d3.json( domains_graph_data_path, function(error, json_graph_data) {
	if (error) {
	    console.log("Failed to open JSON graph data at " + domains_graph_data_path + "\n");
	}
	d3.json(domains_tree_data_path, function(error, json_tree_data) {
	    if (error) {
		console.log("Failed to open JSON tree data at " + domains_tree_data_path + "\n");
	    }
	    d3.json(namespaces_data_path, function(error, namespaces) {
		if (error) {
		    console.log("Failed to open JSON namespaces at " + namespaces_data_path + "\n");
		}
		htv = new HierarchyTreeView();
		htv.initialize(json_graph_data, json_tree_data);
		htv.config.namespaces = namespaces;
		graph_edges = htv.compute_graph_edges();
		n_edges = 0;
		for (var key in graph_edges) {
		    n_edges = n_edges + graph_edges[key].length;
		}
		assertEquals( 273, n_edges );
		u1 = "SEL_451_1.network.odgenville." + domain_suffix;
		assertTrue( u1 in graph_edges );
		assertEquals( 2, graph_edges[u1].length );
	    });
	});
    });
}

function testHasPairwiseEdges() {
    d3.json( domains_graph_data_path, function(error, json_graph_data) {
	if (error) {
	    console.log("Failed to open JSON graph data at " + domains_graph_data_path + "\n");
	}
	d3.json(domains_tree_data_path, function(error, json_tree_data) {
	    if (error) {
		console.log("Failed to open JSON tree data at " + domains_tree_data_path + "\n");
	    }
	    d3.json(namespaces_data_path, function(error, namespaces) {
		if (error) {
		    console.log("Failed to open JSON namespaces at " + namespaces_data_path + "\n");
		}
		htv = new HierarchyTreeView();
		htv.initialize(json_graph_data, json_tree_data);

		domain_suffix = "8sub.cypsa.projects.cptl-c.org";
		u1 = "network.odgenville." + domain_suffix;
		v1 = "yard.odgenville." + domain_suffix;
		assertFalse( htv.is_ancestor(u1, v1) );
		assertFalse( htv.is_ancestor(v1, u1) );
		htv.config.namespaces = namespaces;
		graph_edges = htv.compute_graph_edges();  // Get the dictionary
		assertTrue( htv.has_pairwise_edges( u1, v1, graph_edges) );

		v2 = "network.cypress-creek." + domain_suffix;
		assertFalse( htv.is_ancestor( u1, v2 ) );
		assertFalse( htv.is_ancestor( v2, u1 ) );
		assertTrue( htv.has_pairwise_edges( u1, v2, graph_edges ) );
	    });
	});
    });
}

function testComputeInducedEdges() {
    d3.json( domains_graph_data_path, function(error, json_graph_data) {
	if (error) {
	    console.log("Failed to open JSON graph data at " + domains_graph_data_path + "\n");
	}
	d3.json(domains_tree_data_path, function(error, json_tree_data) {
	    if (error) {
		console.log("Failed to open JSON tree data at " + domains_tree_data_path + "\n");
	    }
	    d3.json(namespaces_data_path, function(error, namespaces) {
		if (error) {
		    console.log("Failed to open JSON namespaces at " + namespaces_data_path + "\n");
		}

		htv = new HierarchyTreeView();
		htv.initialize(json_graph_data, json_tree_data);
		htv.config.namespaces = namespaces;

		domain_suffix = "8sub.cypsa.projects.cptl-c.org";		
		var view1 = new buckets.Set();
		view1.add( "yard.springfield." + domain_suffix );
		view1.add( "yard.cypress-creek." + domain_suffix );
		view1.add( "yard.odgenville." + domain_suffix );
		view1.add( "network.odgenville." + domain_suffix );		
		
		induced_edges = htv.compute_induced_edges(view1);
		assertEquals(2, induced_edges.length);

		var x = "odgenville." + domain_suffix;
		view2 = htv.view_contract(view1, x );
		induced_edges = htv.compute_induced_edges(view2);
		assertEquals(1, induced_edges.length);
		edge = induced_edges[0];
		assertEquals( "yard.cypress-creek." + domain_suffix, edge["source"] );
		assertEquals( "odgenville." + domain_suffix, edge["target"] );
	    });
	});
    });
}


function testComputeInducedGraph() {
    d3.json( domains_graph_data_path, function(error, json_graph_data) {
	if (error) {
	    console.log("Failed to open JSON graph data at " + domains_graph_data_path + "\n");
	}
	d3.json(domains_tree_data_path, function(error, json_tree_data) {
	    if (error) {
		console.log("Failed to open JSON tree data at " + domains_tree_data_path + "\n");
	    }
	    d3.json(namespaces_data_path, function(error, namespaces) {
		if (error) {
		    console.log("Failed to open JSON namespaces at " + namespaces_data_path + "\n");
		}
		htv = new HierarchyTreeView();
		htv.initialize(json_graph_data, json_tree_data);
		htv.config.namespaces = namespaces;

		// Building the view
		domain_suffix = "8sub.cypsa.projects.cptl-c.org";		

		var view1 = new buckets.Set();
		view1.add( "yard.springfield." + domain_suffix );
		view1.add( "yard.cypress-creek." + domain_suffix );
		view1.add( "yard.odgenville." + domain_suffix );
		view1.add( "network.odgenville." + domain_suffix );		

		var induced_graph = htv.compute_induced_graph(view1);
		assertEquals( 4, induced_graph["nodes"].length );
		assertEquals( 2, induced_graph["links"].length );		
	    });
	});
    });
}
