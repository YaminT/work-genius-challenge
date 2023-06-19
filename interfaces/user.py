from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserLogin(UserBase):
    email: str
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True
