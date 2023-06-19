from sqlalchemy.orm.collections import InstrumentedList

from models.membership_model import MembershipModel
from models.user_model import UserModel
from actions import teams_actions, user_actions
from database import SessionLocal
from interfaces.membership import Membership, MembershipRequest

def add_user_to_team(
    membership_request: MembershipRequest, owner_user_id: int, db: SessionLocal
) -> Membership:
    # Finding the team:
    if membership_request.team_id != None:
        db_team = teams_actions.get_single_team(
            team_id=membership_request.team_id, user_id=owner_user_id, db=db
        )
    else:
        db_team = teams_actions.existing_team_with_name(
            team_id=membership_request.team_name, user_id=owner_user_id, db=db
        )

    # Finding the user:
    if membership_request.user_id != None:
        db_user = user_actions.get_user_by_id(id=membership_request.user_id, db=db)
    else:
        db_user = user_actions.get_user_by_email(
            email=membership_request.user_email, db=db
        )
    if db_user == None:
        raise Exception("User not found")

    if db_team == None:
        raise Exception("The team does not exists or it does not belong to this user.")
    previous_membership = find_membership(team_id=db_team.id, user_id=db_user.id, db=db)
    if previous_membership:
        raise Exception("User is already a member of this team.")

    db_membership = MembershipModel(
        team_id=db_team.id, user_id=membership_request.user_id
    )
    db.add(db_membership)
    db.commit()
    db.refresh(db_team)
    return db_team


def list_of_users(db: SessionLocal):
    return db.query(UserModel).all()


def find_all_membership(user_id: int, db: SessionLocal) -> list[MembershipModel]:
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user != None and user.teams != None:
        return user.teams
    empty_response: InstrumentedList = InstrumentedList()
    return empty_response


def find_membership(team_id: int, user_id: int, db: SessionLocal) -> MembershipModel:
    return (
        db.query(MembershipModel)
        .where(
            (MembershipModel.team_id == team_id) & (MembershipModel.user_id == user_id)
        )
        .first()
    )


def remove_user_from_team(
    team_id: int, user_id: int, owner_user_id: int, db: SessionLocal
) -> bool:
    db_team = teams_actions.get_single_team(
        team_id=team_id, user_id=owner_user_id, db=db
    )
    if db_team == None:
        raise Exception("The team does not exists or it does not belong to this user.")
    if db_team.owner_id == user_id:
        raise Exception(
            "The user is the owner of the team. we cannot remove this user."
        )
    db_membership = find_membership(team_id=team_id, user_id=user_id, db=db)
    if db_membership == None:
        raise Exception("The user is not a member of this team.")
    db.delete(db_membership)
    db.commit()
    return True
