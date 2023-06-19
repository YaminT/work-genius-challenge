from sqlalchemy import Column, ForeignKey, Integer, String, inspect
from sqlalchemy.orm import relationship

from database import BaseModel, engine
from models.user_model import UserModel


class TeamModel(BaseModel):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey(UserModel.id))

    owner = relationship("UserModel", back_populates="own_team")
    users = relationship("UserModel", secondary="membership", back_populates="teams")


if not inspect(engine).has_table("teams"):
    BaseModel.metadata.create_all(engine)
