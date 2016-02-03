#!/usr/bin/env python
import itertools
import json
import argparse
import os
import time
from pprint import pprint
from collections import defaultdict
from graph.graph import Graph
from datetime import datetime
from sets import Set
import traceback
h2h_fwd = {}
h2h_bck = {}
idToIps = {}
ipToIds = {}
netToHosts = {}
hostVulns = {} # Host vulnerabilities
svcVulns = {} # 1x1 svc to vulnerability id
hIdToSvcIds = defaultdict(list)
hSvcIdToCost = {}
limited_targets = {}
global debug
debug = False
errors = Set()
graph_fwd = None
graph_bck = None
attackers = []
easiest = False
dynamic = False
compromised_file = None
patched_file = None
compromised = []
patched = []
entry_node=None
projectPathName=None
# Extract connectivity information from CSV file
def parse_connectivity_file(connectivity_file):

    dictType = ''

    connectivity_file = open(connectivity_file,'r')
    for line in connectivity_file:
        line = line.rstrip()
        if not len(line): continue
        if '#' in line:
            dictType = line.split('#')[1]
            continue

        # Pick up node id and address information
        if dictType == 'Dictionary':
            [id, ip] = line.split(',')
            idToIps[id] = ip
            ipToIds[ip] = id

        # Pick up forward/backward connectivity information
        elif 'Connectivity' in dictType:
            [first, second, protocols] = line.split(u',')
            plist = protocols.split(u'!')
            pset = set([plist[0]])
            for idx in xrange(1, len(plist)):
                pset.add(plist[idx])
            if dictType == 'Forward Connectivity':
                if first not in h2h_fwd:
                    h2h_fwd[first] = {}
                h2h_fwd[first][second] = pset
            else:
                if first not in h2h_bck:
                    h2h_bck[first] = {}
                h2h_bck[first][second] = pset

        # Pick up network host information
        elif dictType == 'Network':
            hosts = line.split(u',')
            net = hosts[0]
            if net not in netToHosts:
                netToHosts[net] = []
            for idx in xrange(1, len(hosts)):
                netToHosts[net].append(hosts[idx])


def pickup_services(tag, dir, hid):
    for k,v in dir.items():
        if k=='attrib' or type(v) == str or type(v) == unicode:
            continue
        else:
            for item in v:
                if k == 'Device':
                    hid = item['attrib']['id']
                    pickup_services('Device',item, hid)
                if k == 'Service':
                    vulns = []
                    svc_name = item['attrib']['product'] + '_' + item['attrib']['version']
                    svc_ports = item['attrib']['protocol'] + '_' + item['attrib']['port']
                    if 'Vulnerability' in item.keys():
                        for vuln in item['Vulnerability']:
                            vulns.append([vuln['attrib']['id'],vuln['attrib']['cvssExploitSubScore']])
                    if not vulns:
                        svcVulns[svc_ports] = svc_name+':'+svc_ports+'#None'
                        hSvcId = hid+'#' + svcVulns[svc_ports]
                        hIdToSvcIds[hid].append(hSvcId)
                        # @TODO what cost should be associated to an open service w/o known vulnerability
                        # We don't want to prune a valid flow b/c missing vuln
                        hSvcIdToCost[hSvcId] = 1000
                    else:
                        for vuln in vulns:
                            svcVulns[svc_ports] = svc_name+':'+svc_ports+'#'+vuln[0]
                            hSvcId = hid+'#' + svcVulns[svc_ports]
                            hIdToSvcIds[hid].append(hSvcId)
                            hSvcIdToCost[hSvcId] = vuln[1]


def parse_topology_file(tfile):
    '''
    Parse service vulnerabilities from .json topology file
    '''
    root = json.load( open(tfile,"r") )
    pickup_services('Topology', root, '')
    if debug:
        print ' - Nodes w/ open services and corresponding vulnerabilities'
        pprint(hSvcIdToCost)


def parse_limited_targets(afile):
    '''
    Parse ip addresses of the only targets to report in the attack graph
    '''
    asset_file = open(afile,'r')
    for line in asset_file:
        line = line.rstrip()
        if not len(line): continue
        if line in ipToIds.keys():
            limited_targets[ipToIds[line]] = line
        else:
            print "Ignoring critical asset " , line, " not in connectivity map"


