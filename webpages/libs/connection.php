<?php
error_reporting(E_ALL);
$host = "127.0.0.1";
$db_name = "labticketing";
$username = "root";
$password = "";
try {
	
    $con = new PDO("mysql:host={$host};dbname={$db_name}", $username, $password,array(PDO::ATTR_PERSISTENT => true));
	
	$con->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
}  
// to handle connection error
catch(Exception $exception){
	
    echo "Connection error: " . $exception->getMessage();
	exit;
}
?>