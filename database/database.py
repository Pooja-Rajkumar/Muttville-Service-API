import json
import sqlite3

from database.deserialize_behavior_events import convert_row_to_event
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
            event_id TEXT NOT NULL,
            event_type TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            inputted_by TEXT,
            dog_name TEXT NOT NULL,
            source TEXT NOT NULL,
            concerns TEXT NOT NULL,
            summary TEXT NOT NULL,
            event_data TEXT NOT NULL,

            UNIQUE(source, event_id)
        )
    """)

    connection.execute("""
    CREATE TABLE IF NOT EXISTS google_oauth_states (
        state TEXT PRIMARY KEY
        )
    """)
    connection.commit()
    connection.close()

def save_google_oauth_state(state: str):
    connection = get_db_connection()

    connection.execute(
        """
        INSERT INTO google_oauth_states (state)
        VALUES (?)
        """,
        (state,),
    )

    connection.commit()
    connection.close()

def validate_google_oauth_state(state: str) -> bool:
    connection = get_db_connection()

    row = connection.execute(
        """
        SELECT state
        FROM google_oauth_states
        WHERE state = ?
        """,
        (state,),
    ).fetchone()

    if row is None:
        connection.close()
        return False

    connection.execute(
        """
        DELETE FROM google_oauth_states
        WHERE state = ?
        """,
        (state,),
    )

    connection.commit()
    connection.close()

    return True

def get_all_behavior_events():
    connection = get_db_connection()
    rows = connection.execute(
        """
        SELECT *
        FROM behavior_events
        ORDER BY timestamp DESC
        """
    ).fetchall()
    connection.close()
    events = []
    for row in rows:
        events.append(convert_row_to_event(row))
    return events

def behavior_event_changed(
    existing_event: BehaviorEvent,
    new_event: BehaviorEvent,
) -> bool:
    return existing_event != new_event

def get_behavior_events_for_dog(
    dog_name: str,
) -> list[BehaviorEvent]:
    connection = get_db_connection()
    rows = connection.execute(
        """
        SELECT *
        FROM behavior_events
        WHERE dog_name = ?
        ORDER BY timestamp DESC
        """,
        (dog_name,),
    ).fetchall()
    connection.close()
    events = []
    for row in rows:
        events.append(convert_row_to_event(row))
    return events

def get_existing_behavior_event(event: BehaviorEvent):
    connection = get_db_connection()

    row = connection.execute(
        """
        SELECT *
        FROM behavior_events
        WHERE source = ?
        AND event_id = ?
        """,
        (
            event.source.value,
            event.event_id,
        ),
    ).fetchone()

    connection.close()

    return row


def save_behavior_event(event: BehaviorEvent):
    existing_row = get_existing_behavior_event(event) # will be none if not in table 
    if existing_row:
        print("Entry already exists for event", event)
        existing_event = convert_row_to_event(existing_row)
        if existing_event != event: # data has been updated
            print("Updating behavior event since data has been changed...")
            update_behavior_event(event)
        else:
            print("Duplicate entry, skipping...")
    else: 
        print("Creating new db entry...")
        # the event does not exist yet, so add it 
        insert_behavior_event(event)

def insert_behavior_event(event: BehaviorEvent):
    connection = get_db_connection()

    concerns_json = json.dumps(
        [concern.value for concern in event.concerns]
    )

    event_data = event.model_dump(
        mode="json",
        exclude={
            "event_id",
            "timestamp",
            "timestamp_display",
            "inputted_by",
            "dog_name",
            "source",
            "concerns",
            "summary",
        },
    )

    event_data_json = json.dumps(event_data)

    connection.execute(
        """
        INSERT INTO behavior_events (
            event_id,
            event_type,
            timestamp,
            inputted_by,
            dog_name,
            source,
            concerns,
            summary,
            event_data
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            event.event_id,
            event.__class__.__name__,
            event.timestamp.isoformat(),
            event.inputted_by,
            event.dog_name,
            event.source.value,
            concerns_json,
            event.summary,
            event_data_json,
        ),
    )

    connection.commit()
    connection.close()

def update_behavior_event(event: BehaviorEvent):
    connection = get_db_connection()

    concerns_json = json.dumps(
        [concern.value for concern in event.concerns]
    )

    event_data = event.model_dump(
        mode="json",
        exclude={
            "event_id",
            "timestamp",
            "timestamp_display",
            "inputted_by",
            "dog_name",
            "source",
            "concerns",
            "summary",
        },
    )

    event_data_json = json.dumps(event_data)

    connection.execute(
        """
        UPDATE behavior_events
        SET
            event_type = ?,
            timestamp = ?,
            inputted_by = ?,
            dog_name = ?,
            concerns = ?,
            summary = ?,
            event_data = ?
        WHERE source = ?
        AND event_id = ?
        """,
        (
            event.__class__.__name__,
            event.timestamp.isoformat(),
            event.inputted_by,
            event.dog_name,
            concerns_json,
            event.summary,
            event_data_json,
            event.source.value,
            event.event_id,
        ),
    )

    connection.commit()
    connection.close()