from typing import List
from fastapi import HTTPException
from sqlalchemy import exc
from interfaces.membership import MembershipBase

from interfaces.team import TeamBase, TeamUpdate
from models.team_model import TeamModel
from tools.constants import SHOULD_ADD_USER_TO_OWN_TEAM
from database import SessionLocal
from actions import membership_actions as membership_actions

# TODO: add pagination


def get_teams(user_id: int, db: SessionLocal) -> List[TeamModel]:
    return db.query(TeamModel).where(TeamModel.owner_id == user_id).all()


def get_single_team(team_id: int, user_id: int, db: SessionLocal) -> TeamModel:
    team_db = (
        db.query(TeamModel)
        .where((TeamModel.id == team_id) & (TeamModel.owner_id == user_id))
        .first()
    )
    if team_db:
        return team_db


def existing_team_with_name(team_name: str, db: SessionLocal) -> bool:
    team_db = db.query(TeamModel).where(TeamModel.name == team_name).first()
    if team_db:
        return team_db
    return None


def create_team(team: TeamBase, user_id: int, db: SessionLocal) -> TeamModel:
    try:
        if existing_team_with_name(team_name=team.name, db=db) != None:
            raise Exception("Team name already exists")
        team_db = TeamModel(
            name=team.name, description=team.description, owner_id=user_id
        )
        db.add(team_db)
        if SHOULD_ADD_USER_TO_OWN_TEAM:
            db.flush()
            print(team_db.id)
            membership_request: MembershipBase = MembershipBase(
                team_id=team_db.id, user_id=user_id
            )
            membership_actions.add_user_to_team(
                membership_request=membership_request, owner_user_id=user_id, db=db
            )
        db.commit()
        db.refresh(team_db)
        return team_db
    except exc.SQLAlchemyError as error:
        print(error)
        return None


def edit_team(
    team_id: int, team_update_model: TeamUpdate, user_id: int, db: SessionLocal
) -> TeamModel:
    team_db = get_single_team(team_id, user_id, db)
    if team_db:
        # TODO: check if a loop would be better to update values
        # or: db.query(TeamModel).where(TeamModel.owner_id == user_id).update(**team_update_model.dict())
        if team_update_model.name:
            team_db.name = team_update_model.name
        if team_update_model.description:
            team_db.description = team_update_model.description
        db.commit()
        db.refresh(team_db)
        return team_db
    else:
        raise HTTPException(status_code=400, detail="team does not exist")


def delete_team(team_id: int, user_id: int, db: SessionLocal) -> bool:
    team_db = get_single_team(team_id, user_id, db)
    if team_db:
        db.delete(team_db)
        db.commit()
        return True
    return False