def parse_compromised_file(cfile):
    global compromised


    '''
    Parse compromised host file, which a CSV file with 2 columns: IP address, compromised flag (0 or 1)
    '''
    with open(cfile, 'r') as handler:
        for line in handler:
            line = line.rstrip()
            fields = line.split(",")
            if not len(line) or len(fields) < 2 or not "," in line:
                continue
            print(fields)
            ip = fields[0]
            flag = fields[1]
            # Removing IP from list of compromised host if the flag is 0
            if (flag == "0" or flag == 0) and ip in compromised:
                compromised.remove(ip)
            # Adding IP to list of compromised host if the flag is 1
            if (flag == "1" or flag == 1) and ip not in compromised:
                compromised.append(ip)


def parse_patched_file(pfile):
    global compromised

    '''
    Parse patched host file, which a CSV file with 2 columns: IP address, patched flag (0 or 1)
    '''
    with open(pfile, 'r') as handler:
        for line in handler:
            line = line.rstrip()
            fields = line.split(",")
            if not len(line) or len(fields) < 2 or not "," in line:
                continue
            ip = fields[0]
            flag = fields[1]
            # Removing IP from list of patched host if the flag is 0
            if (flag == "0" or flag == 0) and ip in patched:
                patched.remove(ip)
            # Adding IP to list of patched host if the flag is 1
            if (flag == "1" or flag == 1) and ip not in patched:
                patched.append(ip)


def format_service(s):
    '''
    Format service string from format in connectivity .csv file
    to format used in the graph.
    tcp:0-65535:102-102 -> tcp_102
    net:0-65535:0-65535 -> ''
    @return: an array of strings [<proto>_<port_nbr>, ..]
    '''
    formatted_svcs = []
    if s.startswith('net:'):
        return None
    tokens = s.split(':')
    if len(tokens) != 3:
        print("WARNING: Unexpected service syntax:", s)
        return None

    # Ignore any port or non tcp/udp protocols
    if s.startswith('ip:') or '0-65535:0-65535' in s:
        return None

    proto = tokens[0]
    ports = tokens[2].split('-')
    if len(ports) != 2:
        errors.add("WARNING: Unexpected service syntax, missing port range:", s)
        return None
    elif ports[0] != ports[1]:
        low = int(ports[0])
        high = int(ports[1])
        # Disaggregate port ranges
        for i in range(low, high+1):
            formatted_svcs.append(proto + '_' + str(i))
        return formatted_svcs

    formatted_svcs.append(proto + '_' + ports[0])
    return formatted_svcs


def build_graph(g, h2h_dict):
    '''
    Build graph with parsed nodes and edges from connectivity
    and vulnerability data
    '''
    # Add hosts as vertices
    print ' - Adding nodes'
    for node_id in idToIps.keys():
        if node_id in hIdToSvcIds.keys():
            for ndSvcId in hIdToSvcIds[node_id]:
                g.addNode(ndSvcId)
                if debug:
                    print 'Adding node',node_id,'('+idToIps[node_id]+')','->',ndSvcId
        else:
            g.addNode(node_id)
            if debug:
                print 'Adding node',node_id,'('+idToIps[node_id]+')'

    # Add edges between hosts with firewall connectivity
    print ' - Adding analysis-reported edges'
    for frm, toDict in h2h_dict.iteritems():
        for to, svcs in toDict.iteritems():
            for svc in svcs:
                # Construct final node id by appending service id 
                # and corresponding vulnerability
                ftd_target = ''
                ftd_svcs = format_service(svc)
                if not ftd_svcs: # Any service
                    ftd_target = to
                else:
                    for ftd_svc in ftd_svcs:
                        if ftd_svc in svcVulns.keys():
                            ftd_target = to + '#' + svcVulns[ftd_svc]
                        else: # No known vulnerability for this service
                            ftd_target = to + '#' + ftd_svc
                        cost = 1000
                        if ftd_target not in hSvcIdToCost.keys():
                            # If analysis reported a flow to a certain node with a given protocol
                            # and nmap (hSvcIdToCost) did not see that service running on that node, drop
                            # this edge
                            if debug:
                                print 'Ignoring analysis edge:',frm,'-',ftd_target
                            continue
                        else:
                            cost = float(hSvcIdToCost[ftd_target])
                        frms = []
                        if frm in hIdToSvcIds.keys():
                            for ndSvcId in hIdToSvcIds[frm]:
                                frms.append(ndSvcId)
                        else:
                            frms.append(frm)
                        for src in frms:
                            g.addArc(src, ftd_target, cost)
                            if debug:
                                print 'Adding analysis edge:[',src,']-',ftd_target,'w/ cost',cost

    # Replace plain host with list of hosts w/ svc id in their name
    print ' - Adding intranet edges'
    for net, hosts in netToHosts.iteritems():
        hosts_wSvcId = []
        for h in hosts:
            if h in hIdToSvcIds.keys():
                for hSvcId in hIdToSvcIds[h]:
                    hosts_wSvcId.append(hSvcId)
            else:
                hosts_wSvcId.append(h)

        for pair in itertools.permutations(hosts_wSvcId, 2):
            # Add edges between hosts in the same network
            h1_wsvc = pair[0]
            h2_wsvc = pair[1]
            h1 = h1_wsvc.split('#',1)[0]
            h2 = h2_wsvc.split('#',1)[0]
            # Skip intranet communication s/ same src and dst
            if h1 == h2: 
                continue
