import sys
import os
import pytest
import uuid

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from API.app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_get_aule(client):
    response = client.get("/aule")
    assert response.status_code == 200

def test_get_utenti(client):
    response = client.get("/utenti")
    assert response.status_code == 200

def test_get_ticketf(client):
    response = client.get("/ticketf")
    assert response.status_code == 200

@pytest.mark.parametrize("endpoint", ["/aule", "/box", "/fissi", "/portatili"])
def test_generic_get(client, endpoint):
    response = client.get(endpoint)
    assert response.status_code == 200

def test_post_aule(client):
    unique_lab = str(uuid.uuid4())
    payload = {"nAula": "Aula_{unique_lab}", "Lab": f"Lab_{unique_lab}"}
    response = client.post("/aule", json=payload)
    assert response.status_code in [201, 400, 403]

def test_post_utenti(client):
    unique_mail = f"user_{uuid.uuid4()}@example.com"
    payload = {"name_mail": unique_mail, "password": "testpass", "autorizzato": 1}
    response = client.post("/utenti", json=payload)
    assert response.status_code in [201, 400, 403]

def test_patch_ticketf_descrizione(client):
    response = client.patch("/ticketf/1", json={"descrizione": "new desc"})
    assert response.status_code in [200, 400, 404, 403]

def test_patch_ticketf_tecnico(client):
    response = client.patch("/ticketf/1/tecnico", json={"tecnico": "newtech"})
    assert response.status_code in [200, 400, 404, 403]

def test_post_login_missing_credentials(client):
    response = client.post("/login", json={})
    assert response.status_code == 400

def test_post_login_invalid_credentials(client):
    response = client.post("/login", json={"name_mail": "wrong", "password": "wrong"})
    assert response.status_code in [200, 401]