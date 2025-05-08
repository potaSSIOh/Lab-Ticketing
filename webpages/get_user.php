<?php
session_start();

header('Content-Type: application/json');

// Prepare the response data
$response = [];

// Check if 'Pc' is set in the session
if (isset($_SESSION['username'])) {
    $response['username'] = $_SESSION['username'];
} else {
    $response['username'] = null;
}
echo json_encode($response);
?>