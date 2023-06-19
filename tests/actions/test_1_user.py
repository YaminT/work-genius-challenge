from fastapi import Depends
from psycopg2 import IntegrityError
from pytest import Session
from actions.user_actions import (
    create_user,
    get_user_by_email,
    get_user_by_id,
    check_user_password,
)
from database import get_db
from interfaces.user import UserCreate

from models.user_model import UserModel

sample_user = {"email": "test@test.com", "password": "password"}
sample_user_2 = {"email": "test2@test.com", "password": "password"}


def test_create_user():
    db = next(get_db())
    user = UserCreate(email=sample_user["email"], password=sample_user["password"])
    created_user = create_user(db=db, user=user)
    assert created_user != None
    assert created_user.email != None
    assert created_user.id != None
    sample_user["id"] = created_user.id
    assert created_user.own_team != None


def test_create_second_user():
    db = next(get_db())
    user = UserCreate(email=sample_user_2["email"], password=sample_user_2["password"])
    created_user = create_user(db=db, user=user)
    assert created_user != None
    assert created_user.email != None
    assert created_user.id != None
    sample_user_2["id"] = created_user.id
    assert created_user.own_team != None


def test_create_user_duplicate_email():
    db = next(get_db())
    user = UserCreate(email=sample_user["email"], password=sample_user["password"])
    created_user = create_user(db=db, user=user)
    assert created_user == None


def test_get_user_by_email():
    db = next(get_db())
    existing_user = get_user_by_email(email=sample_user["email"], db=db)
    assert existing_user != None


def test_get_user_by_email_not_found():
    db = next(get_db())
    existing_user = get_user_by_email(email="random@rand.com", db=db)
    assert existing_user == None


def test_get_user_by_id():
    db = next(get_db())
    existing_user = get_user_by_id(id=sample_user["id"], db=db)
    assert existing_user != None


def test_get_user_by_id_not_found():
    db = next(get_db())
    existing_user = get_user_by_id(id=-1, db=db)
    assert existing_user == None


def test_check_user_password():
    db = next(get_db())
    existing_user = check_user_password(
        email=sample_user["email"], password=sample_user["password"], db=db
    )
    assert existing_user != None


def test_check_user_password_wrong_pass():
    db = next(get_db())
    existing_user = check_user_password(
        email=sample_user["email"], password="wrong password", db=db
    )
    assert existing_user == None
