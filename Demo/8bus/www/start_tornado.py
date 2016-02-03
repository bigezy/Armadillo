import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
import os
import csv
import json
import xml.etree.ElementTree as ET

PORT = 8888
CypsaEnginePath =r"C:\8bus\bin\runCyPSA.bat"
CypsaEngineRoot =r"C:\8bus\bin"
class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        pass
 
    def on_message(self, message):
        a=message.split(",")
        length=len(a)-1
        path=a[length-1]+"/patched.csv"
        fo=open(path,"wb")
        try:
        	writer = csv.writer(fo)
    		writer.writerow( ('IP Address', 'Patch') )
    		for i in range(length):
       			 writer.writerow( (a[i], 1) )
       	finally:
    		fo.close()
    	
    	project=(a[length-1].split("/"))
    	#batFileCmd = CypsaEnginePath+" " + project[len(project)-2] +" " + a[length]
        #from subprocess import Popen
        #p = Popen(batFileCmd, cwd=CypsaEngineRoot)
        #stdout, stderr = p.communicate()
        #self.write_message(data)
        
 
    def on_close(self):
        pass

class XMLSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        pass
 
    def on_message(self, message):
        a=message.split(",")
        project=(a[0].split("/"))
    	#batFileCmd = CypsaEnginePath+" " + project[len(project)-2] +" " + a[1]
    	#print batFileCmd
        #from subprocess import Popen
        #p = Popen(batFileCmd, cwd=CypsaEngineRoot)
        #stdout, stderr = p.communicate()
        xmlfilepath=a[0]+"/pw_analysis_attack_graph_current.xml"
        
        counter=0
        assets = {}
        dup=0
        from xml.etree import ElementTree
        with open(xmlfilepath, 'rt') as f:
        	tree = ElementTree.parse(f)
	        for Nmap in tree.findall('NmapAnalysis'):
	        	source = Nmap.get('sourceNode')
	        	destination = Nmap.get('destinationNode')
	        	for path in Nmap.findall('Path'):
	        		performanceIndex = path.get('performanceIndex')
	        		securityIndex = path.get('securityIndex')
	        		cyberCost = path.get('cyberCost')
	        		for node in path.findall('Node'):
	        			ipAddress = node.get('IPAddress')
	        			vulID = node.get('vulnID')
	        			if ipAddress == source:
	        				type = "source" 
	        			elif ipAddress == destination:
	        				type = "destination"
	        			else:
	        				type = "intermediate"
	        			
	        			for ip in assets:
	        				if (assets[ip][1]==ipAddress and assets[ip][0]==type):
	        					dupkey = ip
	        					dup=1
	        					break
	        			
	        			
	        			if dup == 1:
	        				assets[dupkey][2]+=float(performanceIndex)
	        				assets[dupkey][3]+=float(securityIndex)
	        				assets[dupkey][4]+=float(cyberCost)
	        				assets[dupkey][5]+=1
	        				assets[dupkey][10]+=","+vulID
	        				
	        			else:
	        				arr = []
		        			arr.append(type)
		        			arr.append(ipAddress)
		        			arr.append(float(performanceIndex))
		        			arr.append(float(securityIndex))
		        			arr.append(float(cyberCost))
		        			arr.append(1)
		        			arr.append(0)
		        			arr.append(0)
		        			arr.append(0)
		        			arr.append(0)
		        			arr.append(vulID)
		        			assets[counter] = arr
		        			counter+=1
		        		dup=0
		        		type=""
		        		dupkey=""
		
	 	
	 	xmlfilepath1=a[0]+"/pw_analysis_attack_graph_previous.xml"
	 	from xml.etree import ElementTree
	 	with open(xmlfilepath1,'rt') as f:
		 	for Nmap in tree.findall('NmapAnalysis'):
		 		source = Nmap.get('sourceNode')
		 		destination=Nmap.get('destinationNode')
		 		for path in Nmap.findall('Path'):
		 			performanceIndex = path.get('performanceIndex')
		 			securityIndex = path.get('securityIndex')
		 			cyberCost = path.get('cyberCost')
	        		for node in path.findall('Node'):
	        			ipAddress = node.get('IPAddress')
	        			vulID = node.get('vulnID')
	        			if ipAddress == source:
	        				type = "source" 
	        			elif ipAddress == destination:
	        				type = "destination"
	        			else:
	        				type = "intermediate"
	        				
	        			
	        			for ip in assets:
	        				if (assets[ip][1]==ipAddress and assets[ip][0]==type):
	        					dupkey = ip
	        					dup=1	
	        					break
	        			
	        			if dup == 1:
	        				assets[dupkey][6]+=float(performanceIndex)
	        				assets[dupkey][7]+=float(securityIndex)
	        				assets[dupkey][8]+=float(cyberCost)
	        				assets[dupkey][9]+=1
	        				assets[dupkey][10]+=","+vulID
	        				
	        				
	        			else:
	        				arr = []
		        			arr.append(type)
		        			arr.append(ipAddress)
		        			arr.append(0)
		        			arr.append(0)
		        			arr.append(0)
		        			arr.append(0)
		        			arr.append(float(performanceIndex))
		        			arr.append(float(securityIndex))
		        			arr.append(float(cyberCost))
		        			arr.append(1)
		        			arr.append(vulID)
		        			assets[counter] = arr
		        			counter+=1
		        		dup=0
		        		type=""
		        		dupkey=""
		json_data = json.dumps(assets)
		self.write_message(json_data)
	
	
	def on_close(self):
		pass       
        
class XSLSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        pass
 
    def on_message(self, message):
        a=message.split(",")
        path=a[0]+"/pw_analysis_attack_graph_current.xml"
        fo=open(path,"r")
        data=fo.read()
        self.write_message(data)
 
    def on_close(self):
        pass



class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

def make_app():
    settings = {
        'static_path' : os.path.join(os.path.dirname(__file__),"static"),
        'debug' : 'True'
    }
    handlers = [
  (r'/', MainHandler),
   (r'/websocket', WebSocketHandler),
   (r'/xmlsocket', XMLSocketHandler),
   (r'/xslsocket', XSLSocketHandler),
  (r'/(.*)', tornado.web.StaticFileHandler, {'path': settings['static_path']}),
]
    return tornado.web.Application(handlers,
         **settings)
         
def check_origin(self, origin):
    return True
    
if __name__ == "__main__":
    app = make_app()
    print "Starting server on port " + str(PORT)
    server = tornado.httpserver.HTTPServer(app)
    server.listen(PORT)
    tornado.ioloop.IOLoop.current().start()
