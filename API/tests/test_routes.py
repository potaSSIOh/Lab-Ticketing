import sys
import os
import pytest


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



def test_get_ticketf(client):
    response = client.get("/ticketf")
    assert response.status_code == 200


@pytest.mark.parametrize("endpoint", ["/aule", "/box", "/fissi", "/portatili", "/utenti"])
def test_generic_get(client, endpoint):
    response = client.get(endpoint)
    assert response.status_code == 200