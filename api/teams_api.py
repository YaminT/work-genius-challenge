from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException

from interfaces.team import TeamBase, TeamUpdate
from actions import teams_actions as team_actions
from actions.auth_actions import get_current_user
from database import SessionLocal, get_db

teams_router = APIRouter()


@teams_router.post("/")
def create_new_team(
    team: TeamBase,
    current_user: Annotated[str, Depends(get_current_user)],
    db: SessionLocal = Depends(get_db),
):
    try:
        return team_actions.create_team(team=team, user_id=current_user["id"], db=db)
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error))


@teams_router.get("/")
def get_all_teams(
    current_user: Annotated[str, Depends(get_current_user)],
    db: SessionLocal = Depends(get_db),
):
    return team_actions.get_teams(user_id=current_user["id"], db=db)


@teams_router.get("/{team_id}")
def get_team(
    team_id: int,
    current_user: Annotated[str, Depends(get_current_user)],
    db: SessionLocal = Depends(get_db),
):
    return team_actions.get_single_team(
        team_id=team_id, user_id=current_user["id"], db=db
    )


# Note: PATCH method is used instead of PUT method because we allow users to partially update the model.


@teams_router.patch("/{team_id}")
def edit_team(
    team_id: int,
    team: TeamUpdate,
    current_user: Annotated[str, Depends(get_current_user)],
    db: SessionLocal = Depends(get_db),
):
    return team_actions.edit_team(
        team_id=team_id, team_update_model=team, user_id=current_user["id"], db=db
    )


@teams_router.delete("/{team_id}")
def delete_team(
    team_id,
    current_user: Annotated[str, Depends(get_current_user)],
    db: SessionLocal = Depends(get_db),
):
    delete_result = team_actions.delete_team(
        team_id=team_id, user_id=current_user["id"], db=db
    )
    if delete_result:
        return {"message": "Item is deleted successfully."}
    raise HTTPException(status_code=400, detail="Item does not exist.")
