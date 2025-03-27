<?php
$user = $_SESSION["username"] ?? "";
$pass = $_SESSION["password"] ?? "";

if ($user == "") {
    header('Location: index.html');
    exit();
}

session_start();
include 'libs/connection.php';

try {
    // Query per ottenere i dati dalla tabella aule
    $queryAule = "SELECT nAula FROM aule";
    $stmtAule = $con->prepare($queryAule);
    $stmtAule->execute();
    $aule = $stmtAule->fetchAll(PDO::FETCH_ASSOC);

    // Query per ottenere i dati dalla tabella box
    $queryBox = "SELECT codBox FROM box";
    $stmtBox = $con->prepare($queryBox);
    $stmtBox->execute();
    $box = $stmtBox->fetchAll(PDO::FETCH_ASSOC);

    // Salvare i dati nelle variabili di sessione
    $_SESSION['aule'] = $aule;
    $_SESSION['box'] = $box;

    // Verifica dell'utente e della password
    $queryUser = "SELECT * FROM users WHERE username = :user";
    $stmtUser = $con->prepare($queryUser);
    $stmtUser->bindParam(':user', $user, PDO::PARAM_STR);
    $stmtUser->execute();
    $num = $stmtUser->rowCount();

    if ($num > 0) {
        $rowUser = $stmtUser->fetch(PDO::FETCH_ASSOC);

        if ($pass == $rowUser["password"]) {
            $_SESSION["username"] = $user;
            $_SESSION["id"] = $rowUser["id"];

            header('Location: home.php');
            exit();
        }
    }

} catch(PDOException $ex) {
    echo "Error: " . $ex->getMessage();
    exit();
}

session_destroy();
header('Location: index.html?error=1');
exit();
?>