import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
import os
import os.path
import csv
import json
import time
import sys
import subprocess
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import xml.etree.ElementTree as ET

PORT = 8888
flag = "a"
CypsaEnginePath =r"C:\armadillo\Demo\8bus\bin\runCyPSA.bat"
CypsaEngineRoot =r"C:\armadillo\Demo\8bus\bin"
globalPath = ""


class MyHandler(FileSystemEventHandler):
    patterns = ["*.xml", "*.lxml"]

    def process(self, event):
        print "Watch Dog"
        event.event_type = 'modified'
        event.is_directory = True
        projectPath = event.src_path
        # the file will be processed there
        print event.src_path, event.event_type, projectPath[len(projectPath) - 1]
        #self.runCypsa(projectPath)

    def on_modified(self, event):
        #print "modified"
        global flag
        flag = "b"
        print "File got Modified..."
        print "Updating the UI..."

    def on_created(self, event):
        self.process(event)

    def runCypsa(self, projectPath):
        project=projectPath.split("\\")
        batFileCmd = CypsaEnginePath+" " + project[len(project)-2] +" " + "10.1.31.101"+" " + "offline"
        print batFileCmd
        #from subprocess import Popen
        #p = Popen(batFileCmd, cwd=CypsaEngineRoot)
        #stdout, stderr = p.communicate()
        #xmlHandler = XMLSocketHandler(self,tornado.websocket.WebSocketHandler)
        xmlHandler.on_message(projectPath)


class timerSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        #print "Hello"
        if flag=="a":
            print "No Modified File Found.."
        else:
            print "File Modified.."
        self.write_message(flag)
        pass

    def on_message(self, message):
        global flag
        s=""
        #self.write_message("hello")
        if flag == "b":
            #read PID's
            #save them in an array
            filepath=globalPath+"/pw_analysis_attack_graph_current.xml"
            prevfilepath=globalPath+"/pw_analysis_attack_graph_previous.xml"
            print "This is csvfile path timer "+filepath
            percentage=0
            sumtotal=0
            counter=0
            assets = {}
            dup=0
            csvfilepath=globalPath+"/patched.csv"
            print "This is csvfile path timer"+csvfilepath
            patched = []
            #read patched csv file and store elements already patched
            if os.path.isfile(csvfilepath):
                with open(csvfilepath) as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        if(row['Patch']=="1"):
                            patched.append(row['IP Address'])
                    #else:
                    #    print row['Patch']
            #print patched[1]
            if os.path.isfile(filepath):
                tree = ET.parse(filepath)
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
                                percentage+=float(securityIndex)
                                sumtotal+=1
                                assets[dupkey][11]=percentage
                                assets[dupkey][12]=sumtotal
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
                                percentage+=float(securityIndex)
                                sumtotal+=1
                                arr.append(percentage)
                                arr.append(sumtotal)
                                if(ipAddress in patched):
                                    arr.append(1)
                                else:
                                    arr.append(0)
                                assets[counter] = arr
                                counter+=1
                            dup=0
                            type=""
                            dupkey=""
            if os.path.isfile(prevfilepath):
                tree = ET.parse(prevfilepath)
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
                            assets[dupkey][11]=percentage
                            assets[dupkey][12]=sumtotal
                            print assets[dupkey]


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
                            arr.append(percentage)
                            arr.append(sumtotal)
                            if(ipAddress in patched):
                                arr.append(1)
                            else:
                                arr.append(0)
                            assets[counter] = arr
                            counter+=1
                        dup=0
                        type=""
                        dupkey=""

            for ip in assets:
                assets[ip][11]=percentage
                assets[ip][12]=sumtotal
            json_data = json.dumps(assets)
            flag = "a"
            self.write_message(json_data)
        else:
            self.write_message(flag)

    def on_close(self):
        pass


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        pass

    def on_message(self, message):
        a=message.split(",")
        length=len(a)-1
        path=a[0]+"/patched.csv"
        fo=open(path,"wb")
        try:
            writer = csv.writer(fo)
            writer.writerow( ('IP Address', 'Patch') )
            for i in range(2,length+1):
                b=a[i].split("-")
                writer.writerow( (b[0], b[1]) )
        finally:
            fo.close()

            #project=(a[length-1].split("/"))
            #batFileCmd = CypsaEnginePath+" " + project[len(project)-2] +" " + a[length]
            #from subprocess import Popen
            #p = Popen(batFileCmd, cwd=CypsaEngineRoot)
            #stdout, stderr = p.communicate()
            #self.write_message(data)


    def on_close(self):
        pass

class CompWebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        pass

    def on_message(self, message):
        a=message.split(",")
        length=len(a)-1
        path=a[length-1]+"/compromised.csv"
        fo=open(path,"wb")
        try:
            writer = csv.writer(fo)
            writer.writerow( ('IP Address', 'Patch') )
            for i in range(length-1):
                print a[i]
                writer.writerow( (a[i], 1) )
        finally:
            fo.close()

            project=(a[length-1].split("/"))
            #self.write_message(data)


    def on_close(self):
        pass


class StopAnalysisWebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        pass

    def on_message(self, message):
        print "Killing process : %s" % time.ctime()
        #time.sleep(60)
        #print "End : %s" % time.ctime()
        command="taskkill /f"
        print os.getcwd()
        file = open('../bin/PIDs.txt', 'r')
        for line in file:
            s=line
            s=s.strip()
            command=command+" /pid "+s
        print command
        os.system(command)


    def on_close(self):
        pass


class CypsaAnalysisWebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        pass

    def on_message(self, message):
        projectinfo=(message.split(","))
        project=projectinfo[0].split("/")
        reply="This is Cypsa analysis project: "+projectinfo[0]
        batFileCmd = CypsaEnginePath+" " + project[len(project)-2] +" " + projectinfo[1]
        print "Compromised process:"+batFileCmd
        cwdir=os.getcwd()
        os.chdir(CypsaEngineRoot)
        #time.sleep(15)
        from subprocess import Popen
        p = Popen(batFileCmd, cwd=CypsaEngineRoot)
        stdout, stderr = p.communicate()
        print os.getcwd()
        os.chdir(cwdir)
        self.write_message(reply)


    def on_close(self):
        pass

class CompFileWebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        pass

    def on_message(self, message):
        path=message+"/host_ips.csv"
        filedata=""
        with open(path, 'rb') as csvfile:
            for line in csvfile:
                filedata=filedata+line+"/n"
        self.write_message(filedata)
            #project=(a[length-1].split("/"))
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
        global globalPath
        a=message.split(",")
        project=(a[0].split("/"))
        #batFileCmd = CypsaEnginePath+" " + project[len(project)-2] +" " + a[1]
        #print batFileCmd
        #from subprocess import Popen
        #p = Popen(batFileCmd, cwd=CypsaEngineRoot)
        #stdout, stderr = p.communicate()
        xmlfilepath=a[0]+"/pw_analysis_attack_graph_current.xml"
        csvfilepath=a[0]+"/patched.csv"
        percentage=0
        sumtotal=0
        counter=0
        assets = {}
        dup=0
        patched = []
        #read patched csv file and store elements already patched
        with open(csvfilepath) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if(row['Patch']=="1"):
                    patched.append(row['IP Address'])
                else:
                    print row['Patch']
        #print patched[1]
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
                            percentage+=float(securityIndex)
                            sumtotal+=1
                            assets[dupkey][11]=percentage
                            assets[dupkey][12]=sumtotal

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
                            percentage+=float(securityIndex)
                            sumtotal+=1
                            arr.append(percentage)
                            arr.append(sumtotal)
                            if(ipAddress in patched):
                                arr.append(1)
                            else:
                                arr.append(0)
                            assets[counter] = arr
                            counter+=1
                        dup=0
                        type=""
                        dupkey=""


            xmlfilepath1=a[0]+"/pw_analysis_attack_graph_previous.xml"
            if os.path.isfile(xmlfilepath1):
                from xml.etree import ElementTree
                with open(xmlfilepath1,'rt') as f:
                    tree = ElementTree.parse(f)
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
                                    assets[dupkey][11]=percentage
                                    assets[dupkey][12]=sumtotal
                                    print assets[dupkey]


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
                                    arr.append(percentage)
                                    arr.append(sumtotal)
                                    if(ipAddress in patched):
                                        arr.append(1)
                                    else:
                                        arr.append(0)
                                    assets[counter] = arr
                                    counter+=1
                                dup=0
                                type=""
                                dupkey=""



            for ip in assets:
                assets[ip][11]=percentage
                assets[ip][12]=sumtotal
            json_data = json.dumps(assets)
            event_handler = MyHandler()
            args = a[0]
            if args:
                print args[0]
            else:
                print "helo"
            observer = Observer()
            observer.schedule(event_handler, path=a[0], recursive=False)
            observer.start()
            globalPath=a[0]
            print globalPath+" This is intializing"
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
        loader = tornado.template.Loader("static")
        #self.write(loader.load("static/CypsaAnalysisProject.html").generate(title="Awesome"))
        self.render("index.html")

def make_app():

    settings = {
        'static_path' : os.path.join(os.path.dirname(__file__),"static"),
        'debug' : 'True'
    }
    handlers = [
        (r'/', MainHandler),
        (r'/', MyHandler),
        (r'/websocket', WebSocketHandler),
        (r'/timersocket', timerSocketHandler),
        (r'/xmlsocket', XMLSocketHandler),
        (r'/xslsocket', XSLSocketHandler),
        (r'/compwebsocket', CompWebSocketHandler),
        (r'/startcypsasocket',CypsaAnalysisWebSocketHandler),
        (r'/stopcypsasocket',StopAnalysisWebSocketHandler),
        (r'/compfilewebsocket', CompFileWebSocketHandler),
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
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
