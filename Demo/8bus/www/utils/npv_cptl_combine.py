import sys
import copy
import json
import pprint
import traceback
import argparse
import os.path
import xml.etree.ElementTree as ET
from collections import defaultdict

# Export NPView topology information to D3 json format (nodes/links)
# and merge-in cptl nodes

def load_npv_topo (input_topo_file, cptl_dict):
    '''
    Parse topology.xml and save into D3 json dict
    '''
    i = 0
    node_id_map = {}  # 1x1 device id to d3 node id (strxint)
    links = defaultdict(list)  # 1x1 srcxdst strxstr
    d3_dict = {'nodes': [], 'links': []}

    # Open topology.xml file
    try:
        tree = ET.parse(input_topo_file)
        root = tree.getroot()
    except Exception,e:
        print 'Exception parsing file',input_topo_file,'.\n',str(e)

    # Extract devices
    for dev in root.iter('Device'):
        dev_type = unicode(dev.attrib['type'], "utf-8")
        dev_name = unicode(dev.attrib['name'], "utf-8")
        dev_id = unicode(dev.attrib['id'], "utf-8")
        dev_addrs = set()
        node_id_map[dev_id] = i
        i += 1
        if 'nodeRefId' in dev.attrib:
            noderef = dev.attrib['nodeRefId']
            if noderef:
                links[dev_id].extend(noderef.split(';'))
        for nic in dev.iter('NIC'):
            ip = nic.attrib['ipAddress']
            if ip != 'unknown':
                dev_addrs.add(ip)
            noderef = nic.attrib['nodeRefId']
            if noderef:
                links[dev_id].extend(noderef.split(';'))

        npv_nd = {u'rdfs:type': 'npv:'+dev_type,
                 u'd3:name': dev_name,
                 u'npv:id': dev_id,
                 u'd3:domain' : 'cyber',
                 u'enet:hasIPValues' : ', '.join(dev_addrs)
                 }            # Look for matching cptl node

        d3_dict['nodes'].append(npv_nd)

    # Extract networks, creating corresponding nodes
    # and preparing edges for each noderef
    for net in root.iter('Network'):
    #     print net.attrib
        net_id = unicode(net.attrib['id'], "utf-8")
        net_name = unicode(net.attrib['name'], "utf-8")
        net_type = unicode(net.attrib['network_type'], "utf-8")
        if 'nodeRefId' in net.attrib:
            noderef = unicode(net.attrib['nodeRefId'], "utf-8")
            if noderef:
                links[net_id].extend(noderef.split(';'))
        node_id_map[net_id] = i
        i += 1
        d3_dict['nodes'].append({u'rdfs:type': u'npv:net_' + net_type,
                                     u'd3:name': net_name,
                                     u'npv:id': net_id,
                                     u'd3:domain' : u'cyber'})

    # @TODO Parse tunnels

    # After all nodes have been parsed, go through all edges
    # and use index in nodes list as endpoints
    for link_src, link_dsts in links.iteritems():
        for link_dst in link_dsts:
            d3_dict['links'].append({u'source':node_id_map[link_src],
                                      u'target':node_id_map[link_dst],
                                      u'value':2})
    return d3_dict

def load_cptl_data(input_cptl_file):
    '''
    Parse cptl nodes (from D3 json format) and save into dict
    '''
    cptl_d3_dict = None
    with open(input_cptl_file) as f:
        cptl_d3_dict = json.load(f)
    return cptl_d3_dict

def set_d3_attrs (node, name, type, domain=None, id=''):
    '''
    Set d3 attributes for a given node, Will create a new node if None.
    '''
    if not node:
        node = {}
    if not domain:
        if '-network:' in name:
            domain = 'cyber'
        elif '-yard:' in name:
            domain = 'power'
        else:
            domain = 'n/a'

    node[u'd3:domain'] = domain 
    if id:
        node[u'npv:id'] = id
    node[u'd3:name'] = name
    node[u'rdfs:type'] = type
    return node

