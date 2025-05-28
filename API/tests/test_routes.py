import pytest
from fastapi.testclient import TestClient
from API.app import app  # Assumendo che l'istanza FastAPI sia in API/main.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from API.app import app  # o main se il file si chiama main.py
from fastapi.testclient import TestClient

client = TestClient(app)

# Esempio: test GET per aule_routes
def test_get_aule():
    response = client.get("/aule")  # Modifica con il path reale
    assert response.status_code == 200

# Esempio: test POST per box_routes
def test_create_box():
    new_box = {"nome": "Box1", "capienza": 10}  # Aggiorna fields secondo schema reale
    response = client.post("/box", json=new_box)
    assert response.status_code in (200, 201)
    # assert "id" in response.json()  # Se la risposta prevede un id

# Esempio: test autenticazione login_routes
def test_login():
    credentials = {"username": "user", "password": "pass"}
    response = client.post("/login", data=credentials)
    assert response.status_code in (200, 401)

# Esempio: test GET per ticketf_routes
def test_get_ticketf():
    response = client.get("/ticketf")
    assert response.status_code == 200

# Esempio: test POST ticketp_routes
def test_create_ticketp():
    new_ticket = {"subject": "Problema", "description": "Dettagli"}
    response = client.post("/ticketp", json=new_ticket)
    assert response.status_code in (200, 201)

# Aggiungi altri test similari per ogni route, usando i path e i dati coerenti con il tuo schema

# Esempio di parametrizzazione
@pytest.mark.parametrize("endpoint", ["/aule", "/box", "/fissi", "/portatili", "/utenti"])
def test_generic_get(endpoint):
    response = client.get(endpoint)
    assert response.status_code == 200