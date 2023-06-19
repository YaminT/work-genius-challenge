from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException

from interfaces.user import UserCreate, UserLogin
from interfaces.auth import AuthResponse, MeAuthResponse
from actions import auth_actions, user_actions
from database import SessionLocal, get_db

auth_router = APIRouter()

####
# Note: As the auth part is not mentioned in the API list, only the necessary endpoints will be created and endpoints like `forget password` are dropped.
###


@auth_router.post("/register", response_model=AuthResponse)
def register(user: UserCreate, db: SessionLocal = Depends(get_db)):
    if len(user.password) < 6:
        raise HTTPException(status_code=400, detail="Password is too short")
    existing_user = user_actions.get_user_by_email(email=user.email, db=db)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists.")
    created_user = user_actions.create_user(db, user)
    if created_user == None or created_user.email == None:
        raise HTTPException(status_code=400, detail="Error during user registration.")
    jwt_token = auth_actions.generateJWT(created_user.id, created_user.email)

    return {
        "email": user.email,
        "token": jwt_token,
        "message": "Registration was successful. you can login using the passwords you",
    }


@auth_router.post("/login", response_model=AuthResponse)
def login(user: UserLogin, db: SessionLocal = Depends(get_db)):
    existing_user = user_actions.check_user_password(db, user.email, user.password)
    if existing_user:
        jwt_token = auth_actions.generateJWT(existing_user.id, existing_user.email)
        return {
            "email": existing_user.email,
            "token": jwt_token,
            "message": "You are logged in successfully.",
        }
    else:
        raise HTTPException(status_code=400, detail="Username or password is wrong")


@auth_router.get("/", response_model=MeAuthResponse)
def me(current_user: Annotated[str, Depends(auth_actions.get_current_user)]):
    return {"message": "Welcome " + current_user["email"]}
