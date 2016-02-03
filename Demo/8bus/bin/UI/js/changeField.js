
function SelectProject()
{
	var project = $("#selectProject").val();
	window.location = "test4.php?project="+project;
}

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
function runAnalysis(entryHost)
{
	$.ajax({
		type: "GET",
		url: "js/command.php?entryHost="+entryHost,
		dataType: "xml",
		success: function(xml) {
		            console.log(xml);		            
				}
});
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
			            var pathtablebody="<table>";
			            $("#cyber").empty();
			            $("#physical").empty();
						$("#paths").empty();
			            //$("#pathtable").append("<tr><table class='paths'>");
			            $(xml).find('path').each(function(){
			            	pathtablebody+="<tr border='1'><td valign='top'><br/><b>Path : "+i+++"</b></td><td width='200px' valign='top'><br/><b>Security Index : "+$(this).find('securityIndex').text()+"<br>Performance Index : "+$(this).find('performanceIndex').text()+"<br>Cyber Cost : "+$(this).find('cyberCost').text()+"</b></td></tr>";
			            	
			            	//pathtablebody+="<tr border='1'><td ><br/><b>Path : "+i+++"</b></td><td width='175px'><br/><b>Security Index : "+$(this).find('securityIndex').text()+"</b></td></tr>";
			            	//pathtablebody+="<tr border='1'><td ><br/><b>Performance Index : "+$(this).find('performanceIndex').text()+"</b></td><td width='175px'><br/><b>Cost : "+$(this).find('cyberCost').text()+"</b></td></tr>";
			            	// $("#pathtable").append("<tr><td><br/><b>Path : "+i+++"</b></td><td width='175px'><br/><b>Security Index : "+$(this).find('securityIndex').text()+"</b></td></tr>");
			            $(this).find('node').each(function(){
			            	pathtablebody+="<tr><td width='150px'>"+$(this).find('ip').text()+"</td></tr>";
			            	//<td>"+$(this).find('nodeName').text()+"</td>
			            	//$("#pathtable").append("<tr><td width='250px'>"+$(this).find('nodeName').text()+"</td><td>"+$(this).find('ip').text()+"</td></tr>");
			            });
			             
			            // $("#pathtable").append("");
			            });
			            pathtablebody+="</table>";
			            $("#cyber").append(cyber);
			            $("#physical").append(physical);
						$("#paths").append(pathtablebody);
						//var construct=text();
						//alert(construct);
						//$("#path").empty();
						//$("#path").append("<table><tr><td style='width:450px;'><b>Paths containing asset "+assetid+" and ipaddress : "+ip+" will be displayed here</b></td></tr></table>");
						
						
					}
	});
	
}
