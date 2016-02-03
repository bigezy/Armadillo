"""
  copyright (c) 2015, Gabriel A. Weaver, Information Trust Institute
    at the University of Illinois, Urbana-Champaign.
"""
import json
import simplejson
import sys

def visit_tree_nodes( node_dict ):

    # Fix the IP address and add the type
    if "path" in node_dict:
        octets = node_dict["path"].split(".")
        octets.reverse();
        ip_address = ".".join(octets);
        node_dict["path"] = ip_address;

        if len(octets) < 4:
            node_dict["rdfs:type"] = "enet:Network"
        elif len(octets) == 4:
            node_dict["rdfs:type"] = "enet:hasIPAddressValue"

    new_children = []
    if "children" in node_dict:
        for child in node_dict["children"]:
            new_child = visit_tree_nodes(child)
            new_children.append(new_child)

        node_dict["children"] = new_children
    return node_dict
            
def usage():
    print("append <input_tree_filepath> <output_tree_filepath>")

def main(argv):
    if len(argv) != 2:
        usage()
        sys.exit(-1)

    input_tree_filepath = argv[0]
    output_tree_filepath = argv[1]

    input_tree_file = open(input_tree_filepath, 'r')
    input_tree_data = simplejson.load(input_tree_file)
    input_tree_file.close()

    input_tree_data = visit_tree_nodes( input_tree_data )

    output_file = open(output_tree_filepath, "w")
    json.dump(input_tree_data, output_file, indent=4, sort_keys=True)
    output_file.close()

if __name__ == "__main__":
    main(sys.argv[1:])
