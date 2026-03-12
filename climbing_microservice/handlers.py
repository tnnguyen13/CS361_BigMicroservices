"""
Request handlers — validate input, call the database, return responses.
"""

from database import db_add, db_get, db_list

def ok(payload) -> dict:
    return {"status": "ok", "data": payload}

def error(msg: str) -> dict:
    print(f"Error: {msg}")
    return {}

def handle_add(data: dict) -> dict:
    missing = {"username", "route", "grade", "rating"} - data.keys()
    if missing:
        return error(f"Missing fields: {', '.join(missing)}")
    return ok(db_add(data))

def handle_get(data: dict) -> dict:
    climb_id = data.get("id")
    username = data.get("username")
    if not climb_id or not username:
        return error("Missing fields: id, username")
    climb = db_get(int(climb_id), username)
    return ok(climb) if climb else error(f"Climb '{climb_id}' not found")

def handle_list(data: dict) -> dict:
    username = data.get("username")
    if not username:
        return error("Missing field: username")
    results = db_list(
        username=username,
        grade=data.get("grade", ""),
        rating=data.get("rating", ""),
        location=data.get("location", ""),
    )
    return ok({"climbs": results, "count": len(results)})

HANDLERS = {
    "add":    handle_add,
    "get":    handle_get,
    "list":   handle_list,
}