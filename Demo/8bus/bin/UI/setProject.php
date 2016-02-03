<?php session_start();

$_SESSION['project']=$_POST['project'];
header("Location: index.php");
?>