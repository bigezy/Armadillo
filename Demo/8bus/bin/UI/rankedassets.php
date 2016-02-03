<?php
//cmd 11/22/15 - broke into seperate file to make things more readable
ini_set('auto_detect_line_endings', true);
	$uassets = array();
	$cve=array();
	$vul;
	$xmlfile=$loadfile;
		
	//echo $xmlfile;
	$xml1=simplexml_load_file($xmlfile) or die("Error: Cannot create object"); //../../CYPSA-8-Bus/xml-output/pw_analysis_attack_graph
	foreach($xml1->children() as $nmap)
	{
		foreach($nmap->Path as $path)
		{
			$securityIndex= (float)$path['securityIndex'];
			$performanceIndex= (float)$path['performanceIndex'];
			$cyberCost= (float)$path['cyberCost'];
			//I don't know what this code is supposed to be doing, but I'm not sure it makes any sense ***debug***	
			if($securityIndex>0.0)
			{
				$zk=0;
				foreach($path->Node as $node)
				{
					if($zk==0)
					{
						$zk++;
						$ID=(string)$node['nodeName'];
						$IP=(string)$node['IPAddress'];
						$criticalID=$ID;
						$criticalIP=$IP;
						if(isset($uassets)&&is_array($uassets)&&array_key_exists($criticalID,$uassets))
						{
							$uassets[$criticalID][0][1]=$uassets[$criticalID][0][1]+$securityIndex;
							$uassets[$criticalID][0][4]=$uassets[$criticalID][0][4]+1;
							$uassets[$criticalID][0][5][$nodevul]=1;
							
								$uassets[$criticalID][0][2]=$performanceIndex;
								$uassets[$criticalID][0][3]=$uassets[$criticalID][0][3]+$cyberCost;
								$uassets[$criticalID][0][6]="Source";
						}
						else if(isset($criticalID)&&isset($vul))
						{
							$uassets[$criticalID][0][1]=$securityIndex;
							$uassets[$criticalID][0][0]=$criticalIP;
							$uassets[$criticalID][0][4]=1;
							if(isset($nodevul))$uassets[$criticalID][0][5][$nodevul]=1;
							$uassets[$criticalID][0][2]=$performanceIndex;
							$uassets[$criticalID][0][3]=$cyberCost;
							$uassets[$criticalID][1][1]=0;
							$uassets[$criticalID][0][0]=$criticalIP;
							$uassets[$criticalID][1][4]=0;
							if(isset($nodevul))$uassets[$criticalID][1][5][$nodevul]=0;
							$uassets[$criticalID][1][2]=0;
							$uassets[$criticalID][1][3]=0;
						}
					}
					
							//array_push($cve[(string)$node['vulnID']][0],1);
							$vul=(string)$node['vulnID'];
						
						if(isset($ID)&&($ID==""))
						{
							$ID=(string)$node['nodeName'];
							$IP=(string)$node['IPAddress'];
			
						}
		
						//$criticalID=$ID;
						//$criticalIP=$IP;
						$ID=(string)$node['nodeName'];
						$IP=(string)$node['IPAddress'];
						$criticalID=$ID;
						$criticalIP=$IP;
						$nodevul = (string)$node['vulnID'];
						//echo "hello";
				}
					if(isset($uassets)&&is_array($uassets)&&array_key_exists($criticalID,$uassets))
					{
							if(!isset($cve))
							{
								$cve="";
							}
							if((!array_key_exists($vul,$cve)))
								$cve[$vul]="";
						if(!isset($cve[$vul][0]))
						{	$cve[$vul][0]=1;
						}	
						else
						{
							$cve[$vul][0]=$cve[$vul][0]+1;
							//echo "alert('Hi');";
							//array_push($cve[(string)$node['vulnID']][0],1);
							
						}
							$uassets[$criticalID][0][1]=$uassets[$criticalID][0][1]+$securityIndex;
							$uassets[$criticalID][0][4]=$uassets[$criticalID][0][4]+1;
							$uassets[$criticalID][0][5][$nodevul]=1;
							if(!isset($cve[$vul][1]))
								$cve[$vul][1]="";
							if(!isset($cve[$vul][1][$criticalID]))
								$cve[$vul][1][$criticalID]=1;
							else 
								$cve[$vul][1][$criticalID]=$cve[$vul][1][$criticalID]+1;
							

								$uassets[$criticalID][0][2]=$performanceIndex;
								$uassets[$criticalID][0][3]=$uassets[$criticalID][0][3]+$cyberCost;
								$uassets[$criticalID][0][6]="Target";
					}
					else if(isset($criticalID)&&isset($vul))
					{
						if(!isset($cve))
							{
								$cve="";
							}
					if((!array_key_exists($vul,$cve)))
								$cve[$vul]="";
						if(!isset($cve[$vul][0]))
						{	$cve[$vul][0]=1;
						}	
						else
						{
							$cve[$vul][0]=$cve[$vul][0]+1;
							//echo "alert('Hi');";
							//array_push($cve[(string)$node['vulnID']][0],1);
							
						}
						if(!isset($cve[$vul][1]))
								$cve[$vul][1]="";
							if(!isset($cve[$vul][1][$criticalID]))
								$cve[$vul][1][$criticalID]=1;
							else 
								$cve[$vul][1][$criticalID]=$cve[$vul][1][$criticalID]+1;
						$uassets[$criticalID][0][1]=$securityIndex;
						$uassets[$criticalID][0][0]=$criticalIP;
						$uassets[$criticalID][0][4]=1;
						$uassets[$criticalID][0][5][$nodevul]=1;
						$uassets[$criticalID][0][2]=$performanceIndex;
						$uassets[$criticalID][0][3]=$cyberCost;
						$uassets[$criticalID][1][1]=0;
						$uassets[$criticalID][0][0]=$criticalIP;
						$uassets[$criticalID][1][4]=0;
						$uassets[$criticalID][1][5][$nodevul]=0;
						$uassets[$criticalID][1][2]=0;
						$uassets[$criticalID][1][3]=0;
					}
				}
			}
		}
		//$uassets;
		//$cve;
		//$xmlfile=$folder."\pw_analysis_attack_graph_old.xml";
		$xmlfile=$folder."\pw_analysis_attack_graph_previous.xml";
		if(!file_exists($xmlfile))
		$xmlfile=$afilename;
		//echo $xmlfile;
		$xml1=simplexml_load_file($xmlfile) or die("Error: Cannot create object"); //../../CYPSA-8-Bus/xml-output/pw_analysis_attack_graph
		foreach($xml1->children() as $nmap)
		{
			foreach($nmap->children() as $path)
			{
				$securityIndex= (float)$path['securityIndex'];
				$performanceIndex= (float)$path['performanceIndex'];
				$cyberCost= (float)$path['cyberCost'];
				if($securityIndex>0.0)
				{
					$zk=0;
						
					foreach($path->children() as $node)
					{
						if($zk==0)
						{
							$zk++;
							$ID=(string)$node['nodeName'];
							$IP=(string)$node['IPAddress'];
							$criticalID=$ID;
							$criticalIP=$IP;
							$nodevul = (string)$node['vulnID'];
							if(array_key_exists($criticalID,$uassets))
							{
								$uassets[$criticalID][1][1]=$uassets[$criticalID][1][1]+$securityIndex;
								$uassets[$criticalID][1][4]=$uassets[$criticalID][1][4]+1;
								$uassets[$criticalID][1][5][$nodevul]=1;
								/*if(!$cve[$vul][1][$criticalID])
									$cve[$vul][1][$criticalID]=1;
								else
									$cve[$vul][1][$criticalID]=$cve[$vul][1][$criticalID]+1;
								*/
								$uassets[$criticalID][1][2]=$performanceIndex;
								$uassets[$criticalID][1][3]=$uassets[$criticalID][1][3]+$cyberCost;
								$uassets[$criticalID][0][6]="Source";
							}
							else
							{
								//$cve[$vul][1][$criticalID]=$cve[$vul][1][$criticalID]+1;
								$uassets[$criticalID][1][1]=$securityIndex;
								$uassets[$criticalID][0][0]=$criticalIP;
								$uassets[$criticalID][1][4]=1;
								$uassets[$criticalID][1][5][$nodevul]=1;
								$uassets[$criticalID][1][2]=$performanceIndex;
								$uassets[$criticalID][1][3]=$cyberCost;
								$uassets[$criticalID][0][1]=0;
								$uassets[$criticalID][0][2]=0;
								$uassets[$criticalID][0][3]=0;
								
							}
						}
						/*$vul;
						if($zk==0)
						{
							$zk++;
							if(!$cve[(string)$node[0]['vulnID']])
							{
								$cve[(string)$node[0]['vulnID']][0]=1;
								$vul=(string)$node[0]['vulnID'];
							}
							else
							{
								//$cve[(string)$node[0]['vulnID']][0]=$cve[(string)$node[0]['vulnID']][0]+1;
								$vul=(string)$node[0]['vulnID'];
							}
						}
						*/
						if($ID=="")
						{
							$ID=(string)$node['nodeName'];
							$IP=(string)$node['IPAddress'];
								
						}
		
						//$criticalID=$ID;
						//$criticalIP=$IP;
						$ID=(string)$node['nodeName'];
						$IP=(string)$node['IPAddress'];
						$criticalID=$ID;
						$criticalIP=$IP;
						$nodevul = (string)$node['vulnID'];
						//echo "hello";
					}
					if(array_key_exists($criticalID,$uassets))
					{
						$uassets[$criticalID][1][1]=$uassets[$criticalID][1][1]+$securityIndex;
						$uassets[$criticalID][1][4]=$uassets[$criticalID][1][4]+1;
						$uassets[$criticalID][1][5][$nodevul]=1;
						/*if(!$cve[$vul][1][$criticalID])
							$cve[$vul][1][$criticalID]=1;
						else
							$cve[$vul][1][$criticalID]=$cve[$vul][1][$criticalID]+1;
						*/
						$uassets[$criticalID][1][2]=$performanceIndex;
						$uassets[$criticalID][1][3]=$uassets[$criticalID][1][3]+$cyberCost;
						$uassets[$criticalID][0][6]="Target";
					}
					else
					{
						//$cve[$vul][1][$criticalID]=$cve[$vul][1][$criticalID]+1;
						$uassets[$criticalID][1][1]=$securityIndex;
						$uassets[$criticalID][0][0]=$criticalIP;
						$uassets[$criticalID][1][4]=1;
						$uassets[$criticalID][1][5][$nodevul]=1;
						$uassets[$criticalID][1][2]=$performanceIndex;
						$uassets[$criticalID][1][3]=$cyberCost;
						$uassets[$criticalID][0][1]=0;
						$uassets[$criticalID][0][2]=0;
						$uassets[$criticalID][0][3]=0;
						
					}
				}
			}
		}
	
	echo "<br/>";
		//print_r($uassets);
	echo "<div style='width: 500px; height: 340px; overflow-y: scroll; border:1px' >"; 

	
	if(isset($uassets)&&is_array($uassets))
	{
		echo "<table  id='assettable' class='tablesorter'><thead ><th class='header headerSortDown' width='27px;' >ID</th><th class='header' width='70px;'>IP Address</th><th class='header' width='50px;' >Type</th><th>Physical Metric (Current/Previous)</th><th>Cyber Metric (Current/Previous)</th><th>Rank (Current/Previous)</th></tr></thead><tbody class='member'>"; 
		$i=0;
		foreach($uassets as $key => $value)
		{	$j=0;
			$i++;
			$k=json_encode($value[0][0]);
			echo "<tr id='example'  onmouseover='change(this);' onmouseout='changeback(this);' onclick='showAsset($k)'>";
			echo "<td>".$i."</td>"; //ID
			echo "<td>".$value[0][0]; //IP Address
			echo "</td><td>";
			if(isset($value[0][6]))
			echo $value[0][6]."</td>"; //node type
			else
			echo " Source </td>";
			$hosts[]='abcdefg';
			//Physical metric doesn't look right ***debug***
			echo "<td>".$value[0][2]." / ".$value[1][2]."</td>"; //physical metric
			echo "<td>".$value[0][3]." / ".$value[1][3]."</td>"; //cyber metric
			echo "<td>".$value[0][1]." / ".$value[1][1]."</td></tr>"; //rank
		}
		echo "</tbody></table></div>";
	}
	else
		echo "<table><tr><td>No Vulnerabilties reported</td></tr></table>";

?>	
