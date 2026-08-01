import sqlite3
from datetime import datetime
import pytest
from database.database import get_behavior_events_for_dog, save_behavior_event
from forms.medication_form import create_medication_event
from forms.trainer_form import create_trainer_event
from forms.intake_form import create_intake_event
from forms.foster_form import create_foster_event
from main import store_dog_info
from models.behavior_event import BehaviorConcern, EventSource
from models.behavior_modification_event import MedicationBehaviorEvent, TrainerBehaviorEvent
from models.foster_behavior_event import (
    EngagementBehaviorType,
    EnjoymentBehaviorType,
    FosterBehaviorEvent,
    LeashBehaviorType,
    PottyBehaviorType,
    SleepBehaviorType,
    SoloMuttBehaviorType,
    StairBehaviorType,
)
from models.intake_event import IntakeEvent

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


def test_app_event_is_passed_to_main_and_saved(test_db):
    # These represent the shared values collected in app.py.
    common_event_data = {
        "event_id": "medication-cece-2026-07-31",
        "timestamp": datetime(2026, 7, 31, 14, 30),
        "inputted_by": "Pooja",
        "dog_name": "Cece",
        "source": EventSource.GS_MEDICATIONS,
        "concerns": [BehaviorConcern.SEPARATION_DISTRESS],
        "summary": "Cece was anxious and pacing.",
    }

    # These represent the medication-specific values collected in app.py.
    medication_fields = {
        "medication": "Trazodone",
        "location": "HQ",
    }

    # This is the same helper app.py uses to create the Pydantic model.
    event = create_medication_event(
        common_event_data,
        medication_fields,
    )

    # This is the function app.py calls in main.py.
    store_dog_info(event)

    # Read the event back from the test database.
    saved_events = get_behavior_events_for_dog("Cece")

    assert len(saved_events) == 1

    saved_event = saved_events[0]

    assert isinstance(saved_event, MedicationBehaviorEvent)
    assert saved_event.event_id == "medication-cece-2026-07-31"
    assert saved_event.dog_name == "Cece"
    assert saved_event.inputted_by == "Pooja"
    assert saved_event.timestamp == datetime(2026, 7, 31, 14, 30)
    assert saved_event.source == EventSource.GS_MEDICATIONS
    assert saved_event.concerns == [
        BehaviorConcern.SEPARATION_DISTRESS
    ]
    assert saved_event.summary == "Cece was anxious and pacing."
    assert saved_event.medication == "Trazodone"
    assert saved_event.location == "HQ"

def test_store_and_get_medication_event(test_db):
    common_event_data = {
        "event_id": "medication-cece-2026-07-31",
        "timestamp": datetime(2026, 7, 31, 14, 30),
        "inputted_by": "Pooja",
        "dog_name": "Cece",
        "source": EventSource.GS_MEDICATIONS,
        "concerns": [BehaviorConcern.SEPARATION_DISTRESS],
        "summary": "Cece was anxious and pacing.",
    }

    medication_fields = {
        "medication": "Trazodone",
        "location": "HQ",
    }

    # Same helper used by app.py
    event = create_medication_event(
        common_event_data,
        medication_fields,
    )

    # Same backend entry point used by app.py
    store_dog_info(event)

    saved_events = get_behavior_events_for_dog("Cece")

    assert len(saved_events) == 1

    saved_event = saved_events[0]

    assert isinstance(saved_event, MedicationBehaviorEvent)
    assert saved_event.event_id == "medication-cece-2026-07-31"
    assert saved_event.timestamp == datetime(2026, 7, 31, 14, 30)
    assert saved_event.inputted_by == "Pooja"
    assert saved_event.dog_name == "Cece"
    assert saved_event.source == EventSource.GS_MEDICATIONS
    assert saved_event.concerns == [
        BehaviorConcern.SEPARATION_DISTRESS
    ]
    assert saved_event.summary == "Cece was anxious and pacing."
    assert saved_event.medication == "Trazodone"
    assert saved_event.location == "HQ"

