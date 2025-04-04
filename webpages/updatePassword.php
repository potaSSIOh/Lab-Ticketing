<?php
require_once 'libs/connection.php'; // Include the database connection

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $input = $_POST['email'];
    $token = $_POST['token'];
    $new_password = $_POST['new_password'];

    // Connect to the database
    $conn = connect_to_database();

    // Check if the input is the special username "ilBoss" (case insensitive)
    if (strtolower($input) === 'ilboss') {
        $email = 'ilBoss';
    } else {
        $email = $input;

        // Validate email format
        if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
            echo "Invalid email format";
            exit;
        }
    }

    // Prepare and execute the query to validate the token
    $stmt = $conn->prepare("SELECT * FROM users WHERE (email = ? OR username = ?) AND reset_token = ?");
    $stmt->bind_param("sss", $email, $email, $token);
    $stmt->execute();
    $result = $stmt->get_result();

    if ($result->num_rows == 0) {
        echo "Invalid token or email";
        exit;
    }

    // Update the user's password
    $stmt = $conn->prepare("UPDATE users SET password = ?, reset_token = NULL WHERE email = ? OR username = ?");
    $hashed_password = password_hash($new_password, PASSWORD_DEFAULT);
    $stmt->bind_param("sss", $hashed_password, $email, $email);

    if ($stmt->execute()) {
        echo "Password updated successfully.";
    } else {
        echo "Failed to update password.";
    }
    $stmt->close();
    $conn->close();
}
?>