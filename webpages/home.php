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
            flex-direction: column; /* Impila gli elementi in verticale */
            align-items: center; /* Ricentra gli oggetti del Body */
            padding: 20px;
        }

        /* Stile per ogni oggetto del Dropdown */
        .dropdown-container {
            display: flex;
            justify-content: space-between; /* Distanzio i Dropdown */
            width: 100%;
            max-width: 600px; 
            margin-top: 20px; /* Per distanziare i dropdown e il titolo */
        }

        /* stile per i dropdown */
        select {
            padding: 10px;
            font-size: 16px;
            margin: 10px 0;
            border: 1px solid #ccc;
            border-radius: 5px;
        }

        h1 {
            text-align: center;
        }

        h4 {
            margin-right: 10px; 
        }
    </style>
</head>
<body>

    <h1>Welcome</h1>

    <!-- Tabelle per i dropdown, verranno poi popolate in base ai dati ricevuti dal Database-->
    <div class="dropdown-container">
        <div>
            <h4>Aule</h4>
            <select name="Aule" id="AuleList">

            </select>
        </div>

        <div>
            <h4>Box</h4>
            <select name="SecondSelect" id="SecondSelect">

            </select>
        </div>
    </div>

</body>
</html>

    
<!-- parte della tabella 

    <table id="prodottiTable">
        <thead>
            <tr>
                <th>ID</th>
                <th>Nome</th>
                <th>Descrizione</th>
                <th>Prezzo</th>
                <th>Azioni</th> 
            </tr>
        </thead>
        <tbody id="TABPC">
           
        </tbody>
    </table>

<script>
        window.onload = function() {
            // URL della pagina PHP che restituisce i dati XML
            var url = 'prod001.php';

            // Carica il file XML
            fetch(url)
                .then(response => response.text())  // asincrona
                .then(data => {
                    var parser = new DOMParser();
                    var xmlDoc = parser.parseFromString(data, 'application/xml');
                    var prodotti = xmlDoc.getElementsByTagName('prodotto');

                    // Ottieni il corpo della tabella
                    var tableBody = document.getElementById('TABPROD');

                    // Loop attraverso ogni prodotto e aggiungi una riga nella tabella
                    for (var i = 0; i < prodotti.length; i++) {
                        var row = tableBody.insertRow();
                        var idCell = row.insertCell(0);
                        var nomeCell = row.insertCell(1);
                        var descrCell = row.insertCell(2);
                        var prezzoCell = row.insertCell(3);
                        var actionCell = row.insertCell(4); // Cella per il pulsante di modifica

                        // Estrai l'ID dal nodo prodotto
                        var id = prodotti[i].getAttribute('id');
                        idCell.textContent = id;

                        // Estrai i dati del prodotto (nome, descrizione, prezzo)
                        var nome = prodotti[i].getElementsByTagName('nome')[0]?.textContent || 'N/A';
                        var descr = prodotti[i].getElementsByTagName('descr')[0]?.textContent || 'N/A';
                        var prezzo = prodotti[i].getElementsByTagName('prezzo')[0]?.textContent || 'N/A';

                        nomeCell.textContent = nome;
                        descrCell.textContent = descr;
                        prezzoCell.textContent = prezzo;

                        // Crea il pulsante "modifica"
                        var modifyButton = document.createElement('button');
                        modifyButton.textContent = 'Modifica';
                        modifyButton.onclick = function() {
                            // Puoi aggiungere la logica per modificare il prodotto, 
                            // ad esempio redirigendo a una pagina di modifica con l'ID del prodotto
                            window.location.href = 'changeProd.php?id=' + id; // Passa l'ID del prodotto per la modifica
                        };

                        // Aggiungi il pulsante alla cella di azioni
                        actionCell.appendChild(modifyButton);
                    }
                })
                .catch(error => {
                    console.error("Errore nel caricamento dei dati:", error);
                });
        };
    </script>
 -->
    