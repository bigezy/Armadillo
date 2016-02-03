"""
  copyright (c) 2015, Gabriel A. Weaver, Information Trust Institute
    at the University of Illinois, Urbana-Champaign.
"""
import json
import simplejson
import sys

def expand_namespace(namespaces_data, qualified_domain_name):
    pieces = qualified_domain_name.split(":")
    namespace = pieces[0]
    name = pieces[1]

    uri = namespaces_data[ namespace ]
    return name + "." + uri
    
def usage():
    print("convert <input_graph_filepath> <reference_attribute_name> <output_graph_filepath>")
    
def main(argv):
    if len(argv) != 3:
        usage()
        sys.exit(-1)

    input_graph_filepath = argv[0]
    reference_attribute_name = argv[1]
    output_graph_filepath = argv[2]

    input_graph_file = open(input_graph_filepath, 'r')
    input_graph_data = simplejson.load(input_graph_file)
    input_graph_file.close()

    nodes = input_graph_data["nodes"]
    links = input_graph_data["links"]

    old_to_new = {}
    
    for node in nodes:
        old_node_name = node["name"]
        if reference_attribute_name in node:
            new_node_name = node[reference_attribute_name]
        else:
            new_node_name = old_node_name
            
        old_to_new[ old_node_name ] = new_node_name
        node["name"] = new_node_name
        
    for link in links:
        old_source_str = link["source"]
        old_target_str = link["target"]

        link["source"] = old_to_new[ old_source_str ]
        link["target"] = old_to_new[ old_target_str ]

    output_file = open(output_graph_filepath, "w")
    json.dump(input_graph_data, output_file, indent=4, sort_keys=True)
    output_file.close()
    
if __name__ == "__main__":
    main(sys.argv[1:])
    
