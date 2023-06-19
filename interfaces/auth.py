from pydantic import BaseModel


class MeAuthResponse(BaseModel):
    message: str


class AuthResponse(MeAuthResponse):
    email: str
    token: str
