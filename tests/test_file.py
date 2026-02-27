# import pytest
# from fastapi.testclient import TestClient
# from main import app

# @pytest.mark.parametrize("a, b , res", [(1, 2, 3), (2, 3, 5), (3, 4, 7)])
# def test_add(a, b, res):
#     assert a+b == res

# @pytest.mark.hey
# def test_add():
#     assert(2+3) == 5  

# client = TestClient(app)

def test_register(test_client):
    res = test_client.post(
        "/register",
        json = {
            "username": "testing", 
            "password": "testing"
        }
    )

    assert res.status_code == 200
    assert res.json()["message"] == "registered"

def test_login(test_client):
    res = test_client.post(
        "/register", 
        json = {
            "username": "testing", 
            "password": "password"
        }
    )

    res2 = test_client.post(
        "/login",
        json = {
            "username": "testing", 
            "password": "password"
        }
    )

    assert res2.status_code == 200
    assert "access token" in res2.json()

def test_journal_entry(test_client):
    res = test_client.post(
        "/register", 
        json = {
            "username": "testing", 
            "password": "password"
        }
    )

    res2 = test_client.post(
        "/login",
        json = {
            "username": "testing", 
            "password": "password"
        }
    )

    token = res2.json()["access token"]
    headers = {"Authorization": f"Bearer {token}"}

    jour = test_client.post(
        "/api/create", 
        json = {
            "title": "testing", 
            "content": "i am writing this in testing"
          }, 
        headers=headers  
    )

    assert jour.status_code == 200
    assert jour.json()["title"] == "testing"

