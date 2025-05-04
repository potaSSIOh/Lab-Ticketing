<?php
session_start();
session_unset();
session_destroy();
//il server da al client lo stato di "success" se tutto va bene
echo json_encode(["status" => "success"]);
?>