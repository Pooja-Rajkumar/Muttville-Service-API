import sqlite3
from datetime import datetime
import pytest
from database.database import get_behavior_events_for_dog, save_behavior_event
from models.behavior_event import BehaviorConcern, EventSource
from models.behavior_modification_event import MedicationBehaviorEvent
from models.foster_behavior_event import (
    FosterBehaviorEvent,
    LeashBehaviorType,
    SleepBehaviorType,
)

@pytest.fixture
def test_db(tmp_path, monkeypatch):
    db_path = tmp_path / "test_muttville.db"

    def get_test_db_connection():
        connection = sqlite3.connect(db_path)
        connection.row_factory = sqlite3.Row
        return connection

    monkeypatch.setattr(
        "database.database.get_db_connection",
        get_test_db_connection,
    )

    connection = get_test_db_connection()

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

    connection.commit()
    connection.close()

def make_foster_event() -> FosterBehaviorEvent:
    return FosterBehaviorEvent(
        timestamp=datetime(2026, 4, 17, 18, 10, 29),
        inputted_by="Kaitlyn Wain",
        event_id="abc-123",
        dog_name="Cece",
        source=EventSource.GS_FOSTER_QUESTIONNAIRE,
        concerns=[BehaviorConcern.HANDLING_SENSITIVITY],
        summary="Cece is settling in well.",
        sleep_behavior=[SleepBehaviorType.DOG_BED],
        leash_behavior=[
            LeashBehaviorType.MEANDERS,
            LeashBehaviorType.WALKS_BRISKLY,
        ],
    )


def make_medication_event() -> MedicationBehaviorEvent:
    return MedicationBehaviorEvent(
        timestamp=datetime(2026, 4, 2, 10, 47, 20),
        inputted_by="Hannah",
        event_id="hannah-cece",
        dog_name="Cece",
        source=EventSource.GS_MEDICATIONS,
        concerns=[BehaviorConcern.OTHER],
        summary="Frequent whining and anxious pacing.",
        medication="trazodone 14 day trial",
        location="HQ",
    )


def test_saves_multiple_events_for_same_dog(test_db):
    foster_event = make_foster_event()
    medication_event = make_medication_event()

    save_behavior_event(foster_event)
    save_behavior_event(medication_event)

    events = get_behavior_events_for_dog("Cece")

    assert len(events) == 2
    assert isinstance(events[0], FosterBehaviorEvent)
    assert isinstance(events[1], MedicationBehaviorEvent)


def test_foster_event_round_trip(test_db):
    original = make_foster_event()

    save_behavior_event(original)

    events = get_behavior_events_for_dog("Cece")

    assert len(events) == 1

    saved = events[0]

    assert isinstance(saved, FosterBehaviorEvent)
    assert saved.dog_name == original.dog_name
    assert saved.timestamp == original.timestamp
    assert saved.inputted_by == original.inputted_by
    assert saved.source == original.source
    assert saved.concerns == original.concerns
    assert saved.summary == original.summary
    assert saved.sleep_behavior == original.sleep_behavior
    assert saved.leash_behavior == original.leash_behavior


def test_medication_event_round_trip(test_db):
    original = make_medication_event()

    save_behavior_event(original)

    events = get_behavior_events_for_dog("Cece")

    assert len(events) == 1

    saved = events[0]

    assert isinstance(saved, MedicationBehaviorEvent)
    assert saved.dog_name == original.dog_name
    assert saved.timestamp == original.timestamp
    assert saved.source == original.source
    assert saved.concerns == original.concerns
    assert saved.medication == original.medication
    assert saved.location == original.location


def test_same_event_is_not_saved_twice(test_db):
    """
    This assumes save_behavior_event() checks for duplicates
    before inserting.
    """
    event = make_foster_event()

    save_behavior_event(event)
    save_behavior_event(event)

    events = get_behavior_events_for_dog("Cece")

    assert len(events) == 1

def test_save_behavior_event_inserts_and_updates(test_db):
    original_event = make_foster_event()

    save_behavior_event(original_event)

    events = get_behavior_events_for_dog("Cece")

    assert len(events) == 1
    assert events[0].summary == original_event.summary

    updated_event = make_foster_event()
    updated_event.summary = "Cece is doing much better now."

    save_behavior_event(updated_event)

    events = get_behavior_events_for_dog("Cece")

    assert len(events) == 1
    assert events[0].summary == "Cece is doing much better now."