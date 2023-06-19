from actions.auth_actions import generateJWT, validateJWT
import pytest


# PYTHONPATH=. pytest


def test_generateJWT():
    # TODO: better to mock JWT secret. otherwise, the test will fail if we change the JWT secret
    correct_jwt = generateJWT(id=2, email="test@test.com")
    assert correct_jwt is not None
    assert type(correct_jwt) is str


def test_validateJWT():
    generated_JWT = generateJWT(id=2, email="test@test.com")
    decoded_jwt = validateJWT(generated_JWT)
    assert type(decoded_jwt) == dict
    assert decoded_jwt["id"] == 2
    assert decoded_jwt["email"] == "test@test.com"
    assert "password" not in decoded_jwt
    assert "hashed_password" not in decoded_jwt
    assert len(decoded_jwt) == 2
