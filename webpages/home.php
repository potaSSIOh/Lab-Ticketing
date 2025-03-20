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

    <h1>Welcome</h1>

    <!-- Dropdowns for selecting options -->
    <div class="dropdown-container">
        <!-- Dropdown for Aule -->
        <div>
            <h4>Aule</h4>
            <select name="Aule" id="AuleList" onchange="handleAuleChange()">
                <option value="">Select Aule</option>
                <option value="Aule1">247</option>
                <option value="Aule2">Aule 2</option>
                <option value="Aule3">Aule 3</option>
            </select>
        </div>

        <!-- Dropdown for Box -->
        <div>
            <h4>Box</h4>
            <select name="SecondSelect" id="SecondSelect" onchange="handleBoxChange()">
                <option value="">Select Box</option>
                <option value="Box1">Box 1</option>
                <option value="Box2">Box 2</option>
                <option value="Box3">Box 3</option>
            </select>
        </div>
    </div>

    <script>
        // Function to handle change in "Aule" dropdown
        function handleAuleChange() {
            var auleDropdown = document.getElementById('AuleList');

            // Get the selected option element
            var selectedOption = auleDropdown.options[auleDropdown.selectedIndex];

            // Get the text content of the selected option (not the value)
            var selectedAuleContent = selectedOption.textContent || selectedOption.innerText;

            // Check if something is selected
            if (selectedAuleContent) {
                // Send the selected content to the server using AJAX
                var xhr = new XMLHttpRequest();
                xhr.open('POST', 'saveAuleToSession.php', true);
                xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

                // Send the selected content to the server
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

        // Function to handle change in "Box" dropdown (empty for now, can be customized)
        function handleBoxChange() {
            var boxDropdown = document.getElementById('SecondSelect');
            var selectedBox = boxDropdown.value; // Get the selected value

            if (selectedBox) {
                // Handle the box selection logic here
                console.log('Selected Box: ' + selectedBox);
            }
        }
    </script>

</body>

</html>
