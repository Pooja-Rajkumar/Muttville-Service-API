import json
import sqlite3

from database.deserialize_behavior_events import deserialize_behavior_event
from models.behavior_event import BehaviorEvent


def get_db_connection():
    connection = sqlite3.connect("muttville.db")
    connection.row_factory = sqlite3.Row
    return connection


def create_tables():
    connection = get_db_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS behavior_events (
            id INTEGER PRIMARY KEY,
            event_type TEXT NOT NULL,
            occurred_at TEXT NOT NULL,
            inputted_by TEXT,
            dog_name TEXT NOT NULL,
            source TEXT NOT NULL,
            concerns TEXT NOT NULL,
            summary TEXT NOT NULL,
            event_data TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()

def get_behavior_events():
    connection = get_db_connection()

    rows = connection.execute(
        "SELECT * FROM behavior_events"
    ).fetchall()

    connection.close()
    return rows


def save_behavior_event(event: BehaviorEvent):
    if(behavior_event_exists(event)):
        return 
    connection = get_db_connection()

    concerns = []

    for concern in event.concerns:
        concerns.append(concern.value)

    event_data = event.model_dump(
        mode="json",
        exclude={
            "occurred_at_display",
            "occurred_at",
            "inputted_by",
            "dog_name",
            "source",
            "concerns",
            "summary",
            "raw_data",
        },
    )
    connection.execute(
        """
        INSERT INTO behavior_events (
            event_type,
            occurred_at,
            inputted_by,
            dog_name,
            source,
            concerns,
            summary,
            event_data
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            event.__class__.__name__,
            event.occurred_at.isoformat(),
            event.inputted_by,
            event.dog_name,
            event.source.value,
            json.dumps(concerns),
            event.summary,
            json.dumps(event_data),
        ),
    )
    print("Saved event:", event.dog_name, event.source.value)
    connection.commit()
    connection.close()


def get_behavior_events():
    connection = get_db_connection()

    rows = connection.execute(
        """
        SELECT *
        FROM behavior_events
        ORDER BY occurred_at DESC
        """
    ).fetchall()

    connection.close()

    return [dict(row) for row in rows]


def get_behavior_events_for_dog(
    dog_name: str,
) -> list[BehaviorEvent]:
    connection = get_db_connection()

    rows = connection.execute(
        """
        SELECT *
        FROM behavior_events
        WHERE dog_name = ?
        ORDER BY occurred_at DESC
        """,
        (dog_name,),
    ).fetchall()
    connection.close()
    events = []
    for row in rows:
        events.append(deserialize_behavior_event(row))
    return events

def behavior_event_exists(event: BehaviorEvent) -> bool:
    connection = get_db_connection()

    row = connection.execute(
        """
        SELECT id
        FROM behavior_events
        WHERE source = ?
        AND dog_name = ?
        AND occurred_at = ?
        AND summary = ?
        """,
        (
            event.source.value,
            event.dog_name,
            event.occurred_at.isoformat(),
            event.summary,
        ),
    ).fetchone()

    connection.close()

    return (row is not None)