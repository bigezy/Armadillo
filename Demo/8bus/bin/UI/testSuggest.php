<?php
session_start();
if(isset($_GET['action']) && $_GET['action'] == "patch") {
	$hosts1 = $_POST['hosts'];
	$file=$_SESSION['project'].'/patched.csv';
	$fp = fopen($file, 'w');

	foreach($hosts1 as $key=>$critic)
	{
		$row= array($critic,'1');
		//echo $critic;
		fputcsv($fp, $row);
	}

	fclose($fp);
	chmod($file,0777);
	header("Location: index.php?action=patchInfoSent");
}
if(isset($_GET['action']) && $_GET['action'] == "configure") {
	$hosts1 = $_POST['hosts'];
	$file=$_SESSION['project'].'/compromised.csv';
	$fp = fopen($file, 'w');
	
	foreach($hosts1 as $key=>$critic)
	{
		$row= array($critic,'1');
		//echo $critic;
		fputcsv($fp, $row);
		}
		
		fclose($fp);
		chmod($file,0777);
		header("Location: index.php?action=compramizedInfoSent");
}
if(isset($_GET['action']) && $_GET['action'] == "vulnBased") {
	$vulnBased = $_POST['vulnBased'];
	
	$file=$_SESSION['project'].'/patchvulnerability.csv';
	$fp = fopen($file, 'w');
	foreach($vulnBased as $key => $value)
	{
		foreach($value as $host => $value1)
		{
			//echo "<br> Vulnerability : ".$key." - Host : ".$value1;
			
				$row= array($key,$value1);
			fputcsv($fp, $row);
			if($value1 == "all")
				break;
		}
	}
	
		
	

	fclose($fp);
	chmod($file,0777);
	
	header("Location: index.php?action=patchInfoSubmitted");
}