#             if debug:
#                 print 'Adding intranet edge:',h1,'('+idToIps[h1]+')','-',h2,'('+idToIps[h2]+')'
            g.addArc(h1_wsvc, h2_wsvc, 1000 if h2_wsvc not in hSvcIdToCost.keys() else float(hSvcIdToCost[h2_wsvc]))


def prune_edges_by_services():
    '''
    Parse vulnerabilities (actual services running on hosts) from topology XML file
    '''


def generateAttackGraph(graph_fwd, attacker, easiest_only):
    attack_graph = defaultdict(dict)
    attack_graph_nd_only = defaultdict(dict)
    for source in attacker:
        if not source:
            continue
        # print("Source:",source)
        src_nd = source.split('#')[0]
        # Get list of all shortest paths from each attacker:
        try:
            all_paths = graph_fwd.shortestPaths(source, True)
        except Exception, ex:
            # No path found to reach target, or target is invalid
            print("EXCEPTION when computing shortest paths from source "+str(source)+": "+str(ex))
            traceback.print_exc()
            attack_graph[source] = None
            continue;
        # Get path sequence and path weight for each path
        distances = all_paths[0]
        predecessors = all_paths[1]

        if len(distances) == 0:
            attack_graph[source] = None
            continue;
        else:
            attack_graph[source] = {}

        for target in distances:
            dst_nd = target.split('#')[0]
            if dst_nd not in limited_targets.keys():
                continue
            path = graph_fwd.shortestPath(source, target)
            path_weight = graph_fwd.sumPathw(path)
            path_no_vuln = strip_path_vulnerabilities(path)
            new_seq = {'sequence_no_vuln': path_no_vuln,
                    'sequence': path, 
                    'cost': path_weight}
            # Path for this pair of nodes already exists
            if src_nd not in attack_graph_nd_only.keys() or dst_nd not in attack_graph_nd_only[src_nd].keys():
                attack_graph_nd_only[src_nd][dst_nd] = []
            if src_nd in attack_graph_nd_only.keys() and dst_nd in attack_graph_nd_only[src_nd].keys():
                if easiest_only and len(attack_graph_nd_only[src_nd][dst_nd]):
                    #print("Pruning:",src_nd, dst_nd, path_weight,attack_graph_nd_only[src_nd][dst_nd][0]['cost'])
                    # update if cumulative cost is lower than existing path and easiest_only set otherwise add
                    # this other path
                    if path_weight < attack_graph_nd_only[src_nd][dst_nd][0]['cost']:
                        #print("OK:",path_weight, attack_graph_nd_only[src_nd][dst_nd][0]['cost'])
                     # path_no_vuln == attack_graph_nd_only[src_nd][dst_nd][0]['sequence_no_vuln'] \
                     # (len(path_no_vuln) < len(attack_graph_nd_only[src_nd][dst_nd]['sequence_no_vuln'])) or\
                        attack_graph_nd_only[src_nd][dst_nd] = [new_seq]
                    continue
            # Different intermediate nodes or same but more costly
            attack_graph_nd_only[src_nd][dst_nd].append(new_seq)
    for s in attack_graph_nd_only.keys():
        for d in attack_graph_nd_only[s]:
            attack_graph[s][d] = attack_graph_nd_only[s][d]
    return attack_graph


def strip_path_vulnerabilities(nodes):
    path_no_vulns = []
    for nd in nodes:
        path_no_vulns.append(nd.split('#')[0]) 
    return path_no_vulns

#looks up a node by IP address
def lookupIP(nodeIP):
    nodeId = None
    if nodeIP in ipToIds.keys():
      nodeId = ipToIds[nodeIP];
    return nodeId;

	
