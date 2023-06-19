from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def prepare_token():
    response = client.post(
        "/auth/login", json={"email": "testnew@test.com", "password": "111111"}
    )
    assert response.status_code == 200
    parsed_response = response.json()
    return parsed_response["token"]


def test_create_new_team_without_access():
    response = client.post("/team/", json={"name": "team", "description": "Awesomer"})
    assert response.status_code == 401
    parsed_response = response.json()
    assert parsed_response != None


def test_create_new_team():
    token = prepare_token()
    response = client.post(
        "/team/",
        json={"name": "team", "description": "Awesomer"},
        headers={"Authorization": "Bearer " + token},
    )
    assert response.status_code == 200
    parsed_response = response.json()
    assert parsed_response != None


def test_create_new_team_dup_name():
    token = prepare_token()
    assert token != None
    print("Bearer" + token)
    response = client.post(
        "/team/",
        json={"name": "team", "description": "Awesomer"},
        headers={"Authorization": "Bearer " + token},
    )
    assert response.status_code == 400
    parsed_response = response.json()
    assert parsed_response != None


def test_edit_new_team_no_access():
    token = prepare_token()
    assert token != None
    print("Bearer" + token)
    response = client.patch(
        "/team/1",
        json={"name": "team2", "description": "Awesomer2"},
        headers={"Authorization": "Bearer " + token},
    )
    assert response.status_code == 400
    parsed_response = response.json()
    assert parsed_response != None


def test_edit_new_team():
    token = prepare_token()
    assert token != None
    print("Bearer" + token)
    response = client.patch(
        "/team/2",
        json={"name": "team2", "description": "Awesomer2"},
        headers={"Authorization": "Bearer " + token},
    )
    assert response.status_code == 200
    parsed_response = response.json()
    assert parsed_response != None


def test_delete_new_team_no_access():
    token = prepare_token()
    assert token != None
    print("Bearer" + token)
    response = client.delete("/team/1", headers={"Authorization": "Bearer " + token})
    assert response.status_code == 400
    parsed_response = response.json()
    assert parsed_response != None


def test_delete_new_team():
    token = prepare_token()
    assert token != None
    print("Bearer" + token)
    response = client.delete("/team/2", headers={"Authorization": "Bearer " + token})
    assert response.status_code == 200
    parsed_response = response.json()
    assert parsed_response != None


def test_get_current_user_teams():
    test_create_new_team()
    token = prepare_token()
    assert token != None
    print("Bearer" + token)
    response = client.get("/team", headers={"Authorization": "Bearer " + token})
    assert response.status_code == 200
    parsed_response = response.json()
    print(parsed_response)
    assert parsed_response != None
