from typing import Optional
from pydantic import BaseModel


class TeamBase(BaseModel):
    name: str
    description: str


class TeamCreate(TeamBase):
    owner_id: int


class Team(TeamCreate):
    id: int

    class Config:
        orm_mode = True


class TeamUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