def merge_npv_cptl(npv_dict, cptl_dict):
    '''
    Allow addition of cptl data to an existing npv json dict.
    '''
    matched_cptl_nds = {} # 1x1 cptl node name -> final/combined npv_cptl node object
    cyber_nds = {} # 1x1 node ip -> node object
    power_nds = {} # 1x1 node ip -> node object
    node_id_map = {}  # 1x1 device name -unique in cptl data- to d3 node id (strxint)

    # Identify cptl nodes known by npv and update attributes
    for npv_nd in npv_dict['nodes']:
        try:
            dev_type = npv_nd[u'rdfs:type']
            if 'npv:net_' in dev_type:
                continue
            dev_name = npv_nd[u'd3:name']
            dev_ips = npv_nd[u'enet:hasIPValues']
            cptl_nd = None
            if cptl_dict:
                new_cptl_nd = matching_cptl_node(cptl_dict, (u'enet:hasIPValue', dev_ips.split(', ')))
                if cptl_nd and new_cptl_nd and dev_type not in ['firewall', 'router', 'switch']:
                    print 'WARNING: already have a cptl node for ' + dev_type + ' ' + dev_name + '\n' + str(cptl_nd)
                else:
                    cptl_nd = new_cptl_nd
            if cptl_nd:
                npv_nd.update(cptl_nd)
                matched_cptl_nds[cptl_nd[u'name']] = npv_nd
                del npv_nd['enet:hasIPValue']
        except Exception, e:
            traceback.print_exc()
            print 'ERROR: failed to match cptl to npv node ',str(npv_nd),'.',str(e)
            continue

    # Add new nodes (cyber or power) found only in cptl data
    for cptl_nd in cptl_dict['nodes']:
        if 'enet:hasIPValue' in cptl_nd.keys():
            cyber_nds[cptl_nd[u'enet:hasIPValue']] = cptl_nd
            # cptl cyber node not found in npv topo
            if cptl_nd[u'name'] not in matched_cptl_nds.keys():
                clone = copy.deepcopy(cptl_nd)
                npv_dict['nodes'].append(clone)
                set_d3_attrs(clone, cptl_nd[u'name'], cptl_nd[u'rdfs:type'])
                # @TODO Remove obsolete field enet:hasIPValue
                del clone['enet:hasIPValue']
        else:
            # cptl power node
            power_nds[cptl_nd[u'name']] = cptl_nd
            clone = copy.deepcopy(cptl_nd)
            npv_dict['nodes'].append(clone)
            set_d3_attrs(clone, cptl_nd[u'name'], cptl_nd[u'rdfs:type'])


    print 'cptl>',str(len(cyber_nds.keys())),'cyber nodes'
    print 'cptl>',str(len(power_nds.keys())),'power nodes'
    print 'npv>',str(len(npv_dict['nodes'])),' nodes incl.',str(len(matched_cptl_nds)),'matched cptl nodes'

    for i, nd in enumerate(npv_dict['nodes']):
        node_id_map[nd[u'd3:name']] = i
        if u'name' in nd.keys():
            node_id_map[nd[u'name']] = i

    # Remove unnecessary attributes
    for npv_nd in npv_dict['nodes']:
        if u'd3:name' not in npv_nd.keys():
            npv_nd[u'd3:name'] = npv_nd[u'name']
        if u'name' in npv_nd.keys():
            del npv_nd[u'name']

    # Add all cptl links
    missing = {'source':[], 'target':[]}
    for link in cptl_dict['links']:
        if link['source'] in node_id_map and\
        link['target'] in node_id_map:
            npv_dict['links'].append({u'source':node_id_map[link['source']],
                                      u'target':node_id_map[link['target']],
                                      u'value':2
                                      })
            continue

    # @DEBUG
#         if link['source'] not in node_id_map:
#             missing['source'].append(link['source'])
#         if link['target'] not in node_id_map:
#             missing['target'].append(link['source'])
# 
#     if missing['source'] or missing['target']:
#         print 'Missing sources and targets:'
#         pprint.pprint(missing.values())
# 
#     for x,y in enumerate(npv_dict['nodes']):
#         print x,y
#                  
#     for x,y in enumerate(npv_dict['links']):
#         if y['source'] > len(npv_dict['nodes']):
#             print 'Error source node',x,y,str(len(npv_dict['nodes']))
#         if y['target'] > len(npv_dict['nodes']):
#             print 'Error target node',x,y,str(len(npv_dict['nodes']))
#         print x,y 

def matching_cptl_node(cptld, attr_pair):
    '''
    Locate cptl node matching provided attribute pair
    '''
    for nd in cptld['nodes']:
        if attr_pair and attr_pair[0] in nd.keys():
            for addr in attr_pair[1]:
                if addr == nd[attr_pair[0]]:
#                     print 'Matched node',nd['name'],'/',addr
                    return nd
    
def main():
    '''
    Main entry point
    '''
    arg_parser = argparse.ArgumentParser(description='Combine NPV and CPTL nodes into JSON file for D3 display')
    arg_parser.add_argument('-project', metavar='<project name>', dest='project', help='project name', required=True)

    cmdline = sys.argv[1:] 
    args = arg_parser.parse_args(cmdline)

    project_name = args.project

    in_topo_file = os.path.join('..', 'static', 'projects', project_name, 'npv', 'topology.xml')
    in_cptl_file =  os.path.join('..', 'static', 'projects', project_name, 'substations.graph.json')
    out_d3_json = os.path.join('..', 'static', 'projects', project_name, 'npv_cptl_graph.json')

    # Load cptl nodes first
    cptl_d3_dict = load_cptl_data(in_cptl_file)
    # pprint.pprint(cptl_d3_dict)

    # Load npv nodes and edges making sure not to create 
    # duplicates of cptl nodes
    npv_d3_dict = load_npv_topo(in_topo_file, cptl_d3_dict)
    # pprint.pprint(npv_d3_dict)

    # Update nodes in npv dict with attributes found in cptl dict
    merge_npv_cptl(npv_d3_dict, cptl_d3_dict)

    # Write nodes and links to output json file
    with open(out_d3_json, 'w') as d3_json_file:
        json.dump(npv_d3_dict, d3_json_file, sort_keys=True, indent=4, separators=(',', ': '))

    print 'Successfully combined npv and cptl data to D3 json format saved into',out_d3_json

if __name__ == "__main__":
    main()
