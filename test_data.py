import pytest
import data as data_module
from data import (
    load_data, save_data, update_initiative,
    add_goal, update_goal, delete_goal, get_initiative_by_id,
)


@pytest.fixture(autouse=True)
def isolate_data_file(tmp_path, monkeypatch):
    monkeypatch.setattr(data_module, "DATA_FILE", tmp_path / "tracker_data.json")


def test_load_data_creates_10_initiatives():
    data = load_data()
    assert len(data["initiatives"]) == 10


def test_load_data_weeks_numbered_1_to_10():
    data = load_data()
    assert [i["week"] for i in data["initiatives"]] == list(range(1, 11))


def test_load_data_empty_goals():
    data = load_data()
    assert data["goals"] == []


def test_load_data_default_status_not_started():
    data = load_data()
    assert all(i["status"] == "not_started" for i in data["initiatives"])


def test_save_and_load_roundtrip():
    data = load_data()
    data["initiatives"][0]["title"] = "Custom Title"
    save_data(data)
    assert load_data()["initiatives"][0]["title"] == "Custom Title"


def test_update_initiative_title_and_status():
    data = load_data()
    init_id = data["initiatives"][0]["id"]
    update_initiative(data, init_id, title="New Title", status="in_progress")
    assert data["initiatives"][0]["title"] == "New Title"
    assert data["initiatives"][0]["status"] == "in_progress"


def test_update_initiative_unknown_id_leaves_data_unchanged():
    data = load_data()
    titles_before = [i["title"] for i in data["initiatives"]]
    update_initiative(data, "nonexistent", title="X")
    assert [i["title"] for i in data["initiatives"]] == titles_before


def test_update_initiative_time_and_dates():
    data = load_data()
    init_id = data["initiatives"][2]["id"]
    update_initiative(data, init_id, time_spent_hours=3.5, start_date="2026-04-01", end_date="2026-04-07")
    updated = get_initiative_by_id(data, init_id)
    assert updated["time_spent_hours"] == 3.5
    assert updated["start_date"] == "2026-04-01"
    assert updated["end_date"] == "2026-04-07"


def test_add_goal_fields():
    data = load_data()
    add_goal(data, "Lose weight", "Exercise daily", 1)
    goal = data["goals"][0]
    assert goal["title"] == "Lose weight"
    assert goal["description"] == "Exercise daily"
    assert goal["priority"] == 1
    assert goal["status"] == "active"
    assert "id" in goal


def test_add_multiple_goals():
    data = load_data()
    add_goal(data, "Goal A", "", 2)
    add_goal(data, "Goal B", "", 1)
    assert len(data["goals"]) == 2


def test_update_goal_title_and_priority():
    data = load_data()
    add_goal(data, "Original", "", 3)
    goal_id = data["goals"][0]["id"]
    update_goal(data, goal_id, title="Updated", priority=1)
    assert data["goals"][0]["title"] == "Updated"
    assert data["goals"][0]["priority"] == 1


def test_update_goal_status():
    data = load_data()
    add_goal(data, "G", "", 1)
    goal_id = data["goals"][0]["id"]
    update_goal(data, goal_id, status="completed")
    assert data["goals"][0]["status"] == "completed"


def test_delete_goal_removes_it():
    data = load_data()
    add_goal(data, "To delete", "", 1)
    goal_id = data["goals"][0]["id"]
    delete_goal(data, goal_id)
    assert len(data["goals"]) == 0


def test_delete_goal_only_removes_target():
    data = load_data()
    add_goal(data, "Keep", "", 1)
    add_goal(data, "Remove", "", 2)
    goal_id = data["goals"][1]["id"]
    delete_goal(data, goal_id)
    assert len(data["goals"]) == 1
    assert data["goals"][0]["title"] == "Keep"


def test_get_initiative_by_id_returns_correct_week():
    data = load_data()
    init_id = data["initiatives"][4]["id"]
    result = get_initiative_by_id(data, init_id)
    assert result is not None
    assert result["week"] == 5


def test_get_initiative_by_id_not_found_returns_none():
    data = load_data()
    assert get_initiative_by_id(data, "nonexistent") is None
