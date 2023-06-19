from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_main_api():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Message": "Hello from work genius"}


def test_register_api():
    response = client.post(
        "/auth/register", json={"email": "testnew@test.com", "password": "111111"}
    )
    assert response.status_code == 200
    parsed_response = response.json()
    assert parsed_response != None
    assert (
        parsed_response["message"]
        == "Registration was successful. you can login using the passwords you"
    )


def test_register_api_fail_dup_email():
    response = client.post(
        "/auth/register", json={"email": "testnew@test.com", "password": "111111"}
    )
    assert response.status_code == 400
    parsed_response = response.json()
    assert parsed_response != None
    assert parsed_response["detail"] == "Email already exists."


def test_register_api_fail_short_password():
    response = client.post(
        "/auth/register", json={"email": "testnew2@test.com", "password": "111"}
    )
    assert response.status_code == 400
    parsed_response = response.json()
    assert parsed_response != None
    assert parsed_response["detail"] == "Password is too short"


def test_login_api():
    response = client.post(
        "/auth/login", json={"email": "testnew@test.com", "password": "111111"}
    )
    assert response.status_code == 200
    parsed_response = response.json()
    assert parsed_response != None
    assert parsed_response["email"] != None
    assert parsed_response["token"] != None
    assert parsed_response["message"] == "You are logged in successfully."


def test_login_api_fail():
    response = client.post(
        "/auth/login", json={"email": "t@test.com", "password": "111111"}
    )
    assert response.status_code == 400
    parsed_response = response.json()
    assert parsed_response != None
    assert parsed_response["detail"] == "Username or password is wrong"