def lookupNode(nodeId):
    info = "N/A"
    if '#' in nodeId:
        toks = nodeId.split('#')
        nodeId = toks[0]
    if nodeId in idToIps.keys():
        info = idToIps[nodeId]
    return str(info)


def parseNodeString(node):
    nodeId = node
    service = None
    vulnId = None

    if "#" in node:
        tmp = node.split("#")
        nodeId = tmp[0]
        if len(tmp) > 2:
            service = tmp[1]
            vulnId = tmp[2]

    nodeIP = lookupNode(nodeId)

    return [nodeId, nodeIP, service, vulnId]

#Checks to see if we should skip this IP address or not in attack graph generation.
#If the IP address is is a patched vulnerability, we will not add it to the attack graph
def pruneIP(ip_addr):
    return ip_addr in patched	

def saveXML(attack_graph, filename):
    xml = XMLHeader()
    xml += u'<VCReport type="vuln">\n' 
    print("Attack graph keys:", attack_graph.keys())
    for attacker in attack_graph.keys():
        if attacker is None or attack_graph[attacker] is None:
            continue
        #if attacker is None:#or attack_graph[attacker] is None:
         #   continue
        ##   if pruneIP(attacker_ip):
           #    continue
          #  path = u'    <NmapAnalysis sourceNode="'+str(lookupNode(attacker))+'" sourceNodeId="'+str(attacker)+'" destinationNode="'+str(lookupNode(attacker))+'" destinationNodeId="'+str(attacker)+'">\n'
          #  path += u'        <Path attackNode="'+str(lookupNode(attacker))+'" nodeId="'+str(attacker)+'" cost="0">\n'
           # node_vuln = None
            #path += u'            <Node IPAddress="'+str(lookupNode(attacker))+'" nodeId="'+str(attacker)+'" vulnID="'+str(node_vuln)+'"/>\n'
           # path += u'        </Path>\n'
            #path += u'    </NmapAnalysis>\n'
            #xml += path
            #continue
        [attacker_id, attacker_ip, attacker_service, attacker_vuln] = parseNodeString(attacker)
        #Luis: make sure the ip is not in compromised set or patched set
        if pruneIP(attacker_ip):
            continue
			
        for asset in attack_graph[attacker].keys():
            [asset_id, asset_ip, asset_service, asset_vuln] = parseNodeString(asset)
            if pruneIP(asset_ip): 
                continue
            for seq in attack_graph[attacker][asset]:
                prune = False
                cost = seq['cost']
                sequence = seq['sequence']
                path = u'    <NmapAnalysis sourceNode="'+str(attacker_ip)+'" sourceNodeId="'+str(attacker_id)+'" destinationNode="'+str(asset_ip)+'" destinationNodeId="'+str(asset_id)+'">\n'
                path += u'        <Path attackNode="'+str(attacker_ip)+'" nodeId="'+str(attacker_id)+'" cost="'+str(cost)+'">\n'
                node_vuln = None
                for n in sequence:
                    [node_id, node_ip, node_service, node_vuln] = parseNodeString(n)
                    if pruneIP(node_ip): 
                        prune = True
                        break
                    path += u'            <Node IPAddress="'+str(node_ip)+'" nodeId="'+str(node_id)+'" vulnID="'+str(node_vuln)+'"/>\n'
                path += u'        </Path>\n'
                path += u'    </NmapAnalysis>\n'
                # \TODO: Will be done through pruning:
                if node_vuln is not None and attacker_id != asset_id:
                 # Prune out paths w/o either cost information nor vulnerability
                    if cost == 'None' or not node_vuln or node_vuln == "None":
                         continue
                    if attacker_id != asset_id and not prune:
                        xml += path
    xml += u'</VCReport>\n'

    with open(filename, 'wb') as f:
        f.write(xml)


