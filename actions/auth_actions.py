from typing import Annotated
from fastapi import Depends, HTTPException
import jwt
from fastapi.security import OAuth2PasswordBearer

from tools.constants import jwt_secret, jwt_algorithm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def generateJWT(id: int, email: str) -> str:
    return jwt.encode({"id": id, "email": email}, jwt_secret, algorithm=jwt_algorithm)


def validateJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, jwt_secret, algorithms=jwt_algorithm)
        if decoded_token["email"]:
            return decoded_token
    except:
        raise HTTPException(status_code=401, detail="JWT token is not valid")


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    user = validateJWT(token)
    return user
