from models.behavior_event import BehaviorConcern, BehaviorEvent, EventSource
from datetime import datetime
from typing import Any
from helpers.behavior_concern_classifier import classify_behavior_concern
from helpers.helper import clean_string, parse_timestamp

def parse_trainer_info(rows: list[dict]) -> list[BehaviorEvent]:
    events = []
    for row in rows:
        events.append(
            BehaviorEvent(
                occurred_at=datetime.strptime(
                    row["Referral Date "],
                    "%m/%d/%Y",
                ),
                dog_name=row["Dog Name"],
                source=EventSource.GS_MUTT_CHEAT_SHEET,
                concern=[BehaviorConcern(row["Primary Behavior Concern(s)"])],
                summary=f"Referred to trainer {row['Trainer Name']}",
                details={"notes": row.get("Notes")},
                raw_data=row,
            )
        )

    return [
    event.model_dump(
        exclude_none=True,
        exclude={"raw_data"}
    )
    for event in events
]


def parse_medication_info(
    rows: list[dict[str, Any]],
) -> list[BehaviorEvent]:
    events: list[BehaviorEvent] = []
    for row in rows:
        dog_name = clean_string(row.get("Dog's name"))
        summary = clean_string(
            row.get("Short description of behavior observed")
        )
        occurred_at = parse_timestamp(row.get("Timestamp"))

        if not dog_name or not summary or not occurred_at:
            continue

        additional_notes = clean_string(
            row.get("Any additional notes?")
        )

        event = BehaviorEvent(
            occurred_at=occurred_at,
            dog_name=dog_name,
            source=EventSource.GS_MEDICATIONS,
            concern=[classify_behavior_concern(
                summary=summary,
                notes=additional_notes,
            )],
            summary=summary,
            details={"additional_notes": additional_notes},
            location=clean_string(
                row.get("Where was behavior observed?")
            ),
            medication=clean_string(row.get("Medication")),
            raw_data=row,
        )

        events.append(event)

    return [
    event.model_dump(
        exclude_none=True,
        exclude={"raw_data"}
    )
    for event in events
]
