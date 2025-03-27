<?php
session_start(); // Start the session

// Check if the selectedAule is set in the POST request
if (isset($_POST['selectedAule'])) {
    // Set the session variable $_SESSION["nAule"]
    $_SESSION["nAule"] = $_POST['selectedAule'];
    
    // Optionally, you can return a response to the client
    echo 'Session variable $_SESSION["nAule"] has been set to: ' . $_SESSION["nAule"];
}
?>