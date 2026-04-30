import json
import uuid
from pathlib import Path

DATA_FILE = Path("tracker_data.json")


def load_data() -> dict:
    if not DATA_FILE.exists():
        return {"initiatives": _default_initiatives(), "goals": []}
    return json.loads(DATA_FILE.read_text())


def save_data(data: dict) -> None:
    DATA_FILE.write_text(json.dumps(data, indent=2))


def _default_initiatives() -> list:
    return [
        {
            "id": str(uuid.uuid4()),
            "week": i,
            "title": f"Week {i} Initiative",
            "start_date": "",
            "end_date": "",
            "time_spent_hours": 0.0,
            "summary": "",
            "status": "not_started",
        }
        for i in range(1, 11)
    ]


def update_initiative(data: dict, initiative_id: str, **kwargs) -> dict:
    for item in data["initiatives"]:
        if item["id"] == initiative_id:
            item.update(kwargs)
            break
    return data


def add_goal(data: dict, title: str, description: str, priority: int) -> dict:
    data["goals"].append({
        "id": str(uuid.uuid4()),
        "title": title,
        "description": description,
        "priority": priority,
        "status": "active",
    })
    return data


def update_goal(data: dict, goal_id: str, **kwargs) -> dict:
    for goal in data["goals"]:
        if goal["id"] == goal_id:
            goal.update(kwargs)
            break
    return data


def delete_goal(data: dict, goal_id: str) -> dict:
    data["goals"] = [g for g in data["goals"] if g["id"] != goal_id]
    return data


def get_initiative_by_id(data: dict, initiative_id: str) -> dict | None:
    for item in data["initiatives"]:
        if item["id"] == initiative_id:
            return item
    return None
