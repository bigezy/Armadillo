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
import cptl.daos 
import ConfigParser
import unittest

class FilesystemAnalysesDAOTest(unittest.TestCase):

    fad = None
    
    def setUp(self):
        Config = ConfigParser.ConfigParser()
        Config.read("config/tests.ini")
        section = "FilesystemAnalysesDAOTest"
        
        model_basedir = Config.get( section, "model_basedir" )
        resolver_file_name = Config.get( section, "resolver_file_name" )

        self.fad = cptl.daos.FilesystemAnalysesDAO.create_dao(model_basedir, resolver_file_name)
        

class FilesystemGraphsDAOTest(unittest.TestCase):

    fdg = None
    
    def setUp(self):
        Config = ConfigParser.ConfigParser()
        Config.read("config/tests.ini")
        section = "FilesystemGraphsDAOTest"
        
        model_basedir = Config.get( section, "model_basedir" )
        resolver_file_name = Config.get( section, "resolver_file_name" )

        self.fgd = cptl.daos.FilesystemGraphsDAO.create_dao(model_basedir, resolver_file_name)
        
    def test_retrieve(self):
        ref_str = "514d63aa-1fcf-423b-880d-168bac34354f"
        graph_data = self.fgd.retrieve(ref_str)
        self.assertEquals( len(graph_data["nodes"]), 179 )

class FilesystemImagesDAOTest(unittest.TestCase):

    fid = None

    def setUp(self):
        Config = ConfigParser.ConfigParser()
        Config.read("config/tests.ini")
        section = "FilesystemImagesDAOTest"
        
        model_basedir = Config.get( section, "model_basedir" )
        resolver_file_name = Config.get( section, "resolver_file_name" )

        self.fid = cptl.daos.FilesystemImagesDAO.create_dao(model_basedir, resolver_file_name)
        
    def test_retrieve(self):
        ref_str = "syard:Bus"
        image_data = self.fid.retrieve(ref_str)
        self.assertTrue( image_data != None )

class CPTLServerGraphsDAOTest(unittest.TestCase):
    """
    Still under development! 
    """
    csgd = None
    
    def setUp(self):
        Config = ConfigParser.ConfigParser()
        Config.read("config/tests.ini")
        section = "CPTLServerGraphsDAOTest"
        
        base_url = Config.get( section, "base_url" )
        resolver_name = None #Config.get( section, "resolver_name" )
        self.csgd = cptl.daos.CPTLServerGraphsDAO.create_dao(base_url)
        
    def test_retrieve(self):
        ref_str = "4adddaa9-d137-4a0b-ae20-9344e6a2336e"
        graph_data = self.csgd.retrieve(ref_str)
        self.assertEquals( len(graph_data["nodes"]), 23 )
        
        
if __name__ == '__main__':
    suite0 = unittest.TestLoader().loadTestsFromTestCase(FilesystemAnalysesDAOTest)    
    suite1 = unittest.TestLoader().loadTestsFromTestCase(FilesystemGraphsDAOTest)
    suite2 = unittest.TestLoader().loadTestsFromTestCase(FilesystemImagesDAOTest)
    unittest.TextTestRunner(verbosity=2).run(suite0)
    unittest.TextTestRunner(verbosity=2).run(suite1)
    unittest.TextTestRunner(verbosity=2).run(suite2)

