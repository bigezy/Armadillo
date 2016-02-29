/**
 *
 */
//var d3 = require('d3')
//var reqJs;
//reqJs = require('requirejs');
//reqJs.config({
//    //Pass the top-level main.js/index.js require
//    //function to requirejs so that node modules
//    //are loaded relative to the top-level JS file.
//    nodeRequire: require
//});

//var merge =
//merge = require(["gulp-merge-json"], function (src) {
//    //This function is called when scripts/helper/util.js is loaded.
//    //If util.js calls define(), then this function is not fired until
//    //util's dependencies have loaded, and the util argument will hold
//    //the module value for "helper/util".
//});
//var merge = require('gulp-merge-json');
//var jsoncombine = require("gulp-jsoncombine");


    /*
     *  Zoom  
     */	
	function zoomer() {
		svg.attr("transform",
			"translate(" + d3.event.translate + ")"
			+ " scale(" + d3.event.scale + ")");
	}
	
    /*
     *  Drag  
     */	
    function dragstarted(d) {
        d3.event.sourceEvent.stopPropagation();
        d3.select(this).classed("dragging", true);
		force.stop();
    }

    function dragged(d) {
        d3.select(this).attr("cx", d.x = d3.event.x).attr("cy", d.y = d3.event.y);
		d.px += d3.event.dx;
        d.py += d3.event.dy;
        d.x += d3.event.dx;
        d.y += d3.event.dy; 
		//tick();
    }

    function dragended(d) {
        d3.select(this).classed("dragging", false);
		d.fixed = true; // set the node to fixed so the force doesn't include the node in its auto positioning stuf
		force.resume();
		
		//tick();
    }
    function releasenode(d) {
        d.fixed = false; // set the node to fixed so the force doesn't include the node in its auto positioning stuff
        //force.resume();
    }
	
//Drag test
var node_drag = d3.behavior.drag()
	//.origin(function(d) { return d; })
	.on("dragstart", dragstarted)
	.on("drag", dragged)
	.on("dragend", dragended);

var width = 960, height = 500;
var color;
color = d3.scale.category20();

var force = d3.layout.force().charge(-120).linkDistance(30).size(
    [width, height]);

// Add canvas
var svg = d3.select("#topoContainer")
    .append("svg")
	//.attr("width", width)
	//.attr("height", height);
	.attr("viewBox", "0 0 " + width + " " + height )
	//Add zoom
	//.attr("pointer-events", "all")
	.call(d3.behavior.zoom().on("zoom", zoomer))
	.append('svg:g');
		
// Draw graph from json data
var drawGraph = function (graph) {
	  console.log(graph);
    d3.json(graph, function (error, graph) {
        if (error)
            throw error;

        force
            .nodes(graph.nodes)
            .links(graph.links).start();

        var link = svg.selectAll(".link")
            .data(graph.links).enter()
            .append("line")
            .attr("class", "link")
            .style("stroke-width", function (d) {
                return Math.sqrt(d.value);
            });

        var gnodes = svg.selectAll('g.gnode')
            .data(graph.nodes).enter()
            .append('g')
            .classed('gnode', true)
			.on('dblclick', releasenode)//added
			.call(node_drag); //added

        /*             var node = gnodes.append("circle")
         .attr("class", "node")
         .attr("r", 5)
         .style("fill", function(d) { return color(d.d3_type); })
         .call(force.drag); */

        // Associate icons to nodes
        gnodes.append("image").attr("xlink:href", function (d) {
            if (d['rdfs:type'].indexOf('firewall') != -1) {
                return "img/13_05_osa_icons_svg/osa_firewall.svg";
            } else if (d['rdfs:type'].indexOf('network') != -1) {
                return "img/13_05_osa_icons_svg/osa_cloud.svg";
            } else if (d['rdfs:type'].indexOf('host') != -1) {
                return "img/13_05_osa_icons_svg/osa_ics_plc.svg";
            } else {
              return "img/13_05_osa_icons_svg/osa_awareness.svg";            	
            }
        }).attr("x", -8).attr("y", -8).attr("width", 16).attr("height", 16);

        // Tooltip
        gnodes.append("title").text(function (d) {
            return d['rdfs:type'] + ' ' + d['d3:name'];
        });

        var labels = gnodes.append("text").attr("dx", 10).attr("dy", ".35em").attr(
            "class", "textClass").text(function (d) {
            return d['d3:name']
        }).style("stroke", "gray");

        console.log(labels);

        force.on("tick", function () {
            link.attr("x1", function (d) {
                return d.source.x;
            }).attr("y1", function (d) {
                return d.source.y;
            }).attr("x2", function (d) {
                return d.target.x;
            }).attr("y2", function (d) {
                return d.target.y;
            });

            gnodes.attr("transform", function (d) {
                return 'translate(' + [d.x, d.y] + ')';
            });
        });

        //Add node search feature
        var optArray = [];
        for (var i = 0; i < graph.nodes.length - 1; i++) {
            optArray.push(graph.nodes[i]['d3:name']);
        }
        optArray = optArray.sort();
        $(function () {
            $("#search").autocomplete({
                source: optArray
            });
        });
    })
};

