from fastapi.testclient import TestClient
from actions import user_actions as user_actions
from database import get_db
from interfaces.user import UserCreate

from main import app

client = TestClient(app)


def prepare_new_user():
    db = next(get_db())
    request_user = UserCreate(email="sample@test.com", password="111111")
    new_user = user_actions.create_user(user=request_user, db=db)
    return new_user.id


def login_new_user():
    db = next(get_db())
    new_user = user_actions.check_user_password(
        email="sample@test.com", password="111111", db=db
    )
    return new_user.id


def prepare_token():
    response = client.post(
        "/auth/login", json={"email": "testnew@test.com", "password": "111111"}
    )
    assert response.status_code == 200
    parsed_response = response.json()
    return parsed_response["token"]


def test_add_user_to_team():
    token = prepare_token()
    assert token != None
    new_user_id = prepare_new_user()
    response = client.post(
        "/membership",
        json={"user_id": new_user_id, "team_id": 2},
        headers={"Authorization": "Bearer " + token},
    )
    parsed_response = response.json()
    assert response.status_code == 200
    assert parsed_response != None


def test_add_user_to_team_without_access():
    token = prepare_token()
    assert token != None
    new_user_id = login_new_user()
    response = client.post(
        "/membership",
        json={"user_id": new_user_id, "team_id": 1},
        headers={"Authorization": "Bearer " + token},
    )
    parsed_response = response.json()
    assert response.status_code == 400
    assert parsed_response != None


def test_remove_user_from_team_without_access():
    token = prepare_token()
    assert token != None
    new_user_id = login_new_user()
    response = client.delete(
        "/membership/user/" + str(new_user_id) + "/team/1",
        headers={"Authorization": "Bearer " + token},
    )
    assert response.status_code != 200


def test_remove_user_from_team():
    token = prepare_token()
    assert token != None
    new_user_id = login_new_user()
    response = client.delete(
        "/membership/user/" + str(new_user_id) + "/team/2",
        headers={"Authorization": "Bearer " + token},
    )
    assert response.status_code == 200


def list_of_users():
    token = prepare_token()
    assert token != None
    response = client.get("/users", headers={"Authorization": "Bearer " + token})
    assert response.status_code == 200
    parsed_response = response.json()
    assert type(parsed_response) == list
    assert len(parsed_response) == 1


def list_of_users_without_access():
    response = client.get("/users/")
    assert response.status_code == 401


# def test_edit_new_team():
#     token = prepare_token()
#     assert token != None
#     print('Bearer' + token)
#     response = client.patch('/team/2', json={
#         "name": "team2",
#         "description": "Awesomer2"
#     }, headers={"Authorization": 'Bearer ' + token})
#     assert response.status_code == 200
#     parsed_response = response.json()
#     assert parsed_response != None

# def test_delete_new_team_no_access():
#     token = prepare_token()
#     assert token != None
#     print('Bearer' + token)
#     response = client.delete('/team/1', headers={"Authorization": 'Bearer ' + token})
#     assert response.status_code == 400
#     parsed_response = response.json()
#     assert parsed_response != None

# def test_delete_new_team():
#     token = prepare_token()
#     assert token != None
#     print('Bearer' + token)
#     response = client.delete('/team/2', headers={"Authorization": 'Bearer ' + token})
#     assert response.status_code == 200
#     parsed_response = response.json()
#     assert parsed_response != None
