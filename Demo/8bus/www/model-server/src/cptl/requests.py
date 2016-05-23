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
import cptl.analyses
import cptl.daos
import ConfigParser
import json
import logging
import tornado.template
import tornado.web

class AnalysesRequestHandler(tornado.web.RequestHandler):

    fgd = None
    
    def initialize(self, config_file):
        Config = ConfigParser.ConfigParser()
        Config.read(config_file)

        section = "AnalysesRequestHandler"
        model_basedir = Config.get( section, "model_basedir" )
        resolver_file_name = Config.get( section, "resolver_file_name" )
        self.fad = cptl.daos.FilesystemAnalysesDAO.create_dao(model_basedir, resolver_file_name)
        
    def get(self, uuid=None):

        if (uuid != None):
            if not uuid in self.fad.resolver[uuid]:
                logging.error()
            self.write( json.dumps( graph_data, indent=2 ) );
        else:
            self.write( json.dumps( self.fad.resolver, indent=2 ) );

        self.set_header("Content-Type", "application/json")
        self.set_header("Access-Control-Allow-Origin", "http://localhost:8888")
        self.set_header("Access-Control-Allow-Credentials", "true")

class GraphJoinAnalysisRequestHandler(tornado.web.RequestHandler):

    cgj = None
    
    def initialize(self, config_file):
        Config = ConfigParser.ConfigParser()
        Config.read(config_file)

        section = "GraphJoinAnalysisRequestHandler"
        model_basedir = Config.get( section, "model_basedir" )
        resolver_file_name = Config.get( section, "resolver_file_name" )
        self.cgj = cptl.analyses.CPTLGraphJoin()
        self.cgj.graphs_dao = cptl.daos.FilesystemGraphsDAO.create_dao(model_basedir, resolver_file_name)        

    def get(self):
        graph_ref1 = self.get_arguments("graph_ref1")[0]
        graph_ref2 = self.get_arguments("graph_ref2")[0]
        id_field = self.get_arguments("id_field")[0]
        join_field1 = self.get_arguments("join_field1")[0]
        join_field2 = self.get_arguments("join_field2")[0]        
        
        if ( graph_ref1 != None and graph_ref2 != None and
             id_field != None and join_field1 != None
             and join_field2 != None):

            self.cgj.id_field = id_field
            self.cgj.join_field1 = join_field1
            self.cgj.join_field2 = join_field2

            self.cgj.merge_graphs(graph_ref1, graph_ref2)
            merged_graph = self.cgj.get_merged_graph()
            self.write( json.dumps(merged_graph, indent=2) )
        else:
            self.write( json.dumps( { "graph_ref1": graph_ref1, "graph_ref2":graph_ref2, "join_field1":join_field1, "join_field2":join_field2 }, indent=2 ) )

        self.set_header("Content-Type", "application/json")
        self.set_header("Access-Control-Allow-Origin", "http://localhost:8008")
        self.set_header("Access-Control-Allow-Credentials", "true")
            
class GraphsRequestHandler(tornado.web.RequestHandler):

    csgd = None
    fgd = None
    
    def initialize(self, config_file):
        Config = ConfigParser.ConfigParser()
        Config.read(config_file)

        section = "GraphsRequestHandler"
        model_basedir = Config.get( section, "model_basedir" )
        resolver_file_name = Config.get( section, "resolver_file_name" )
        self.fgd = cptl.daos.FilesystemGraphsDAO.create_dao(model_basedir, resolver_file_name)
        
    def get(self, uuid=None):

        if (uuid != None):
            graph_data = self.fgd.retrieve( uuid )
            if (graph_data):  
                self.write( json.dumps( graph_data, indent=2 ) )
        else:
            self.write( json.dumps( self.fgd.resolver, indent=2 ) )

        self.set_header("Content-Type", "application/json")
        self.set_header("Access-Control-Allow-Origin", "http://localhost:8888")
        self.set_header("Access-Control-Allow-Credentials", "true")


class IconsRequestHandler(tornado.web.RequestHandler):

    fid = None
    
    def initialize(self, config_file):
        Config = ConfigParser.ConfigParser()
        Config.read(config_file)

        section = "IconsRequestHandler"
        model_basedir = Config.get( section, "model_basedir" )
        resolver_file_name = Config.get( section, "resolver_file_name" )
        self.fid = cptl.daos.FilesystemImagesDAO.create_dao(model_basedir, resolver_file_name)
        
    def get(self, uuid=None):

        if (uuid != None):
            graph_data = self.fid.retrieve( uuid )
            self.write( graph_data );
            self.set_header("Content-Type", "image/png")
        else:
            self.write( json.dumps( self.fid.resolver, indent=2 ) );
            self.set_header("Content-Type", "application/json")
            
        self.set_header("Access-Control-Allow-Origin", "http://localhost:8888")
        self.set_header("Access-Control-Allow-Credentials", "true")

        