def XMLHeader():
    header = """<?xml version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE VCReport [
<!ELEMENT VCReport ((NetCenter|HostCenter|NmapAnalysis)*, Endpoint*)>
<!ATTLIST VCReport type CDATA #REQUIRED>
<!ELEMENT NetCenter (Network,Intensity*)>
<!ELEMENT HostCenter (Host,Intensity*)>
<!ELEMENT Endpoint EMPTY>
<!ATTLIST Endpoint IPAddress CDATA #REQUIRED>
<!ATTLIST Endpoint depth CDATA #REQUIRED>
<!ATTLIST Endpoint width CDATA #REQUIRED>
<!ELEMENT Network EMPTY>
<!ATTLIST Network netAddress CDATA #REQUIRED>
<!ELEMENT Host EMPTY>
<!ATTLIST Host IPAddress CDATA #REQUIRED>
<!ELEMENT Intensity EMPTY>
<!ATTLIST Intensity depth CDATA #REQUIRED>
<!ATTLIST Intensity width CDATA #REQUIRED>
<!ELEMENT Description (#PCDATA)>
<!ELEMENT NmapAnalysis (Path*)>
<!ATTLIST NmapAnalysis sourceNode CDATA #REQUIRED>
<!ATTLIST NmapAnalysis sourceNodeId CDATA #REQUIRED>
<!ATTLIST NmapAnalysis destinationNode CDATA #REQUIRED>
<!ATTLIST NmapAnalysis destinationNodeId CDATA #REQUIRED>
<!ATTLIST NmapAnalysis timeTaken CDATA #IMPLIED>
<!ELEMENT Path (Node*)>
<!ATTLIST Path attackNode CDATA #REQUIRED>
<!ATTLIST Path nodeId CDATA #REQUIRED>
<!ATTLIST Path cost CDATA #REQUIRED>
<!ELEMENT Node EMPTY>
<!ATTLIST Node IPAddress CDATA #REQUIRED>
<!ATTLIST Node nodeId CDATA #REQUIRED>
<!ATTLIST Node vulnID CDATA #REQUIRED>
]>
"""
    return header


def init():
    global graph_bck, graph_fwd, attackers, easiest, dynamic, compromised_file, patched_file, entry_node, projectPathName

    parser = argparse.ArgumentParser(description='Produces attack graph.')
    parser.add_argument('-c', 
                        metavar = 'CSV connectivity file', 
                        dest='cfile',
                        default="connectivity.csv",
                        required=False)
    parser.add_argument(u'-t', 
                        metavar = 'JSON topology file', 
                        dest='tfile',
                        default="topology-dict.json",
                        required=False)
    parser.add_argument(u'-a', 
                        metavar = 'TXT asset ip file', 
                        dest='afile',
                        default="critical_assets.txt",
                        help='file containing ip addresses of interesting targets to consider',
                        required=False)
    parser.add_argument(u'-i',
                        metavar = 'CSV compromised ip file',
                        dest='compromised',
                        default="compromised.csv",
                        help='file containing ip addresses of hosts that are compromised',
                        required=False)
    parser.add_argument(u'-p',
                        metavar = 'CSV patched ip file',
                        dest='patched',
                        default="patched.csv",
                        help='file containing ip addresses of hosts that are patched',
                        required=False)
    parser.add_argument(u'-s',
                        dest='easiest', action='store_const', const=True,
                        help='if the same path with different vulnerabilities is possible, only report the easiest (smallest cumulative vulnerability)',
                        required=False)
    parser.add_argument(u'-d',
                        dest='dynamic', action='store_const', const=True,
                        help='tells the process to run continuously and to monitor changes in the compromised hosts and patched hosts files',
                        required=False)
    parser.add_argument(u'-e',
                        metavar= 'Entry node IP address',
                        dest='entry', 
                        default="127.0.0.1",
                        help='entry node of the attack graph',
                        required=False) 
    parser.add_argument(u'-n',
                        metavar = 'name of project',
                        dest='projectName',
                        default="8bus",
                        help='file containing ip addresses of hosts that are compromised',
                        required=False)
    args = parser.parse_args()
    easiest = args.easiest
    dynamic = args.dynamic
    compromised_file = args.compromised
    patched_file = args.patched
    entry_node=args.entry
    projectPathName=args.projectName
    # Init forward and backward graphs
    graph_fwd = Graph()
    graph_bck = Graph()

    # Parse connectivity info (vertices and edges)
    print "Parse connectivity .csv file",args.cfile
    parse_connectivity_file(args.cfile)

    # Parse vulnerability metrics from topology .json file
    print "Parse vulnerabilities from topology .json file",args.tfile
    parse_topology_file(args.tfile)

    # Parse limited targets if provided
    if os.path.isfile(args.afile):
        print "Parse limited target file",args.afile
        parse_limited_targets(args.afile)
        if len(limited_targets):
            print " - Will limit attack graph to these",len(limited_targets),"targets:",limited_targets.values()

    return True