def test_store_and_get_trainer_event(test_db):
    common_event_data = {
        "event_id": "trainer-cece-2026-07-31",
        "timestamp": datetime(2026, 7, 31, 15, 0),
        "inputted_by": "Pooja",
        "dog_name": "Cece",
        "source": EventSource.GS_BEHAVIORAL_OUTREACH_FOSTER,
        "concerns": [BehaviorConcern.HANDLING_SENSITIVITY],
        "summary": "Trainer recommended gradual handling exercises.",
    }

    trainer_fields = {
        "trainer_name": "Lauren",
        "referral_date": "2026-07-30",
        "notes": "Practice short handling sessions with treats.",
    }

    event = create_trainer_event(
        common_event_data,
        trainer_fields,
    )

    store_dog_info(event)

    saved_events = get_behavior_events_for_dog("Cece")

    assert len(saved_events) == 1

    saved_event = saved_events[0]

    assert isinstance(saved_event, TrainerBehaviorEvent)
    assert saved_event.event_id == "trainer-cece-2026-07-31"
    assert saved_event.timestamp == datetime(2026, 7, 31, 15, 0)
    assert saved_event.inputted_by == "Pooja"
    assert saved_event.dog_name == "Cece"
    assert saved_event.source == (
        EventSource.GS_BEHAVIORAL_OUTREACH_FOSTER
    )
    assert saved_event.concerns == [
        BehaviorConcern.HANDLING_SENSITIVITY
    ]
    assert saved_event.summary == (
        "Trainer recommended gradual handling exercises."
    )
    assert saved_event.trainer_name == "Lauren"
    assert saved_event.referral_date == "2026-07-30"
    assert saved_event.notes == (
        "Practice short handling sessions with treats."
    )

def test_store_and_get_intake_event(test_db):
    common_event_data = {
        "event_id": "intake-cece-2026-07-31",
        "timestamp": datetime(2026, 7, 31, 16, 0),
        "inputted_by": "Pooja",
        "dog_name": "Cece",
        "source": EventSource.GS_MUTT_CHEAT_SHEET,
        "concerns": [BehaviorConcern.INTROS_TO_RESIDENT_PET],
        "summary": "Intake notes recommend slow introductions.",
    }

    intake_fields = {
        "foster_response": (
            "Cece may do best with gradual introductions."
        ),
    }

    event = create_intake_event(
        common_event_data,
        intake_fields,
    )

    store_dog_info(event)

    saved_events = get_behavior_events_for_dog("Cece")

    assert len(saved_events) == 1

    saved_event = saved_events[0]

    assert isinstance(saved_event, IntakeEvent)
    assert saved_event.event_id == "intake-cece-2026-07-31"
    assert saved_event.timestamp == datetime(2026, 7, 31, 16, 0)
    assert saved_event.inputted_by == "Pooja"
    assert saved_event.dog_name == "Cece"
    assert saved_event.source == EventSource.GS_MUTT_CHEAT_SHEET
    assert saved_event.concerns == [
        BehaviorConcern.INTROS_TO_RESIDENT_PET
    ]
    assert saved_event.summary == (
        "Intake notes recommend slow introductions."
    )
    assert saved_event.foster_response == (
        "Cece may do best with gradual introductions."
    )

