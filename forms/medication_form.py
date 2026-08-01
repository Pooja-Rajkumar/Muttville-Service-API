import streamlit as st

from models.behavior_modification_event import MedicationBehaviorEvent


def render_medication_fields() -> dict:
    medication = st.text_input(
        "Medication",
    )

    location = st.text_input(
        "Location",
    )

    return {
        "medication": medication.strip() or None,
        "location": location.strip() or None,
    }


def create_medication_event(
    common_event_data: dict,
    medication_fields: dict,
) -> MedicationBehaviorEvent:
    return MedicationBehaviorEvent(
        **common_event_data,
        **medication_fields,
    )