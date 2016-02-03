<?php  
session_start();
	

?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"   "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en-us">
<head>
	<title>CyPSA</title>
	<link rel="stylesheet" href="index.css" type="text/css" media="print, projection, screen" />
	<link rel="stylesheet" href="css/jq.css" type="text/css" media="print, projection, screen" />
	<link rel="stylesheet" href="themes/blue/style.css" type="text/css" media="print, projection, screen" />
	<script type="text/javascript" src="js/changeField.js"></script>
	<script type="text/javascript" src="jquery-latest.js"></script>
	<script type="text/javascript" src="__jquery.tablesorter.min.js"></script>
	<script type="text/javascript" src="js/chili/chili-1.8b.js"></script>
	<script type="text/javascript" src="js/docs.js"></script>
	<script type="text/javascript">
	$(function() {
			$("#mytable1").tablesorter({sortList:[[0,0],[2,1]], widgets: ['zebra']});
			$("#mytable2").tablesorter({sortList:[[1,1],[1,1]], widgets: ['zebra']});
			$("#mytable3").tablesorter({sortList:[[1,1],[2,1]], widgets: ['zebra']});
			$("#mytable4").tablesorter({sortList:[[1,1],[2,1]], widgets: ['zebra']});
			//$('#cyber').show();
					     $('#physical').hide(); 
						 $('#paths').hide();
			
	});
	
	function ChangeColor(the_element) {
	
	
	if(the_element.checked ) {
		the_element.parentNode.parentNode.style.backgroundColor = '#FA5858';
	} else {
		the_element.parentNode.parentNode.style.backgroundColor = '#A9F5BC';
	}
}
	function ChangeColor1(the_element) {
		
		if(the_element.checked ) {
			the_element.parentNode.parentNode.style.backgroundColor = '#A9F5BC';
		} else {
			the_element.parentNode.parentNode.style.backgroundColor = '#FA5858';
		}
	}
	function getFolder()
	{
		document.fileform.folder.value=document.fileform.fileURL.files[0].name;
	}


	</script>
</head>
<body onload="base()">
	<div id="banner">
		<h1><em>Cy</em>PSA</h1>
		<a href="#"></a>
		</div>
		<?php 
		if(isset($_SESSION['project']))
		{	$folder=$_SESSION['project'];
			$pname=explode("\\",$folder);
			//echo $pname[count($pname)-2];
			echo "<center> Project -".$pname[count($pname)-2]."</center>";
			
		}
		
		
?>

		<div id="modal">
		<div class="modal-content">
			<div class="header">
				<h2>CyPSA Project</h2>
			</div>
			<div style="align:center;" class="copy">
				<form action="setProject.php"  method="post">
				<table style="align:center;">
				<tr><td>Project Link</td><td>:</td><td><input name="project" style="width: 350px;" type="text" placeholder="Folder Link goes here"></input></td></tr>
				<tr><td colspan="3"><center><input type="Submit" value="Select"/></center></td></tr>
				</table>
				</form>
			</div>
			<div class="cf footer">
				<a href="#" class="btn">Close</a>
			</div>
		</div>
		<div class="overlay"></div>
	</div>
