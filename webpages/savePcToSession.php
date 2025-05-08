<?php
session_start(); // Start the session

// Check if the selectedAule is set in the POST request
    // Set the session variable $_SESSION["nAule"]
    $_SESSION["Pc"] = $_POST['selectedPc'];
    $_SESSION["Type"] = $_POST['PcType'];
    // Optionally, you can return a response to the client
    echo 'Session variable $_SESSION["Pc"] has been set to: ' . $_SESSION["Pc"] ;
    echo 'Session variable $_SESSION["Type"] has been set to: ' . $_SESSION["Type"] ;
?>