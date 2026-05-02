import os
import uuid
from supabase import create_client, Client

SUPABASE_URL = "https://wtzxkzepcorpdawaprxc.supabase.co"

_sb: Client | None = None


def _client() -> Client:
    global _sb
    if _sb is None:
        _sb = create_client(SUPABASE_URL, os.environ["SUPABASE_KEY"])
    return _sb


def load_data() -> dict:
    sb = _client()
    initiatives = sb.table("initiatives").select("*").order("week").execute().data
    goals = sb.table("goals").select("*").order("priority").execute().data

    if not initiatives:
        initiatives = _default_initiatives()
        sb.table("initiatives").insert(initiatives).execute()

    return {"initiatives": initiatives, "goals": goals}


def save_data(data: dict) -> None:
    pass  # each mutation function writes directly to Supabase


def update_initiative(data: dict, initiative_id: str, **kwargs) -> dict:
    _client().table("initiatives").update(kwargs).eq("id", initiative_id).execute()
    for item in data["initiatives"]:
        if item["id"] == initiative_id:
            item.update(kwargs)
            break
    return data


def add_goal(data: dict, title: str, description: str, priority: int) -> dict:
    goal = {
        "id": str(uuid.uuid4()),
        "title": title,
        "description": description,
        "priority": priority,
        "status": "active",
    }
    _client().table("goals").insert(goal).execute()
    data["goals"].append(goal)
    return data


def update_goal(data: dict, goal_id: str, **kwargs) -> dict:
    _client().table("goals").update(kwargs).eq("id", goal_id).execute()
    for goal in data["goals"]:
        if goal["id"] == goal_id:
            goal.update(kwargs)
            break
    return data


def delete_goal(data: dict, goal_id: str) -> dict:
    _client().table("goals").delete().eq("id", goal_id).execute()
    data["goals"] = [g for g in data["goals"] if g["id"] != goal_id]
    return data


def get_initiative_by_id(data: dict, initiative_id: str) -> dict | None:
    for item in data["initiatives"]:
        if item["id"] == initiative_id:
            return item
    return None


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
