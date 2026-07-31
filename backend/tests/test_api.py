import os
os.environ["DATABASE_URL"]="sqlite+aiosqlite:///./careerflow-test.db"
from uuid import uuid4
from fastapi.testclient import TestClient
from app.main import app
def test_health():
    with TestClient(app) as client: assert client.get("/health").status_code==200
def test_private_route_requires_token():
    with TestClient(app) as client: assert client.get("/applications").status_code==401
def test_register_create_and_list():
    with TestClient(app) as client:
        token=client.post("/auth/register",json={"email":f"candidate-{uuid4()}@example.com","password":"strong-password"}).json()["access_token"]
        headers={"Authorization":f"Bearer {token}"}
        created=client.post("/applications",headers=headers,json={"company":"Acme","role":"Backend Engineer"});assert created.status_code==201
        assert client.get("/applications",headers=headers).json()[0]["company"]=="Acme"
