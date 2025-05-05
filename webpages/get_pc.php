<?php
session_start();

header('Content-Type: application/json');

// Prepare the response data
$response = [];

// Check if 'Pc' is set in the session
if (isset($_SESSION['Pc'])) {
    $response['Pc'] = $_SESSION['Pc'];
} else {
    $response['Pc'] = null;
}

// Check if 'Type' is set in the session
if (isset($_SESSION['Type'])) {
    $response['Type'] = $_SESSION['Type'];
} else {
    $response['Type'] = null;
}

// Send the JSON response
echo json_encode($response);
?>