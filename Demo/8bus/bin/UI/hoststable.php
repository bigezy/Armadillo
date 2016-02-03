<?php
//cmd 11/22/15 - broke into a seperate file to make reading the code a little easier
$totalvuln=0;
$compromised = array();
$patched = array();
$vpatch = array() ;

$chandle = fopen($folder.'\compromised.csv', "r");
if($chandle)
{		
	while (($data = fgetcsv($chandle, 1000, ",")) !== FALSE) {
		$compromised[]=$data[0];
	}
}
fclose($chandle);

$phandle = fopen($folder.'\patched.csv', "r");
if($phandle)
{
	while (($data = fgetcsv($phandle, 1000, ",")) !== FALSE) {
		$patched[]=$data[0];
	}
}
fclose($phandle);

$vhandle = fopen($folder.'\patchvulnerability.csv', "r");
if($vhandle)
{
	while (($data = fgetcsv($vhandle, 1000, ",")) !== FALSE) {
		//$vpatch[$data[0]][]=$data[1];
		//$vpatch[$data[0]]=$data[1];
		array_push($vpatch, $data[1]);
		//echo "<h1> $data[1] </h1>";
	}
}
fclose($vhandle);
echo "<div id='patch' style='width: 950px; height: 340px; overflow-y: scroll; border:1px'>";
if(isset($uassets)&&is_array($uassets))
{
	echo "<form name='config_form2' method='post' action='testSuggest.php?action=patch'><table id='patchhoststable' class='tablesorter'  border=1 width=840px;><thead><th>Select</th><th>Patch Host </th><th> CVE-ID's</th></thead><tbody>";
	foreach($uassets as $key => $value)
	{
	   if(is_array($patched))
	   {
		if(in_array($value[0][0], $patched))
		{
			$checked= "checked=checked";
			$background= "bgcolor='#A9F5BC'";
		}
		else
		{
			$checked="";
			$background= "bgcolor='#FA5858'";
		}
	   }
	   else
	   {
		$checked="";
		$background= "bgcolor='#FA5858'";
	   }
		echo "<tr $background><td  width=25px;> <input type='checkbox'  onclick='ChangeColor1(this)'  name='hosts[".$value[0][0]."]' $checked id=".$value[0][0]." value=".$value[0][0]."></input></td><td>".$value[0][0]."</td><td>";
		$i=0;
		if(isset($value[0][5]))
		foreach($value[0][5] as $key1=>$value1)
		{
			if($i!=0)
				echo ", ";
			if($key1=="")
				continue;
			echo $key1;
			
			$i++;
		}
		echo "</td></tr>";
	}
	echo "</tbody><tr align='center'><td colspan='3'><input type='submit' value='submit'></td></tr>";
	echo "</table></form>";
}
else
	echo "<table><tr><td>No Data Available</td></tr></table>";
	echo "</div>";
	echo "<div id='compromised' style='width: 950px; height: 340px; overflow-y: scroll; border:1px display:none;'><form name='config_form1' method='post' action='testSuggest.php?action=configure'>";
	
	$hhandle = fopen($folder.'\host_ips.csv', "r");
	if($hhandle)
	{	
		echo "<table id='compromisedhosttable' class='tablesorter'  border=1 width=840px;>";
		echo "<thead><th>Select</th><th>Compromised Host </th></thead><tbody>";
		while (($data = fgetcsv($hhandle, 1000, ",")) !== FALSE) {
			if(in_array($data[0], $compromised))
			{
				$checked= "checked=checked";
				$background= "bgcolor='#FA5858'";
			}
			else 
			{
				$checked="";
				$background= "bgcolor='#A9F5BC'";
			}
		echo "<tr $background ><td  width=25px;> <input type='checkbox' onclick='ChangeColor(this)' ";
		
		echo "$checked name='hosts[".$data[0]."]' id=".$data[0]." value=".$data[0]."></input></td><td>".$data[0]."</td></tr>";
		}
		echo "</tbody><tr align='center'><td colspan='3'><input type='submit' value='submit'></td></tr>";
		echo "</table>";
	
	}
	else 
	{
		echo "<table   border=1 width=840px;><tbody>";
		echo "<tr><td>No File or Data</td></tr></tbody></table>";
	}
	fclose($hhandle);	
	echo "</form></div>";
	echo "<div id='vulnerability' style='width: 950px; height: 340px; overflow-y: scroll; border:1px display:none;'><form name='config_form5' method='post' action='testSuggest.php?action=vulnBased'><table id='vulnerabilitypatchtable' class='tablesorter'  border=1 width=840px;><thead><th>Vulnerability ID</th><th> Frequency </th><th> Select Hosts </th> </thead><tbody>";

	foreach($cve as $vulnID => $value)
	{
		//echo $vpatch;	
		if(array_key_exists($vulnID, $vpatch))
		{
			$background= "bgcolor='#A9F5BC'";
		}
		else
		{
			$background= "";
		}
		echo "<tr><td>".$vulnID."  ";
		$all='all';
		if(array_key_exists($vulnID, $vpatch))
		{
			//echo "<h1> $all:$vulnID<\h1>";
			if(in_array($all,$vpatch[$vulnID]))
				$selected= "selected";
			else
				$selected="";	
		}
		else
			$selected="";
		echo "</td><td>".$cve[$vulnID][0]."</td><td><select name='vulnBased[$vulnID][]' size='5' multiple><option value='$all' $selected>Select All</option>";
		foreach($value[1] as $host => $present)
		{
			//echo "<h1> $host:$vulnID:$vpatch[$vulnID]: </h1>";
			//if(in_array($host, $vpatch[$vulnID]))
			if(in_array($host, $vpatch))
			{
				$selected= "selected";
			}
			else 
				$selected="";
			echo "<option value='$host' $selected>".$host." - ".$present."</option>";
		}
		echo "</select></td></tr>";
					$totalvuln+=$value[0];
	}
	echo "</tbody><tr><td> Total Vulnerabilities: </td><td> ".$totalvuln."</td><td></td></tr>
	<tr align='center'><td colspan='3'><input type='submit' value='submit'></td></tr></table><br><br></form></div>";
	//echo "<table><tr><td>".print_r($vpatch)."</td></tr></table>";
?>
