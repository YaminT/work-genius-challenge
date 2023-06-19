from typing import List
import pytest
from actions.teams_actions import (
    get_teams,
    create_team,
    delete_team,
    edit_team,
    get_single_team,
    existing_team_with_name,
)
from database import get_db
from interfaces.team import TeamBase, TeamUpdate
from models.team_model import TeamModel

sample_team = {"name": "teamtest", "description": "desc"}


def test_create_team():
    db = next(get_db())
    team_request = TeamBase(
        name=sample_team["name"], description=sample_team["description"]
    )
    created_team = create_team(team=team_request, user_id=1, db=db)
    assert created_team != None
    assert created_team.id != None
    sample_team["id"] = created_team.id
    assert created_team.name != None
    assert created_team.description != None
    assert created_team.owner_id != None


def test_create_team_name_dup():
    db = next(get_db())
    team_request = TeamBase(
        name=sample_team["name"], description=sample_team["description"]
    )
    with pytest.raises(Exception) as e:
        create_team(team=team_request, user_id=1, db=db)
    assert e != None


def test_get_teams():
    db = next(get_db())
    teams = get_teams(user_id=1, db=db)
    assert type(teams) == list
    assert len(teams) == 1


def test_get_single_team():
    db = next(get_db())
    existing_team = get_single_team(team_id=sample_team["id"], user_id=1, db=db)
    assert existing_team != None
    assert existing_team.name != None


def test_get_single_team_not_found():
    db = next(get_db())
    existing_team = get_single_team(team_id=-1, user_id=1, db=db)
    assert existing_team == None


def test_get_single_team_wrong_owner():
    db = next(get_db())
    existing_team = get_single_team(team_id=sample_team["id"], user_id=-1, db=db)
    assert existing_team == None


def test_is_team_name_exists_not_found():
    db = next(get_db())
    is_exist = existing_team_with_name(team_name=sample_team["name"], db=db)
    assert is_exist == None


def test_is_team_name_exists_not_found():
    db = next(get_db())
    is_exist = existing_team_with_name(team_name=sample_team["name"], db=db)
    assert is_exist != None


def test_edit_team():
    db = next(get_db())
    update_model = TeamUpdate(name="new name", description="new desc")
    updated_team = edit_team(
        team_id=sample_team["id"], team_update_model=update_model, user_id=1, db=db
    )
    assert updated_team.name == "new name"
    assert updated_team.description == "new desc"


def test_delete_team_not_exist():
    db = next(get_db())
    delete_result = delete_team(team_id=-1, user_id=1, db=db)
    assert delete_result == False


def test_delete_team_wrong_owner():
    db = next(get_db())
    delete_result = delete_team(team_id=sample_team["id"], user_id=2, db=db)
    assert delete_result == False


def test_delete_team():
    db = next(get_db())
    delete_result = delete_team(team_id=sample_team["id"], user_id=1, db=db)
    assert delete_result == True
