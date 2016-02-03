<?php
session_start();

$userinfo = array(
                'cypsa'=>'cypsaonly',
                'panini'=>'panini'
                );

if(isset($_GET['logout'])) {
    $_SESSION['username'] = '';
    header('Location:  ' . $_SERVER['PHP_SELF']);
}

if(isset($_POST['username'])) {
    if($userinfo[$_POST['username']] == $_POST['password']) {
        $_SESSION['username'] = $_POST['username'];
        $invalid=0;
        header("Location: http://web.engr.oregonstate.edu/~patapanp/arpa-e/arpa-e/web_ui/index.php");
    }else {
        //Invalid Login
        $invalid=1;
    }
}
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
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
    </head>
    <body>
        <?php if($_SESSION['username']){ ?>
            <p>You are logged in as <?=$_SESSION['username']?></p>
            <p><a href="?logout=1">Logout</a></p>
        <?php }
        else { header("Location: http://web.engr.oregonstate.edu/~patapanp/arpa-e/arpa-e/web_ui/login.php");
} ?><div id="banner">
	<h1><em>Cy</em>PSA</h1>
	<a href="#"></a>
</div>

<br/><br/>

<div id="main">
        <form name="login" action="" method="post">
           <table align="center"> <tr><td>Username: </td><td> <input type="text" name="username" value="" /><br /></td></tr>
           <tr><td> Password: </td><td> <input type="password" name="password" value="" /><br /></td></tr>
           <tr align="center"><td colspan="2"> <input type="submit" name="submit" value="Submit" /></td></tr>
           <?php if($invalid==1)
           	echo "<tr align='center'><td colspan='2'><font color='red'>Wrong username or password</font></td></tr>"?>
            </table>
        </form>
        </div>
    </body>
</html>