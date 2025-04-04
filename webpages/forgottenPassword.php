<?php
include 'libs/connection.php';
// Dummy database for demonstration
$users = [
    "user@example.com" => ["password" => "old_password"],
    "ilBoss" => ["password" => "boss_password"]
];

// Function to generate a random token
function generate_token($length = 50) {
    return bin2hex(random_bytes($length / 2));
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $input = $_POST['email'];

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

    // Check if email/username exists in the database
    if (!isset($users[$email])) {
        echo "Email or username not found";
        exit;
    }

    // Generate a reset token
    $reset_token = generate_token();

    // Save the reset token to the database (pseudo-code)
    // In a real application, you should save this to your database
    $users[$email]['reset_token'] = $reset_token;

    // Send the reset token to the user's email (pseudo-code)
    // In a real application, you should send an actual email
    // sendPasswordResetEmail($email, $reset_token);

    echo "A password reset link has been sent to your email.";
}
?>