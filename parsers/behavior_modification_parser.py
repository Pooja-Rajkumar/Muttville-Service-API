from models.behavior_event import BehaviorConcern, BehaviorEvent, EventSource
from datetime import datetime
from typing import Any
from helpers.behavior_concern_classifier import classify_behavior_concern
from helpers.helper import clean_string, parse_timestamp
from models.behavior_modification_event import MedicationBehaviorEvent, TrainerBehaviorEvent

def parse_trainer_info(rows: list[dict]) -> list[BehaviorEvent]:
    events = []
    for row in rows:
        events.append(
            TrainerBehaviorEvent(
                timestamp=datetime.strptime(
                    row["Referral Date "],
                    "%m/%d/%Y",
                ),
                inputted_by=clean_string(row.get("Who referred?")),
                dog_name=clean_string(row.get("Dog Name")),
                source=EventSource.GS_MUTT_CHEAT_SHEET,
                concerns=match_behavior_concerns(row.get("Primary Behavior Concern(s)")),
                summary=f"Referred to trainer {row['Trainer Name']}",
                trainer_name=clean_string(row.get("Trainer Name")),
                referral_date=clean_string(row.get("Referral Date ")),
                notes=clean_string(row.get("Notes")),
            )
        )

    return events

def match_behavior_concerns(value: str | None) -> list[BehaviorConcern]:
    if not value:
        return [BehaviorConcern.OTHER]
    concerns = []
    values = value.split(",")
    for item in values:
        item = item.strip()
        try:
            concern = BehaviorConcern(item)
            concerns.append(concern)
        except ValueError:
            continue
    if not concerns:
        return [BehaviorConcern.OTHER]
    return concerns

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

        event = MedicationBehaviorEvent(
            timestamp=occurred_at,
            inputted_by=clean_string(row.get("Your name")),
            dog_name=dog_name,
            source=EventSource.GS_MEDICATIONS,
            concerns=[classify_behavior_concern(
                summary=summary,
                notes=additional_notes,
            )],
            summary=summary,
            location=clean_string(
                row.get("Where was behavior observed?")
            ),
            medication=clean_string(row.get("Medication")),
            raw_data=row,
        )

        events.append(event)

    return events