//var fisheye = d3.fisheye.circular().radius(120);
//svg.on("mousemove", function() {
//	force.stop();
//	fisheye.focus(d3.mouse(this));
//	d3.selectAll(".node")
//		.each(function(d) {
//			d.fisheye = fisheye(d);
//		})
//		.attr("cx", function(d) {
//			return d.fisheye.x;
//		})
//		.attr("cy", function(d) {
//			return d.fisheye.y;
//		})
//		.attr("r", function(d) {
//			return d.fisheye.z * 8;
//		});
//	var link = svg.selectAll(".link")
//		.attr("x1", function(d) {
//			return d.source.fisheye.x;
//		})
//		.attr("y1", function(d) {
//			return d.source.fisheye.y;
//		})
//		.attr("x2", function(d) {
//			return d.target.fisheye.x;
//		})
//		.attr("y2", function(d) {
//			return d.target.fisheye.y;
//		});
//});

function searchNode() {
    //find the node
    var selectedVal = document.getElementById('search').value;
    var node = svg.selectAll(".node");
    if (selectedVal == "none") {
        node.style("stroke", "white").style("stroke-width", "1");
    } else {
        var selected = node.filter(function (d, i) {
            return d.d3_name != selectedVal;
        });
        selected.style("opacity", "0");
        var link = svg.selectAll(".link")
        link.style("opacity", "0");
        d3.selectAll(".node, .link").transition().duration(5000)
            .style("opacity", 1);
    }
}

function showFileBrowser() {
    var f = document.createElement("form");
    f.setAttribute('method',"post");
    f.setAttribute('enctype',"multipart/form-data");
    f.setAttribute('name',"jsonFile");
    f.setAttribute('id',"jsonFile");

    var i = document.createElement("input"); //input element, text
    i.setAttribute('type',"file");
    i.setAttribute('id',"fileinput");

    var s = document.createElement("input"); //input element, Submit button
    s.setAttribute('type',"submit");
    s.setAttribute('value',"Load");
    s.setAttribute('id',"btnLoad");
    s.setAttribute('onclick',"loadFile();");

    f.appendChild(i);
    f.appendChild(s);

    document.getElementById("file_browser_row").appendChild(f)
}

function hideTable() {
    document.getElementById("table_row").style.display = "none";
}

function combineJsonFiles(dir) {
    var result = obj2;
    obj2.prototype = obj1;
}

function loadFile() {
    var input, file, fr;

    if (typeof window.FileReader !== 'function') {
        alert("The file API isn't supported on this browser yet.");
        return;
    }

    input = document.getElementById('fileinput');
    if (!input) {
        alert("Um, couldn't find the fileinput element.");
    }
    else if (!input.files) {
        alert("This browser doesn't seem to support the `files` property of file inputs.");
    }
    else if (!input.files[0]) {
        alert("Please select a file before clicking 'Load'");
    }
    else {
        file = input.files[0];
        fr = new FileReader();
        fr.onload = receivedText;
        fr.readAsText(file);
    }

    function receivedText(e) {
        lines = e.target.result;
        var newArr = JSON.parse(lines);
    }
}

function fillTable(jsonFile) {
    $("#jqGrid").jqGrid({
        url: jsonFile,
        mtype: "GET",
        datatype: "json",
        colModel: [{
            label: 'ID',
            name: 'LocationID',
            key: true,
            width: 75
        }, {
            label: 'Location Name',
            name: 'LocationName',
            width: 150
        }, {
            label: 'Physical Status',
            name: 'PhysicalStatus',
            width: 150
        }, {
            label: 'Cyber Status',
            name: 'CyberStatus',
            width: 150
        }, {
            label: 'Rank',
            name: 'Rank',
            width: 150
        }],
        loadonce: true,
        width: 780,
        height: 250,
        rowNum: 10,
        subGrid: true, // set the subGrid property to true to show expand buttons for each row
        subGridRowExpanded: showChildGrid, // javascript function that will take care of showing the child grid
        subGridOptions: {
            // load the subgrid data only once
            // and the just show/hide
            reloadOnExpand: false,
            // select the row when the expand column is clicked
            selectOnExpand: true
        },
        pager: "#jqGridPager"
    });
};

// the event handler on expanding parent row receives two parameters
// the ID of the grid tow  and the primary key of the row
function showChildGrid(parentRowID, parentRowKey) {
    var childGridID = parentRowID + "_table";
    var childGridPagerID = parentRowID + "_pager";

    // send the parent row primary key to the server so that we know which grid to show
    var childGridURL = "projects/8bus/" + parentRowKey + ".json";
    //childGridURL = childGridURL + "&parentRowID=" + encodeURIComponent(parentRowKey)

    // add a table and pager HTML elements to the parent grid row - we will render the child grid here
    $('#' + parentRowID).append(
        '<table id=' + childGridID + '></table><div id=' + childGridPagerID
        + ' class=scroll></div>');

    $("#" + childGridID).jqGrid({
        url: childGridURL,
        mtype: "GET",
        datatype: "json",
        page: 1,
        colModel: [{
            label: 'Node ID',
            name: 'NodeID',
            key: true,
            width: 75
        }, {
            label: 'Name',
            name: 'Name',
            width: 100
        }, {
            label: 'Type',
            name: 'NodeType',
            width: 100
        }, {
            label: 'Address',
            name: 'NodeAddress',
            width: 100
        }, {
            label: 'Services',
            name: 'NodeServices',
            width: 75
        }],
        loadonce: true,
        width: 500,
        height: '100%',
        pager: "#" + childGridPagerID
    });

}