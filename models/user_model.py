from sqlalchemy.orm import relationship, deferred
from sqlalchemy import Column, Integer, String, inspect

from database import BaseModel, engine

class UserModel(BaseModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = deferred(Column(String, nullable=False))

    own_team = relationship("TeamModel", back_populates="owner")
    teams = relationship(
        "TeamModel", secondary="membership", back_populates="users", uselist=True
    )


if not inspect(engine).has_table("users"):
    BaseModel.metadata.create_all(engine)
else:
    print("date")