def make_graph():
    # Build graphs using connectivity and vulnerability data parsed
    print "Building forward graph..."
    build_graph(graph_fwd, h2h_fwd)
    print "Building backward graph..."
    build_graph(graph_bck, h2h_bck)

    if debug:
        print '\nAll arcs w/ weight in forward graph'
        print("-------------------")
        pprint(graph_fwd.arcsw())
    #pprint(graph_fwd)
    # Print errors
    for e in errors:
        print e

    print "Graph statistics:"
    print("-------------------")
    print(graph_fwd.viewStats())
    print("-------------------")

    #pprint(graph_bck.nodes())

    # Save to dot file for display in GraphViz
#     print "Producing .dot graphs"
#     graph_fwd.saveDot(fileName="h2h_fwd.dot")

    # Commented because not perfectly symmetrical with graph_fwd
    #graph_bck.saveDot(fileName="h2h_bck.dot")

    #print "Shortest path b/w '1734', '1718' is ", graph_fwd.shortestPath('1734', '1718')

    # List of critical assets:
    #assets = [u'1884#http-proxy_:tcp_8080#CVE-2006-5036']
    #assets = ['1884']
    #assets = ['1884#http-proxy_:tcp_8080#CVE-2005-2729']

def append_node_by_ip(ip,attackers):
    print("-You selected IP:",ip)
    print("-We found the following hIds:",hIdToSvcIds[lookupIP(ip)])
    node_id = lookupIP(ip)
    if node_id in hIdToSvcIds.keys():
        if not hIdToSvcIds[node_id]:
            if node_id in graph_fwd:
                print("appending: ", node_id)
                attackers.append(node_id)
            else:
                print("node_id was not in graph_fwd!")
        else:
            for ndSvcId in hIdToSvcIds[node_id]:
                if ndSvcId in graph_fwd :
                    print("appending: ",ndSvcId)
                    attackers.append(ndSvcId)
                else:
                    print("ndSvcId was not in Graph_fwd!");
    else:
        print("node_id was not in hidtosvcids.keys()")
        if node_id in graph_fwd:
            print("appending: ", node_id)
            attackers.append(node_id)
        else:
            print("node_id was not in graph_fwd!")

def compute_attack(full=False):
    attackers = []
    if full:
        for n in graph_fwd.nodes():
            attackers.append(n)
    else:
        
        append_node_by_ip(entry_node,attackers)
        #Append compromised nodes
        for ip in compromised:
            append_node_by_ip(ip,attackers)
 
 
    #attackers.append('1884')

    # Build attack graph for attackers     
    print "Generating attack graph..."
    print datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
    attack_graph = generateAttackGraph(graph_fwd, attackers, easiest)
    print datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
    print "Final attack graph generated for the list of attackers: ", attackers
    pprint(attack_graph)
    t = datetime.strftime(datetime.now(), '%Y-%m-%d-%H-%M-%S')
    fName = projectPathName+"\\attack_graph\\attack_graph-"+t+".xml"
    # Save attack graph to XML
    print "Attack graph exported to XML format and saved in file attack_graph.xml"
    saveXML(attack_graph, fName)


if __name__ == '__main__':
    success = init()
	#initial attack graph calculation:
    make_graph()
    compute_attack(False)

    if success and dynamic:
        print("Starting dynamic mode: monitoring files compromised.csv and patched.csv for changes")

        if not os.path.isfile(compromised_file) and not os.path.isfile(patched_file):
            print("Error: no file to monitor ("+compromised_file+" and "+patched_file+" do not exist)")
        else:
            compromised_file_timestamp = 0
            patched_file_timestamp = 0
            compromised_updated = False
            patched_updated = False

            while True:
                if os.path.isfile(compromised_file):
                    if compromised_file_timestamp != os.stat(compromised_file).st_mtime:
                        print("Change detected in "+compromised_file)
                        compromised_updated = True
                        parse_compromised_file(compromised_file)
                        compromised_file_timestamp = os.stat(compromised_file).st_mtime

                if os.path.isfile(patched_file):
                    if patched_file_timestamp != os.stat(patched_file).st_mtime:
                        print("Change detected in "+patched_file)
                        patched_updated = True
                        parse_patched_file(patched_file)
                        patched_file_timestamp = os.stat(patched_file).st_mtime

                if compromised_updated or patched_updated:
                    print("    Compromised host(s): "+str(compromised))
                    print("    Patched host(s):     "+str(patched))
                    print("    #TODO: update attack graph based on detected changes")
                    compromised_updated = False
                    patched_updated = False
                    compute_attack()
                   
                time.sleep(1)