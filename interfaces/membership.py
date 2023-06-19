from pydantic import BaseModel


class MembershipBase(BaseModel):
    team_id: int
    user_id: int


class MembershipRequest(BaseModel):
    team_id: int | None = None
    user_id: int | None = None
    team_name: int | None = None
    user_email: int | None = None


class Membership(MembershipBase):
    id: int

    class Config:
        orm_mode = True
