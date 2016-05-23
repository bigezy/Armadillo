"""
Copyright (c) 2016 Gabriel A. Weaver, Information Trust Institute
All rights reserved.

Developed by:             Gabriel A. Weaver, Information Trust Institute
                          University of Illinois at Urbana-Champaign
                          http://www.iti.illinois.edu/

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal with the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

Redistributions of source code must retain the above copyright notice,
this list of conditions and the following disclaimers.
Redistributions in binary form must reproduce the above copyright
notice, this list of conditions and the following disclaimers in the
documentation and/or other materials provided with the distribution.

Neither the names of Gabriel A. Weaver, Information Trust Institute,
University of Illinois at Urbana-Champaign, nor the names of its
contributors may be used to endorse or promote products derived from
this Software without specific prior written permission.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE CONTRIBUTORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR
IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS WITH THE
SOFTWARE.
"""
from networkx.readwrite import json_graph
import json
import networkx as nx
import sys

class CPTLGraphJoin():
    graphs_dao = None
    id_field = None
    join_field = None
    merged_graph = None
    
    def get_merged_graph(self):

        graph_data = json_graph.node_link_data(self.merged_graph)
        for node in graph_data["nodes"]:
            del node["id"]
            
        # Convert the graph back to string-based targets
        for edge in graph_data["links"]:
            source_idx = edge["source"]
            source_node = self.merged_graph.node[ source_idx ]

            target_idx = edge["target"]
            target_node = self.merged_graph.node[ target_idx ]

            edge["source"] = source_node[ self.id_field ] 
            edge["target"] = target_node[ self.id_field ] 

        del graph_data["directed"]
        del graph_data["graph"]
        del graph_data["multigraph"]        

        return graph_data
    
    def output_graph(self, graph_filepath):
        graph_data = self.get_merged_graph()
        
        # Output the graph
        f = open(graph_filepath, 'w')
        json.dump(graph_data, f, indent=4, sort_keys=True);
        f.close()
    
    def compute_new_id_mapping( self, graph, graph_id_mapping, next_id, name_2_id, join_field ):
        for node_idx in graph.nodes():
            node = graph.node[node_idx]

            if join_field in node and node[join_field] in name_2_id:
                name = node[join_field]                                
                new_id = name_2_id[ name ]
                graph_id_mapping[ node_idx ] = new_id
            else:
                graph_id_mapping[ node_idx ] = next_id
                next_id = next_id + 1
    
    def load_graph(self, graph_data):
        G = nx.Graph()

        idf_2_idx = {}
        for idx, node in enumerate(graph_data["nodes"]):
            G.add_node(idx, node)
            idf_value = node[self.id_field]
            idf_2_idx[ idf_value ] = idx

        for idx, edge in enumerate(graph_data["links"]):
            source_idf_value = edge["source"]
            target_idf_value = edge["target"]
            source_idx = idf_2_idx[source_idf_value]
            target_idx = idf_2_idx[target_idf_value]
            del edge["source"]
            del edge["target"]
            G.add_edge(source_idx, target_idx, edge)

        return G

    def get_field_value(self, x, field):
        if field in x:
            return x[field]
            
    def merge_graphs(self, graph1_ref, graph2_ref):

        graph1_data = self.graphs_dao.retrieve( graph1_ref )
        graph2_data = self.graphs_dao.retrieve( graph2_ref )

        # 0.  Load the data into network X graphs
        g1 = self.load_graph(graph1_data)
        g2 = self.load_graph(graph2_data)

        ## CREATE NEW LABELS
        # 1.  Create common indices for the 'same' nodes (as defined by the join field)
        s1 = set(map(lambda x: self.get_field_value(x, self.join_field1), graph1_data["nodes"]))
        s2 = set(map(lambda x: self.get_field_value(x, self.join_field2), graph2_data["nodes"]))
        if None in s1:
            s1.remove(None)
        if None in s2:
            s2.remove(None)
            
        common = s1 & s2
        different = s1 ^ s2

        #graph1_keys = list(common) + list(s1 - common)
        #graph2_keys = list(common) + list(s2 - common)

        # 2.  Get a list of integer IDs for all the nodes with the 
        common_name_2_id = dict(zip( list(common), range(0,len(common)) ))

        next_g1_id = len(common)
        g1_id_mapping = {}
        self.compute_new_id_mapping( g1, g1_id_mapping, next_g1_id, common_name_2_id, self.join_field1 )

        next_g2_id = len(g1.nodes())                
        g2_id_mapping = {}
        self.compute_new_id_mapping( g2, g2_id_mapping, next_g2_id, common_name_2_id, self.join_field2 )
                
        h1 = nx.relabel_nodes(g1, g1_id_mapping)
        h2 = nx.relabel_nodes(g2, g2_id_mapping)

        H = nx.compose(h1, h2)

        ## NODE ATTRIBUTES
        #  Take care of these now
        h1_attr = map( lambda x: x[1].keys(), h1.nodes(data=True))        
        h1_attr = set(item for sublist in h1_attr for item in sublist)

        h2_attr = map( lambda x: x[1].keys(), h2.nodes(data=True))        
        h2_attr = set(item for sublist in h2_attr for item in sublist)        

        common_attr = h1_attr & h2_attr
        h1_unique_attr = h1_attr - common_attr

        # Merge the attributes for nodes in h1 and h2 with a common join field value
        h1_node2attr = {}
        for node, data in h1.nodes_iter(data=True):
            if not self.join_field1 in data:
                continue
            node_idf = data[self.join_field1]

            if not node_idf in common:
                continue
            
            if not node_idf in h1_node2attr:
                h1_node2attr[node_idf] = {}
            for attr in h1_attr:
                if attr in data.keys():
                    if not attr in h1_node2attr[node_idf]:
                        h1_node2attr[node_idf][attr] = [] 
                    h1_node2attr[node_idf][attr].append(data[attr])

        h2_node2attr = h1_node2attr
        for node, data in h2.nodes_iter(data=True):
            if not self.join_field2 in data:
                continue
            node_idf = data[self.join_field2]

            if not node_idf in common:
                continue
            
            if not node_idf in h2_node2attr:
                h2_node2attr[node_idf] = {}
            for attr in h2_attr:
                if attr in data.keys():
                    if not attr in h2_node2attr[node_idf]:
                        h2_node2attr[node_idf][attr] = [] 
                    h2_node2attr[node_idf][attr].append(data[attr])

        # Now attached the combined attributes to the graph
        for node, data in H.nodes_iter(data=True):

            # Does the node have the join field?
            if not self.join_field1 in data and not self.join_field2 in data:
                continue

            # Get the join field value
            node_idf = None
            if self.join_field1 in data:
                node_idf = data[self.join_field1]
            elif self.join_field2 in data:
                node_idf = data[self.join_field2]                

            if node_idf in common:
                for attr in h2_node2attr[node_idf].keys():
                    data[attr] = ",".join( list(set(h1_node2attr[node_idf][attr])) ) #[0]
                    
        for node, data in H.nodes_iter(data=True):
            if self.id_field in data:
                node_ids = data[ self.id_field ].split(',')
                primary_id = node_ids[0]
                data[ self.id_field ] = primary_id
                if len(node_ids) > 1:
                    data[ "cptlc:hasAliases" ] = ",".join(node_ids[1:])
        
                
        self.merged_graph = H
        

    
    

