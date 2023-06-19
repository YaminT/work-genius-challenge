import pytest
from actions.membership_actions import (
    add_user_to_team,
    find_all_membership,
    find_membership,
    remove_user_from_team,
)
from actions.teams_actions import create_team, delete_team
from database import get_db
from interfaces.membership import MembershipBase
from interfaces.team import TeamBase
from sqlalchemy.orm.collections import InstrumentedList

sample_team = {"name": "team-test-new", "description": "desc-new"}


def prepare_data():
    db = next(get_db())
    team_request = TeamBase(
        name=sample_team["name"], description=sample_team["description"]
    )
    created_team = create_team(team=team_request, user_id=1, db=db)
    return created_team.id


def remove_data(team_id: int):
    db = next(get_db())
    team_request = TeamBase(
        name=sample_team["name"], description=sample_team["description"]
    )
    delete_team(team_id=team_id, user_id=1, db=db)


def test_add_user_to_team_wrong_owner():
    db = next(get_db())
    team_id = prepare_data()
    membership_request = MembershipBase(team_id=team_id, user_id=-1)
    with pytest.raises(Exception) as e:
        add_user_to_team(membership_request=membership_request, owner_user_id=1, db=db)
    assert e != None
    remove_data(team_id)


def test_add_user_to_team_wrong_team():
    db = next(get_db())
    membership_request = MembershipBase(team_id=-1, user_id=1)
    with pytest.raises(Exception) as e:
        add_user_to_team(membership_request=membership_request, owner_user_id=1, db=db)
    assert e != None


def test_add_user_to_team():
    db = next(get_db())
    team_id = prepare_data()
    membership_request = MembershipBase(team_id=team_id, user_id=2)
    team_db = add_user_to_team(
        membership_request=membership_request, owner_user_id=1, db=db
    )
    assert team_db != None


def test_find_all_membership():
    db = next(get_db())
    membership_list = find_all_membership(user_id=2, db=db)
    assert membership_list != None
    www = type(membership_list)
    assert type(membership_list) == InstrumentedList
    assert len(membership_list) == 1


def test_find_membership():
    db = next(get_db())
    membership = find_membership(team_id=1, user_id=2, db=db)
    assert membership != None


def test_find_membership_wrong_user():
    db = next(get_db())
    membership = find_membership(team_id=1, user_id=-1, db=db)
    assert membership == None


def test_remove_user_from_team_wrong_user():
    db = next(get_db())
    with pytest.raises(Exception) as e:
        remove_user_from_team(team_id=1, user_id=-1, owner_user_id=1, db=db)
    assert e != None


def test_remove_user_from_team():
    db = next(get_db())
    delete_result = remove_user_from_team(team_id=1, user_id=2, owner_user_id=1, db=db)
    assert delete_result == True


def test_find_all_membership_no_team():
    db = next(get_db())
    membership_list = find_all_membership(user_id=2, db=db)
    assert membership_list != None
    assert type(membership_list) == InstrumentedList
    assert len(membership_list) == 0
