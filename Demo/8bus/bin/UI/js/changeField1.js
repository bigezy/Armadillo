function change(e, linkedObject, color){
	if(color == undefined){
		color = '#BBBBBB'
	}
	
	e.style.backgroundColor=color  
	e.style.cursor='hand'; 
	
	//alert(linkedObjectId);
	
	if(linkedObject != undefined){
		change(linkedObject)
	}
	
	
}

function changeback(e, linkedObject, color){
	if(color == undefined){
		e.style.backgroundColor=''; 
		
		if(linkedObject != undefined){
			changeback(linkedObject)
		}
	}else{
		e.style.backgroundColor=color;
		
		if(linkedObject != undefined){
			changeback(linkedObject, color)
		}	
	}
	
	
}

function load_file()
{
	var e = document.getElementById("filenamev");
	window.location.assign("../web_ui/index.php?loadfile="+e.options[e.selectedIndex].value);

}


function showAsset(asset)
{
	$.ajax({
			type: "GET",
			url: "js/getPaths.php?assetid="+asset,
			dataType: "xml",
			success: function(xml) {
			            console.log(xml);
			            var cyber="<img src='images/cyber.jpg' height='350px;' width='440px;'/>";
			            var physical="<img src='images/physical.jpg' height='350px;' width='440px;'/>";
			             var i=1;
						 // Create a new directed graph
var g = new dagreD3.graphlib.Graph({compound:true})
  .setGraph({})
  .setDefaultEdgeLabel(function() { return {}; });

var employees = {
    "nodes":
    [
	{"name":"OgN:SEL_3620",
	 "rdfstype":"snet:Switch"},

	{"name":"OgN:SEL_421_1",
	 "rdfstype":"snet:DistanceRelay"},

	{"name":"OgN:SEL_421_2",
	 "rdfstype":"snet:DistanceRelay"},

	{"name":"OgN:SEL_451_1",
	 "rdfstype":"snet:OvercurrentRelay"},

	{"name":"OgN:SEL_451_2",
	 "rdfstype":"snet:OvercurrentRelay"},

	{"name":"OgN:SEL_451_3",
	 "rdfstype":"snet:OvercurrentRelay"},

	{"name":"CCN:SEL_421_6",
	 "rdfstype":"snet:DistanceRelay"},

	{"name":"NHN:DistanceRelay_1",
	 "rdfstype":"snet:DistanceRelay"}
	
    ],
    
    "links":
    [
	{"source":"OgN:SEL_3620",
	 "target":"OgN:SEL_421_1",
	 "relation":"cptlc:hasLink" },

	{"source":"OgN:SEL_3620",
	 "target":"OgN:SEL_421_2",
	 "relation":"cptlc:hasLink" },

	{"source":"OgN:SEL_3620",
	 "target":"OgN:SEL_451_1",
	 "relation":"cptlc:hasLink" },

	{"source":"OgN:SEL_3620",
	 "target":"OgN:SEL_451_2",
	 "relation":"cptlc:hasLink" },

	{"source":"OgN:SEL_3620",
	 "target":"OgN:SEL_451_3",
	 "relation":"cptlc:hasLink" },
	
	{"source":"OgN:SEL_421_1",
	 "target":"CCN:SEL_421_6",
	 "relation":"cptlc:hasLink" },

	{"source":"OgN:SEL_421_2",
	 "target":"NHN:DistanceRelay_1",
	 "relation":"cptlc:hasLink" }
    ]
} ;
var states={};
for ( var i = 0; i < employees.nodes.length; i++) {
if(employees.nodes[i].name=='OgN:SEL_3620')
states[employees.nodes[i].name]={ description : ""+employees.nodes[i].rdfstype , 
 style: "fill: #f77" };
else if(i==employees.nodes.length-1)
states[employees.nodes[i].name]={ description : ""+employees.nodes[i].rdfstype , 
 style: "fill: #7f7" };
 else
states[employees.nodes[i].name]={ description : ""+employees.nodes[i].rdfstype};
}
Object.keys(states).forEach(function(state) {
  var value = states[state];
  value.label = state;
  value.rx = value.ry = 5;
  g.setNode(state, value);
});
g.setNode('group', {label: 'Group', clusterLabelPos: 'top', style: 'fill: #d3d7e8'});
g.setNode('top_group', {label: 'Top Group', clusterLabelPos: 'bottom', style: 'fill: #ffd47f'});
g.setNode('middle_group', {label: 'Middle Group', style: 'fill: #5f55'});
g.setNode('bottom_group', {label: 'Bottom Group', style: 'fill: #5f9488'});
g.setParent('top_group', 'group');
g.setParent('middle_group', 'group');
g.setParent('bottom_group', 'group');
g.setParent('OgN:SEL_3620', 'top_group');
g.setParent('OgN:SEL_421_1', 'bottom_group');
g.setParent('OgN:SEL_421_2', 'bottom_group');
g.setParent('OgN:SEL_451_1', 'bottom_group');
g.setParent('OgN:SEL_451_2', 'bottom_group');
g.setParent('OgN:SEL_451_3', 'middle_group');
g.setParent('CCN:SEL_421_6', 'middle_group');
g.setParent('NHN:DistanceRelay_1', 'middle_group');

for ( var i = 0; i < employees.links.length; i++) {
g.setEdge(employees.links[i].source,employees.links[i].target, { label : ""+employees.links[i].relation});
//alert(employees.links[i].source)
}
var render = new dagreD3.render();
var svg = d3.select("svg"),
    inner = svg.append("g");
var zoom = d3.behavior.zoom().on("zoom", function() {
    inner.attr("transform", "translate(" + d3.event.translate + ")" +
                                "scale(" + d3.event.scale + ")");
  });
svg.call(zoom);
var styleTooltip = function(name, description) {
  return "<p class='name'>" + name + "</p><p class='description'>" + description + "</p>";
};
render(inner, g);
inner.selectAll("g.node")
  .attr("title", function(v) { return styleTooltip(v, g.node(v).description) })
  .each(function(v) { $(this).tipsy({ gravity: "w", opacity: 1, html: true }); });
  
  var initialScale = 0.75;
  
  zoom
  .translate([(svg.attr("width") - g.graph().width * initialScale) / 2, 20])
  .scale(initialScale)
  .event(svg);
  svg.attr('height', g.graph().height * initialScale + 40);
			            var pathtablebody="<table>";
			            $("#cyber").empty();
			            $("#physical").empty();
						$("#paths").empty();
			            //$("#pathtable").append("<tr><table class='paths'>");
			            $(xml).find('path').each(function(){
			            	pathtablebody+="<tr border='1'><td ><br/><b>Path : "+i+++"</b></td><td width='175px'><br/><b>Security Index : "+$(this).find('securityIndex').text()+"</b></td></tr>";
			            	// $("#pathtable").append("<tr><td><br/><b>Path : "+i+++"</b></td><td width='175px'><br/><b>Security Index : "+$(this).find('securityIndex').text()+"</b></td></tr>");
			            $(this).find('node').each(function(){
			            	pathtablebody+="<tr><td width='150px'>"+$(this).find('nodeName').text()+"</td><td>"+$(this).find('ip').text()+"</td></tr>";
			            	//$("#pathtable").append("<tr><td width='250px'>"+$(this).find('nodeName').text()+"</td><td>"+$(this).find('ip').text()+"</td></tr>");
			            });
			             
			            // $("#pathtable").append("");
			            });
			            pathtablebody+="</table>";
			            $("#cyber").append(cyber);
			            $("#physical").append(physical);
						$("#paths").append(pathtablebody);
						$("#paths").append("<svg width=430 height=740></svg>");
						//var construct=text();
						//alert(construct);
						//$("#path").empty();
						//$("#path").append("<table><tr><td style='width:450px;'><b>Paths containing asset "+assetid+" and ipaddress : "+ip+" will be displayed here</b></td></tr></table>");
						
						
					}
	});
	
}
