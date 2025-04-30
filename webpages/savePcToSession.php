<?php
session_start(); // Start the session

// Check if the selectedAule is set in the POST request
if (isset($_POST['selectedPc'])) {
    // Set the session variable $_SESSION["nAule"]
    $_SESSION["Pc"] = $_POST['selectedPc'];
    
    // Optionally, you can return a response to the client
    echo 'Session variable $_SESSION["Pc"] has been set to: ' . $_SESSION["Pc"];
}
?>