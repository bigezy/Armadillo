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
import json
import logging
import urllib
import urllib2

class FilesystemAnalysesDAO():
    """
    The FilesystemAnalysesDAO is responsible for CRUD operations on a 
      registry of analyses.
    """
    model_basedir = None            
    resolver = None              
    
    def create(self):
        """
        Create a new analysis

        :return:  returns the new analysis's UUID
        """
        raise Exception("method not yet implemented.")

    def retrieve(self, ref_str):
        """
        Retrieve the analysis for the given UUID.

        :param ref_str:  The reference string of the analysis to retrieve
        :return:  returns the analysis interface
        """
        raise Exception("method not yet implemented.")

    def update(self, ref):
        raise Exception("method not yet implemented.")

    def delete(self, ref):
        raise Exception("method not yet implemented.")

    @staticmethod
    def create_dao( model_basedir, resolver_file_name ):
        """
        Create a data access object for analyses

        :param model_basedir:            Base directory for the analyses
        :param resolver_file_name:       Name of the resolver file to use
        """
        fad = FilesystemAnalysesDAO()
        fad.model_basedir = model_basedir

        resolver_file_path = "/".join([model_basedir, "resolvers", resolver_file_name])
        resolver_file = open( resolver_file_path, 'r' )
        fad.resolver = json.load( resolver_file )
        
        return fad
    

class FilesystemGraphsDAO():
    """
    The FilesystemGraphsDAO is responsible for CRUD operations on a 
       graphs available via the local filesystem.
    """

    model_basedir = None            
    resolver = None              
    
    def create(self):
        """
        Create a new graph

        :return:  returns the new graph's UUID
        """
        raise Exception("method not yet implemented.")

    def retrieve(self, ref_str):
        """
        Retrieve the graph for the given UUID.

        :param uuid_str:  The reference string of the graph to retrieve
        :return:  returns the graph data, empty dict if none
        """
        result = {}
        
        if ( ref_str in self.resolver ):
            if ("graph" in self.resolver[ref_str]):
                graph_file_path = "/".join( [ self.model_basedir, self.resolver[ ref_str ]["graph"] ] )
                graph_file = open( graph_file_path, 'r' )
                graph_data = json.load( graph_file )
                result = graph_data
                graph_file.close()
            else:
                result = {}
        else:
            logging.warning("No entry for " + ref_str + " in resolver")
        
        return result

    def update(self, ref):
        raise Exception("method not yet implemented.")

    def delete(self, ref):
        raise Exception("method not yet implemented.")

    @staticmethod
    def create_dao( model_basedir, resolver_file_name ):
        """
        Create a data access object for graphs

        :param model_basedir:            Base directory for the model to operate upon
        :param resolver_file_name:       Name of the resolver file to use within that model
        """
        fgd = FilesystemGraphsDAO()
        fgd.model_basedir = model_basedir

        resolver_file_path = "/".join([model_basedir, "resolvers", resolver_file_name])
        resolver_file = open( resolver_file_path, 'r' )
        fgd.resolver = json.load( resolver_file )
        
        return fgd

class FilesystemImagesDAO():
    """
    The FilesystemImagesDAO is responsible for CRUD operations on a 
       icons available via the local filesystem.
    """

    model_basedir = None            
    resolver = None              
    
    def create(self):
        """
        Create a new graph

        :return:  returns the new graph's UUID
        """
        raise Exception("method not yet implemented.")

    def retrieve(self, ref_str):
        """
        Retrieve the icon for the given UUID.

        :param ref_str:  The reference string of the graph to retrieve
        :return:  returns the image data, empty dict if none
        """
        result = {}
        
        if ( ref_str in self.resolver ):
            image_file_path = "/".join( [ self.model_basedir, self.resolver[ ref_str ]["icon"] ] )
            image_file = open( image_file_path, 'rb' )
            result = image_file.read()
            image_file.close()
        else:
            logging.warning("No entry for " + ref + " in resolver")
        
        return result

    def update(self, ref):
        raise Exception("method not yet implemented.")

    def delete(self, ref):
        raise Exception("method not yet implemented.")

    @staticmethod
    def create_dao( model_basedir, resolver_file_name ):
        """
        Create a data access object for images

        :param model_basedir:            Base directory for the model to operate upon
        :param resolver_file_name:       Name of the resolver file to use within that model
        """
        fid = FilesystemImagesDAO()
        fid.model_basedir = model_basedir

        resolver_file_path = "/".join([model_basedir, "resolvers", resolver_file_name])
        resolver_file = open( resolver_file_path, 'r' )
        fid.resolver = json.load( resolver_file )
        
        return fid
    

class CPTLServerGraphsDAO():
    """
    The URLGraphsDAO is responsible for retrieving CPTL Graphs from another
      CPTL Server
    """
    base_url = None
    resolver = None
    
    def retrieve(self, ref_str):
        """
        Retrieve the graph for the given UUID
        :param uuid_str:  The reference string of the graph to retrieve
        :return:  returns the graph data, empty dict if none
        """

        result = {}
        
        if ( ref_str in self.resolver ):
            if ("cptla:graph_join" in self.resolver[ref_str]):
                graph_url = self.base_url + "/api/v1.0.0/analyses/graph_join"
                params_str = self.resolver[ref_str]["cptla:graph_join"]
                full_url = graph_url + "?" + params_str
                
                req = urllib2.Request(full_url)
                response = urllib2.urlopen(req)
                graph_data_str = response.read()
                graph_data = json.loads(graph_data_str)
                result = graph_data
        else:
            logging.warning("No entry for " + ref_str + " in resolver")

        return result

    def update(self, ref):
        raise Exception("method not yet implemented.")

    def delete(self, ref):
        raise Exception("method not yet implemented.")

    @staticmethod
    def create_dao( base_url, resolver_name=None ):
        """
        Create a data access object for graphs

        :param base_url:            Base directory for the model to operate upon
        :param resolver_name:       Name of the resolver file to use within that model
        """
        csgd = CPTLServerGraphsDAO()
        csgd.base_url = base_url
        return csgd
    
