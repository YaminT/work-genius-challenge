from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException

from interfaces.membership import MembershipRequest
from database import SessionLocal, get_db
from actions.auth_actions import get_current_user
from actions import membership_actions, user_actions

membership_router = APIRouter()


@membership_router.get("/")
def get_current_user_teams(
    current_user: Annotated[str, Depends(get_current_user)],
    db: SessionLocal = Depends(get_db),
):
    return membership_actions.find_all_membership(user_id=current_user["id"], db=db)


@membership_router.get("/user/{user_id}")
def get_current_user_teams(
    user_id: int,
    current_user: Annotated[str, Depends(get_current_user)],
    db: SessionLocal = Depends(get_db),
):
    db_user = user_actions.get_user_by_id(id=user_id, db=db)
    if db_user == None:
        raise HTTPException(status_code=404, detail="User not found")
    return membership_actions.find_all_membership(user_id=user_id, db=db)


# It is also possible to pass data like "/user/{user_id}/{team_id}".


@membership_router.post("/")
def add_user_to_team(
    membership_request: MembershipRequest,
    current_user: Annotated[str, Depends(get_current_user)],
    db: SessionLocal = Depends(get_db),
):
    try:
        if membership_request.team_id == None and membership_request.team_name == None:
            raise HTTPException(status_code=400, detail="Team is not provided")
        if membership_request.user_email == None and membership_request.user_id == None:
            raise HTTPException(status_code=400, detail="User details are not provided")
        add_result = membership_actions.add_user_to_team(
            membership_request=membership_request,
            owner_user_id=current_user["id"],
            db=db,
        )
        if add_result:
            return {"message": "User is added to the site"}
        else:
            raise Exception("Cannot add user to the team")
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error))


@membership_router.delete("/user/{user_id}/team/{team_id}")
def remove_user_from_team(
    user_id: int,
    team_id: int,
    current_user: Annotated[str, Depends(get_current_user)],
    db: SessionLocal = Depends(get_db),
):
    try:
        delete_result = membership_actions.remove_user_from_team(
            team_id=team_id, user_id=user_id, owner_user_id=current_user["id"], db=db
        )
        if delete_result:
            return {"message": "User is removed from the team."}
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error))


@membership_router.get("/users")
def list_of_users(
    current_user: Annotated[str, Depends(get_current_user)],
    db: SessionLocal = Depends(get_db),
):
    try:
        return membership_actions.list_of_users(db=db)
    except:
        raise HTTPException(status_code=401, detail="No access")
