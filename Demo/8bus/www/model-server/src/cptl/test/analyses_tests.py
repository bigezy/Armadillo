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
import ConfigParser
import json
import networkx as nx
import unittest

from cptl.analyses import CPTLGraphJoin
from cptl.daos import FilesystemGraphsDAO
from networkx.readwrite import json_graph

import unittest

class CPTLGraphJoinTest(unittest.TestCase):

    fgd = None
    
    def setUp(self):
        Config = ConfigParser.ConfigParser()
        Config.read("config/tests.ini")
        section = "CPTLGraphJoinTest"

        model_basedir = Config.get( section, "model_basedir" )
        resolver_file_name = Config.get( section, "resolver_file_name" )

        self.fgd = FilesystemGraphsDAO.create_dao(model_basedir, resolver_file_name)

    def test_merge_graphs(self):
        cgj = CPTLGraphJoin()
        cgj.id_field = "cptlc:hasUUID"
        cgj.join_field1 = "cptlc:hasURI"
        cgj.join_field2 = "cptlc:hasURI"        
        cgj.graphs_dao = self.fgd
        
        graph_ref1 = "e9adc3b5-ba85-4a0d-82f3-4bec283fe086"
        graph_ref2 = "0720ba06-dc7a-46f8-9543-c2caf2676077"

        cgj.merge_graphs(graph_ref1, graph_ref2)
        
        self.assertEqual( 23, nx.number_of_nodes(cgj.merged_graph) )
        self.assertEqual( 34, nx.number_of_edges(cgj.merged_graph) )        

        cgj.merge_graphs(graph_ref2, graph_ref1)
        
        self.assertEqual( 23, nx.number_of_nodes(cgj.merged_graph) )
        self.assertEqual( 34, nx.number_of_edges(cgj.merged_graph) )                

        cgj.id_field = "cptlc:hasUUID"
        cgj.join_field1 = "rdfs:label"        
        cgj.join_field2 = "enet:hasIPAddressValue"
        cgj.graphs_dao = self.fgd

        graph_ref1 = "329e832d-1be2-4094-8722-f91d37595c10"
        graph_ref2 = "514d63aa-1fcf-423b-880d-168bac34354f"

        cgj.merge_graphs(graph_ref1, graph_ref2)
        merged_graph = cgj.get_merged_graph()

        cgj.id_field = "cptlc:hasUUID"
        cgj.join_field1 = "rdfs:label"        
        cgj.join_field2 = "enet:hasIPAddressValue"
        cgj.graphs_dao = self.fgd

        graph_ref1 = "329e832d-1be2-4094-8722-f91d37595c10"  # Control Center Network
        graph_ref2 = "0720ba06-dc7a-46f8-9543-c2caf2676077"  # Odgenville Substation Network

        cgj.merge_graphs(graph_ref1, graph_ref2)
        merged_graph = cgj.get_merged_graph()
        cgj.output_graph("/tmp/out")
        
if __name__ == '__main__':
    suite1 = unittest.TestLoader().loadTestsFromTestCase(CPTLGraphJoinTest)
    unittest.TextTestRunner(verbosity=2).run(suite1)
