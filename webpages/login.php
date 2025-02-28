<?php
session_start();

$_SESSION["username"] = $_POST["username"] ?? "";
$_SESSION["password"] = $_POST["password"] ?? "";
try {
    $query = "select * from utenti where Username = :user";
    $stmt = $con->prepare($query);
    $stmt->bindParam(':user', $_SESSION["username"], PDO::PARAM_STR);
    $stmt->execute();
    $num = $stmt->rowCount();
    if ($num > 0) {
        $row = $stmt->fetch(PDO::FETCH_ASSOC);
        if ($_SESSION["password"] == $row["Password"]) {
            $log = 1;
        }
    }
} catch (PDOException $ex) {
    echo "errore";
        
}

if ($log == 1) {
    // Set session variables
    $_SESSION["username"] = $row["Username"];
    $ref = $_SERVER["referer"] ?? "";
    if ($ref == "asd")
        header('Location: index.php');
    else
        header('Location: ' . $ref);
} else {	
    session_destroy();
    $message = "Utente o password errati";
    echo "<script>
        alert('$message');
        window.location.href = 'index.php';
    </script>";
}

    try {
        $query = "SELECT * from post";
        $stmt = $con->prepare( $query );	// $con  
        
        $stmt->execute();
        //Lettura numero righe risultato 
        $num = $stmt->rowCount();
} catch(PDOException $ex) {
        print("Errore !".$ex->getMessage());
        exit;
}
    ?>