def test_store_and_get_foster_event(test_db):
    common_event_data = {
        "event_id": "foster-cece-2026-07-31",
        "timestamp": datetime(2026, 7, 31, 17, 0),
        "inputted_by": "Pooja",
        "dog_name": "Cece",
        "source": EventSource.GS_FOSTER_QUESTIONNAIRE,
        "concerns": [
            BehaviorConcern.LEASH_REACTIVITY,
            BehaviorConcern.HANDLING_SENSITIVITY,
        ],
        "summary": "Cece is settling into her foster home.",
    }

    foster_fields = {
        "stairs_behavior": [
            StairBehaviorType.FEW_STAIRS,
        ],
        "potty_behavior": [
            PottyBehaviorType.YARD,
        ],
        "sleep_behavior": [
            SleepBehaviorType.DOG_BED,
        ],
        "sleep_behavior_other_text": None,
        "dogs_foster_home": EngagementBehaviorType.IGNORE,
        "cats_foster_home": EngagementBehaviorType.NOT_OBSERVED,
        "adults_foster_home": EngagementBehaviorType.ACTIVE,
        "kids_12_under_foster_home": (
            EngagementBehaviorType.NOT_OBSERVED
        ),
        "kids_13_over_foster_home": (
            EngagementBehaviorType.NOT_OBSERVED
        ),
        "dogs_other_home": EngagementBehaviorType.NOT_OBSERVED,
        "cats_other_home": EngagementBehaviorType.NOT_OBSERVED,
        "adults_other_home": EngagementBehaviorType.NOT_OBSERVED,
        "kids_12_under_other_home": (
            EngagementBehaviorType.NOT_OBSERVED
        ),
        "kids_13_over_other_home": (
            EngagementBehaviorType.NOT_OBSERVED
        ),
        "car_rides": EnjoymentBehaviorType.NERVOUS,
        "public_transportation": (
            EnjoymentBehaviorType.NOT_OBSERVED
        ),
        "carriers_strollers": (
            EnjoymentBehaviorType.NOT_OBSERVED
        ),
        "mobility_devices": EnjoymentBehaviorType.NOT_OBSERVED,
        "toys": EnjoymentBehaviorType.NEUTRAL,
        "being_petted": EnjoymentBehaviorType.ENJOYS,
        "leash_behavior": [
            LeashBehaviorType.BARKS_AT_DOGS,
            LeashBehaviorType.MEANDERS,
        ],
        "solo_mutt_behavior": SoloMuttBehaviorType.VOCAL,
    }

    event = create_foster_event(
        common_event_data,
        foster_fields,
    )

    store_dog_info(event)

    saved_events = get_behavior_events_for_dog("Cece")

    assert len(saved_events) == 1

    saved_event = saved_events[0]

    assert isinstance(saved_event, FosterBehaviorEvent)
    assert saved_event.event_id == "foster-cece-2026-07-31"
    assert saved_event.timestamp == datetime(2026, 7, 31, 17, 0)
    assert saved_event.inputted_by == "Pooja"
    assert saved_event.dog_name == "Cece"
    assert saved_event.source == EventSource.GS_FOSTER_QUESTIONNAIRE
    assert saved_event.concerns == [
        BehaviorConcern.LEASH_REACTIVITY,
        BehaviorConcern.HANDLING_SENSITIVITY,
    ]
    assert saved_event.summary == (
        "Cece is settling into her foster home."
    )

    assert saved_event.stairs_behavior == [
        StairBehaviorType.FEW_STAIRS
    ]
    assert saved_event.potty_behavior == [
        PottyBehaviorType.YARD
    ]
    assert saved_event.sleep_behavior == [
        SleepBehaviorType.DOG_BED
    ]
    assert saved_event.dogs_foster_home == (
        EngagementBehaviorType.IGNORE
    )
    assert saved_event.adults_foster_home == (
        EngagementBehaviorType.ACTIVE
    )
    assert saved_event.car_rides == (
        EnjoymentBehaviorType.NERVOUS
    )
    assert saved_event.being_petted == (
        EnjoymentBehaviorType.ENJOYS
    )
    assert saved_event.leash_behavior == [
        LeashBehaviorType.BARKS_AT_DOGS,
        LeashBehaviorType.MEANDERS,
    ]
    assert saved_event.solo_mutt_behavior == (
        SoloMuttBehaviorType.VOCAL
    )