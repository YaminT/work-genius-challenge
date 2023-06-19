from sqlalchemy import Column, ForeignKey, Integer, inspect
from database import BaseModel, engine
from models.team_model import TeamModel
from models.user_model import UserModel


class MembershipModel(BaseModel):
    __tablename__ = "membership"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(Integer, ForeignKey(UserModel.id))
    team_id = Column(Integer, ForeignKey(TeamModel.id))


if not inspect(engine).has_table("membership"):
    BaseModel.metadata.create_all(engine)
