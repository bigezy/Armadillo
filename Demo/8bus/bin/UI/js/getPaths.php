<?php 
header('Content-type: application/xml');
$assetid=(string)$_GET['assetid'];
session_start();
//echo $assetid;
$xmlfile="../".$_SESSION['project']."/pw_analysis_attack_graph_current.xml";//(string)$_GET['xmlfile'];
$xml=simplexml_load_file($xmlfile) or die("Error: Cannot create object"); //../CYPSA-8-Bus/xml-output/pw_analysis_attack_graph
$k=0;
$flag=0;
$flag1=0;
echo "<sample>";
foreach($xml->children() as $nmap)
{	
	
	foreach($nmap->children() as $path)
	{		$path1=$path;
			$flag=0;
			$securityIndex= (float)$path['securityIndex'];
			$performanceIndex=(float)$path['performanceIndex'];
			$cyberCost=(float)$path['cyberCost'];
			if($securityIndex>0.0)
			{
				foreach($path->children() as $node)
			{
				if($assetid==(string)$node['IPAddress'])
				{	$flag=1;
					$flag1=1;
					break;
				}			
			
			}
			if($flag==1)
			{	
				echo "<path><securityIndex>".$securityIndex."</securityIndex>";
				echo "<performanceIndex>".$performanceIndex."</performanceIndex>";
				echo "<cyberCost>".$cyberCost."</cyberCost>";
				foreach($path1->children() as $node)
				{
				
				
					echo "<node><nodeName>".(string)$node['nodeName']."</nodeName><ip>".(string)$node['IPAddress']."</ip></node>";
			
			
				}
				echo "</path>";
			}
			}
			
	}
	
}
if($flag1==0)
	echo "<path><node><nodeName>Deleted</nodeName><ip>NA</ip></node></path>";
	
	
	echo "</sample>";
	
?>
