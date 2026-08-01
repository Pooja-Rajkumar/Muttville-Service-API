from datetime import datetime
from enum import Enum
from uuid import uuid4

import streamlit as st

from models.behavior_event import BehaviorConcern, EventSource


EVENT_SOURCES = {
    "Medication": EventSource.GS_MEDICATIONS,
    "Trainer": EventSource.GS_BEHAVIORAL_OUTREACH_FOSTER,
    "Intake": EventSource.GS_MUTT_CHEAT_SHEET,
    "Foster Questionnaire": EventSource.GS_FOSTER_QUESTIONNAIRE,
}


def render_common_fields() -> dict:
    pup_name = st.text_input(
        "Pup name",
        placeholder="Example: Cece",
    )

    inputted_by = st.text_input(
        "Inputted by",
    )

    event_date = st.date_input(
        "Date",
    )

    event_time = st.time_input(
        "Time",
    )

    concerns = st.multiselect(
        "Behavior concerns",
        options=list(BehaviorConcern),
        format_func=lambda concern: concern.value,
    )

    summary = st.text_area(
        "Summary",
        placeholder="Describe the behavior or care update.",
    )

    return {
        "pup_name": pup_name,
        "inputted_by": inputted_by,
        "event_date": event_date,
        "event_time": event_time,
        "concerns": concerns,
        "summary": summary,
    }


def build_common_event_data(
    event_type: str,
    common_fields: dict,
) -> dict:
    return {
        "event_id": str(uuid4()),
        "timestamp": datetime.combine(
            common_fields["event_date"],
            common_fields["event_time"],
        ),
        "inputted_by": (
            common_fields["inputted_by"].strip() or None
        ),
        "dog_name": common_fields["pup_name"].strip(),
        "source": EVENT_SOURCES[event_type],
        "concerns": (
            common_fields["concerns"]
            or [BehaviorConcern.OTHER]
        ),
        "summary": common_fields["summary"].strip(),
    }


def optional_enum_selectbox(
    label: str,
    enum_type: type[Enum],
    key: str,
):
    options = [None]

    for option in enum_type:
        options.append(option)

    return st.selectbox(
        label,
        options=options,
        format_func=lambda option: (
            "Not specified"
            if option is None
            else option.value
        ),
        key=key,
    )