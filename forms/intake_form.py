import streamlit as st

from models.intake_event import IntakeEvent


def render_intake_fields() -> dict:
    foster_response = st.text_area(
        "Foster response",
    )

    return {
        "foster_response": foster_response.strip() or None,
    }


def create_intake_event(
    common_event_data: dict,
    intake_fields: dict,
) -> IntakeEvent:
    return IntakeEvent(
        **common_event_data,
        **intake_fields,
    )