<p align="right"><a href="#modal" style="width:150px;" class="btn btn-primary btn-large btn-block btn-caps go">Select Project</a></p>
	

	<div id="main">
	<?php if(isset($folder))
	{
		$afilename=$folder."/pw_analysis_attack_graph_current.xml";
		
		//echo $afilename;
		if(file_exists($afilename))
		{
		?>
		<BR>
  		<table align="center" style="width:940px; " border="0" cellpadding="0" cellspacing="1">
   			<tr>
				<td> <b>CyPSA  &nbsp;   &nbsp;  &nbsp;    </b><select><option><?php echo $pname[count($pname)-2];?></option></select></td>
   			</tr>
   			<tr>
				<td colspan="5"><hr/></td>
			</tr>
   			<tr>
				<td>
					<table style="width:940px;">
						<tr>
							<td colspan="2" width="440px;"><h3><p>Current Analysis</p></h3></td>
							<td width="20px;">&nbsp; &nbsp; &nbsp; </td>
							<td colspan="*" width="440px;"><h3><p>Objective Function</p></h3></td>
						</tr>
						<tr>
							<td colspan="2" width="440px;">
							  <select id="filenamev">
								<?php 
									//error_reporting(E_ERROR);
									//error_reporting(E_ALL&~E_Notice);
									header('Content-type:text/html; charset=utf-8');
									$xmlfiles = glob($folder.'/*.{xml}', GLOB_BRACE);
									$loadfile=$_GET['loadfile'];
									if($_GET['loadfile']!="")
									{	
										$loadfile=$_GET['loadfile'];
										foreach($xmlfiles as $value)
										{	
											$loadfile=$value;
										}
										$loadfile=$folder;
										echo "<option value='".$loadfile."' ";
										echo "selected='selected'";
										echo ">".basename($loadfile)."</option>";
											
									}
									else
									{
										foreach($xmlfiles as $value)
										{
											$loadfile=$value;
										}
										$loadfile=$afilename;
										$_SESSION['mtime']=filemtime ($afilename);
										echo "<option value='".$loadfile."' ";
										echo "selected='selected'";
										echo ">".basename($loadfile)." </option>";

									}
								?>
							  </select> 
							  &nbsp; &nbsp;  
							  <a   class="btn" onclick='javascript:load_file();'>Load</a> &nbsp; &nbsp;<a href="#" class="btn">Edit</a>
						  </td>
						  <td width="20px;">
								&nbsp; &nbsp; &nbsp; 
						 </td>
						 <td colspan="2" width="440px;">
							<select>
								<option>Cyber Exposure + Physical Impact</option>
							</select>
							
						</td>
				
					</tr>
					<tr>
					<td>
					<input id="entryHost" type="text" style="width:249px" />
					&nbsp;&nbsp; &nbsp;<a href="#" class="btn" onclick="javascript:runAnalysis(document.getElementById('entryHost').value);">Run</a>
					</td>
					</tr>
					
					<tr>
						<td colspan="5"><hr/></td>
					</tr>
					<tr>
						<td colspan="2" width="540px;"><b>Ranked Assets &nbsp; &nbsp; &nbsp; </b>&nbsp; </td>
						<td width="20px;">&nbsp; &nbsp; </td>
						<td colspan="2" width="440px;"><b>Topologies and Paths</b></td>
					</tr>		
					<tr>
						<td colspan="2" valign="top" width="440px;">
							<?php
							include ('rankedassets.php');
									
						
							?>	
					</td>
					<td width="20px;">&nbsp; &nbsp; &nbsp; </td>
					<td colspan="2" height="350px;" valign="top" width="440px;"><a href="javascript:void(0);" id="toggle-div">View Cyber</a> &nbsp; | &nbsp; <a href="javascript:void(0);" id="toggle-div1">View Physical</a> &nbsp; | &nbsp; <a href="javascript:void(0);" id="toggle-div2">View Paths</a>
					<div id="cyber"><br/><img height="350px;" width="440px" src="images/cyber.jpg"></img> </div>
					<div id="physical" style="display:none;"><br/><img height="350px;" width="440px;" src="images/physical.jpg"></img></div>
					<div id="paths" style="display:none;"><br/><h1>No Host Selected: Click on host on left side table to see paths</h1></div>
					</td>
				</tr>
			</table>
				<script type="text/javascript">
					$(function(){
					  	 $('#toggle-div').click(function(){
					     $('#cyber').show();
					     $('#physical').hide(); 
						 $('#paths').hide();
					  });
					});
					$(function(){
					  $('#toggle-div1').click(function(){
					     $('#cyber').hide();
					     $('#physical').show(); 
						 $('#paths').hide();
					  });
					});
					$(function(){
					  $('#toggle-div2').click(function(){
					     $('#cyber').hide();
					     $('#physical').hide(); 
						 $('#paths').show();
					  });
					});

				</script>	
							
		</td>
	</tr>
  	<tr>
  		<td><br><br><br><a href="javascript:void(0);" id="toggle-div3"> Patch Hosts </a> &nbsp; | &nbsp; <a href="javascript:void(0);" id="toggle-div4">Compromised Hosts</a> &nbsp; | &nbsp; <a href="javascript:void(0);" id="toggle-div5">Vulnerability Patch</a>
  			<?php include('hoststable.php');
				
  			?>
			
<script type="text/javascript">
					function base()
					{
						$('#compromised').hide(); 
						 $('#vulnerability').hide();
					}
					$(function(){
					  	 $('#toggle-div3').click(function(){
					     $('#patch').show();
					     $('#compromised').hide(); 
						 $('#vulnerability').hide();
					  });
					});
					$(function(){
					  $('#toggle-div4').click(function(){
					     $('#patch').hide();
					     $('#compromised').show(); 
						 $('#vulnerability').hide();
					  });
					});
					$(function(){
					  $('#toggle-div5').click(function(){
					     $('#patch').hide();
					     $('#compromised').hide(); 
						 $('#vulnerability').show();
					  });
					});

				</script>	
				<?php 
				
				?>
  		</td>
  	</tr>
 </table>
<?php 
		}
		else 
		{
			echo "Analysis File doesnot exist";
		}
}
else 
	echo "Select a Project to continue"; ?>
</div>

</body>
</html>
