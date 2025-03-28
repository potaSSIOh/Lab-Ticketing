<!DOCTYPE html>
<html lang="it">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Home</title>
    <link rel="stylesheet" href="styles/style.css">

    <style>
        body {
            display: flex;
            flex-direction: column; /* Stack elements vertically */
            align-items: center; /* Center elements */
            padding: 20px;
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
        }

        h1 {
            text-align: center;
            margin-bottom: 20px;
        }

        .dropdown-container {
            display: flex;
            justify-content: space-between; /* Space out the dropdowns */
            width: 100%;
            max-width: 800px;
            margin-top: 20px;
        }

        h4 {
            margin-bottom: 10px;
            font-size: 18px;
            color: #333;
        }

        select {
            padding: 10px;
            font-size: 16px;
            width: 100%;
            border: 1px solid #ccc;
            border-radius: 5px;
            box-sizing: border-box;
        }

        select:focus {
            outline: none;
            border-color: #007bff;
        }
    </style>
</head>

<body>
    
<label class="theme">
        <div id="themeToggle" class="theme__toggle"></div>
    </label>

    <script>
        document.addEventListener("DOMContentLoaded", function () {
            const toggle = document.getElementById("themeToggle");
            const body = document.body;

            // Controlla se c'è un tema salvato nel localStorage
            if (localStorage.getItem("theme") === "dark") {
                body.classList.add("dark-mode");
                toggle.classList.add("checked");
            }

            toggle.addEventListener("click", function () {
                if (body.classList.contains("dark-mode")) {
                    body.classList.remove("dark-mode");
                    toggle.classList.remove("checked");
                    localStorage.setItem("theme", "light");
                } else {
                    body.classList.add("dark-mode");
                    toggle.classList.add("checked");
                    localStorage.setItem("theme", "dark");
                }
            });
        });
    </script>


    <h1>Welcome</h1>

    <div class="dropdown-container">
        
        <!-- Dropdown per le Aule -->
        <div>
            <h4>Aule</h4>
            <?php
            $url = 'localhost:5000/aule';
            // inizializzazione della sessione curl
            $ch = curl_init($url);

            // opzioni curl
            curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

            // eseguo il curl
            $response = curl_exec($ch);

            // Check degli errori
            if (curl_errno($ch)) {
                echo 'Error:' . curl_error($ch);
            } else {
                //Trasformo il json in un array PHP
                $data = json_decode($response, true);
            }

            // Chiudo la sessione
            curl_close($ch);
            ?>
            <!-- Popolo i dropdown in base ai dati ricavati dal Json-->
            <select name="Aule" id="AuleList" onchange="handleAuleChange($data)">
                <option value="">Select Aule</option>
                <?php
                foreach ($data as $element) {
                    echo "<option value='" . $element['nAula'] . "'>" . $element['nAula'] . "</option>";
                }
                ?>
            </select>
        </div>

        <!-- Dropdown per i Box -->
        <div>
            <h4>Box</h4>
            <?php
            $url = 'localhost:5000/box';
            // inizializzo la sessione
            $ch = curl_init($url);

            // Imposto le opzioni
            curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

            // Eseguo
            $response = curl_exec($ch);

            // Check degli errori
            if (curl_errno($ch)) {
                echo 'Error:' . curl_error($ch);
            } else {
                // Trasformo json in array PHP
                $data = json_decode($response, true);
            }

            // Chiudo la sessione
            curl_close($ch);
            ?>
            <!-- Popolo i dropdown in base ai dati ricavati dal Json-->
            <select name="Box" id="BoxList" onchange="handleBoxChange($data)">
                <option value="">Select Box</option>
                <?php
                foreach ($data as $element) {
                    echo "<option value='" . $element['codBox'] . "'>" . $element['codBox'] . "</option>";
                }
                ?>
            </select>
        </div>

    </div>

    <script>
        // Funzione per salvare in sessione il valore dentro al dropdown delle aule
        function handleAuleChange($data) {
            var auleDropdown = document.getElementById('AuleList');

            // Metto il valore nella variabile
            var selectedOption = auleDropdown.options[auleDropdown.selectedIndex];

            // Inserisco il contenuto in una variabile
            var selectedAuleContent = selectedOption.textContent || selectedOption.innerText;

            // Controllo se ho selezionato una riga del dropdown
            if (selectedAuleContent) {
                // Uso AJAX per mandare il valore al file PHP che si occupa delle sessioni
                var xhr = new XMLHttpRequest();
                xhr.open('POST', 'saveAuleToSession.php', true);
                xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

                xhr.send('selectedAule=' + encodeURIComponent(selectedAuleContent));

                xhr.onload = function () {
                    if (xhr.status == 200) {
                        console.log('Session variable $_SESSION["nAule"] has been set to: ' + selectedAuleContent);
                    } else {
                        console.error('Error in saving session variable');
                    }
                };
            }
        }

        // Funzione per salvare in sessione il valore dentro al dropdown dei box
        function handleBoxChange($data) {
            var boxDropdown = document.getElementById('BoxList');
            var selectedOption = boxDropdown.options[boxDropdown.selectedIndex];

            // Inserisco il contenuto in una variabile
            var selectedBoxContent = selectedOption.textContent || selectedOption.innerText;

// Controllo se ho selezionato una riga del dropdown
            if (selectedBoxContent) {
    // Uso AJAX per mandare il valore al file PHP che si occupa delle sessioni
                var xhr = new XMLHttpRequest();
                xhr.open('POST', 'saveBoxToSession.php', true);
                xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

                xhr.send('selectedAule=' + encodeURIComponent(selectedBoxContent));

                xhr.onload = function () {
                    if (xhr.status == 200) {
                        console.log('Session variable $_SESSION["codBox"] has been set to: ' + selectedBoxContent);
            } else {
                console.error('Error in saving session variable');
        }
    };
}
}
    </script>
    <?php

function generateTable($data) {
    if (empty($data)) {
        return; // Do not display anything if the array is empty
    }
    
    echo "<table border='1' cellpadding='5' cellspacing='0'>";
    echo "<tr>";
    
    // Table headers (assuming array keys as column names)
    foreach (array_keys($data[0]) as $key) {
        echo "<th>" . htmlspecialchars($key) . "</th>";
    }
    echo "</tr>";
    
    // Table rows
    foreach ($data as $row) {
        echo "<tr>";
        foreach ($row as $cell) {
            echo "<td>" . htmlspecialchars($cell) . "</td>";
        }
        echo "</tr>";
    }
    
    echo "</table>";
}

// Example data array
$data = [
    ["Name" => "Alice", "Age" => 25, "City" => "New York"],
    ["Name" => "Bob", "Age" => 30, "City" => "Los Angeles"],
    ["Name" => "Charlie", "Age" => 35, "City" => "Chicago"]
];

generateTable($data);
?>
</body>

</html>
