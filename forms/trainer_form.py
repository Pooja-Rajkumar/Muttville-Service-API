import streamlit as st

from models.behavior_modification_event import TrainerBehaviorEvent


def render_trainer_fields() -> dict:
    trainer_name = st.text_input(
        "Trainer name",
    )

    referral_date = st.date_input(
        "Referral date",
        value=None,
    )

    notes = st.text_area(
        "Trainer notes",
    )

    return {
        "trainer_name": trainer_name.strip() or None,
        "referral_date": (
            referral_date.isoformat()
            if referral_date
            else None
        ),
        "notes": notes.strip() or None,
    }


def create_trainer_event(
    common_event_data: dict,
    trainer_fields: dict,
) -> TrainerBehaviorEvent:
    return TrainerBehaviorEvent(
        **common_event_data,
        **trainer_fields,
    )