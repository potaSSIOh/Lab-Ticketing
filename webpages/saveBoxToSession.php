<?php
session_start(); // Start the session

// Check if the selectedAule is set in the POST request
if (isset($_POST['selectedBox'])) {
    // Set the session variable $_SESSION["nAule"]
    $_SESSION["codBox"] = $_POST['selectedBox'];
    
    // Optionally, you can return a response to the client
    echo 'Session variable $_SESSION["codBox"] has been set to: ' . $_SESSION["codBox"];
}
?>