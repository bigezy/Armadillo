/*
  copyright (c) 2015, Gabriel A. Weaver

  This file is part of the Cyber-Physical Topology Language for the
    Power domain.

  This code is free software:  you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by the
    Free Software Foundation, either version 3 of the License, or 
    (at your option) any later version.

  The Cyber-Physical Topology Language (CPTL):  Electrical Power 
    is distributed in the hope that it will be useful, but 
    WITHOUT ANY WARRANTY; without even the implied warranty of 
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    General Public License for more details.

  You should have received a copy of the GNU General Public License
    along with this program.  If not, see http://www.gnu.org/licenses/    
*/

//These should be annotations eventually
var domains_selector = "enet-hasDomainNameValue$=";

var substations_sizes = {"capital-city.8sub.cypsa.projects.cptl-c.org":20,
			 "cypress-creek.8sub.cypsa.projects.cptl-c.org":20,
			 "haverbrook.8sub.cypsa.projects.cptl-c.org":20,
			 "north-haverbrook.8sub.cypsa.projects.cptl-c.org":20,
			 "odgenville.8sub.cypsa.projects.cptl-c.org":20,
			 "paris.8sub.cypsa.projects.cptl-c.org":20,
			 "shelbyville.8sub.cypsa.projects.cptl-c.org":20,
                         "springfield.8sub.cypsa.projects.cptl-c.org":20};

var networks_sizes = {"network.capital-city.8sub.cypsa.projects.cptl-c.org":20,
                      "yard.capital-city.8sub.cypsa.projects.cptl-c.org":5,
                      "network.cypress-creek.8sub.cypsa.projects.cptl-c.org":20,
                      "yard.cypress-creek.8sub.cypsa.projects.cptl-c.org":5,
                      "network.haverbrook.8sub.cypsa.projects.cptl-c.org":20,
                      "yard.haverbrook.8sub.cypsa.projects.cptl-c.org":5,
                      "network.north-haverbrook.8sub.cypsa.projects.cptl-c.org":20,
                      "yard.north-haverbrook.8sub.cypsa.projects.cptl-c.org":5,
                      "network.odgenville.8sub.cypsa.projects.cptl-c.org":20,
                      "yard.odgenville.8sub.cypsa.projects.cptl-c.org":5,
                      "network.paris.8sub.cypsa.projects.cptl-c.org":20,
                      "yard.paris.8sub.cypsa.projects.cptl-c.org":5,
                      "network.shelbyville.8sub.cypsa.projects.cptl-c.org":20,
                      "yard.shelbyville.8sub.cypsa.projects.cptl-c.org":5,
                      "network.springfield.8sub.cypsa.projects.cptl-c.org":20,
                      "yard.springfield.8sub.cypsa.projects.cptl-c.org":5};

var yards_sizes = {"yard.capital-city.8sub.cypsa.projects.cptl-c.org":20,
                   "network.capital-city.8sub.cypsa.projects.cptl-c.org":5,
                   "yard.cypress-creek.8sub.cypsa.projects.cptl-c.org":20,
                   "network.cypress-creek.8sub.cypsa.projects.cptl-c.org":5,
                   "yard.haverbrook.8sub.cypsa.projects.cptl-c.org":20,
                   "network.haverbrook.8sub.cypsa.projects.cptl-c.org":5,
                   "yard.north-haverbrook.8sub.cypsa.projects.cptl-c.org":20,
                   "network.north-haverbrook.8sub.cypsa.projects.cptl-c.org":5,
                   "yard.odgenville.8sub.cypsa.projects.cptl-c.org":20,
                   "network.odgenville.8sub.cypsa.projects.cptl-c.org":5,
                   "yard.paris.8sub.cypsa.projects.cptl-c.org":20,
                   "network.paris.8sub.cypsa.projects.cptl-c.org":5,
                   "yard.shelbyville.8sub.cypsa.projects.cptl-c.org":20,
                   "network.shelbyville.8sub.cypsa.projects.cptl-c.org":5,
                   "yard.springfield.8sub.cypsa.projects.cptl-c.org":20,
                   "network.springfield.8sub.cypsa.projects.cptl-c.org":5};

function update_graph_sizes( dictionary, selector, document) {
    for (var key in dictionary) {
        var size = dictionary[key];
        var nodes = document.querySelectorAll("[" + selector + "'" + key + "'" + "]");
        for (var i=0; i < nodes.length; i++) {
            var node = nodes[i];			  
            node.setAttribute("r", size);
        }
    }
}

function annotateNode(annotations, node, source_property, target_property) {
    var source_value;
    var target_value = "";
    
    if (source_property in node) {
        source_value  = node[source_property];
    } 
    if (source_value in annotations) {
        target_value = annotations[source_value][0];
    }
    return target_value;
}

    // Load the Annotations Data
/*    var annotations = {};
    var source_property, target_property;
    
    d3.json("@ANNOTATIONS_DATA_PATH@", function(error, json) {
      if (error) throw error;

      annotations = json;
      source_property = annotations["source_property"];
      target_property = annotations["target_property"];
      target_property_attr = target_property.replace(/:/g, "-");
    });
*/
    //.attr(target_property_attr, function(node) {
    //     return annotateNode( annotations, node, source_property, target_property );
    //})
