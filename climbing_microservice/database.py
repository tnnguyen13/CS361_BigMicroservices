"""
Database set up and maintenance using sqlalchemy.
"""

from datetime import datetime, date
from sqlalchemy import (
    create_engine, MetaData, Table, Column,
    Integer, String, Text, insert, select
)

engine = create_engine("sqlite:///climbs.db", echo=False)
metadata = MetaData()

climbs_table = Table("climbs", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("username", String,  nullable=False, default="default_user"),
    Column("route", String,  nullable=False),
    Column("grade", String,  nullable=False),
    Column("rating", Integer,  nullable=False),
    Column("location", String,  default=""),
    Column("attempts", Integer, default=1),
    Column("notes", Text,    default=""),
    Column("date", String),
    Column("created_at", String),
)

def init_db():
    metadata.create_all(engine)

def row_to_dict(row) -> dict:
    return dict(row._mapping)

def db_add(data: dict) -> dict:
    entry = {
        "username":   data["username"],
        "route":      data["route"],
        "grade":      data["grade"],
        "rating":      data["rating"],
        "location":   data.get("location", ""),
        "attempts":   int(data.get("attempts", 1)),
        "notes":      data.get("notes", ""),
        "date":       data.get("date", date.today().isoformat()),
        "created_at": datetime.utcnow().isoformat(),
    }
    with engine.connect() as conn:
        result = conn.execute(insert(climbs_table).values(**entry))
        conn.commit()
        entry["id"] = result.inserted_primary_key[0]
    return entry

def db_get(climb_id: int, username: str):
    with engine.connect() as conn:
        row = conn.execute(
            select(climbs_table).where(
                climbs_table.c.id == climb_id,
                climbs_table.c.username == username,
            )
        ).fetchone()
    return row_to_dict(row) if row else None

def db_list(username: str, grade="", rating="", location="") -> list:
    query = select(climbs_table).where(climbs_table.c.username == username)
    if grade:
        query = query.where(climbs_table.c.grade == grade)
    if rating:
        query = query.where(climbs_table.c.rating == rating)
    if location:
        query = query.where(climbs_table.c.location.ilike(f"%{location}%"))
    with engine.connect() as conn:
        rows = conn.execute(query).fetchall()
    return [row_to_dict(r) for r in rows]