import streamlit as st

from forms.common import optional_enum_selectbox
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


def render_foster_fields() -> dict:
    st.subheader("Home life")

    stairs_behavior = st.multiselect(
        "Stairs",
        options=list(StairBehaviorType),
        format_func=lambda option: option.value,
    )

    potty_behavior = st.multiselect(
        "Potty behavior",
        options=list(PottyBehaviorType),
        format_func=lambda option: option.value,
    )

    sleep_behavior = st.multiselect(
        "Sleep behavior",
        options=list(SleepBehaviorType),
        format_func=lambda option: option.value,
    )

    sleep_behavior_other_text = st.text_input(
        "Other sleep location",
    )

    st.subheader("Social experiences at foster home")

    dogs_foster_home = optional_enum_selectbox(
        "Dogs",
        EngagementBehaviorType,
        "form_dogs_foster_home",
    )

    cats_foster_home = optional_enum_selectbox(
        "Cats",
        EngagementBehaviorType,
        "form_cats_foster_home",
    )

    adults_foster_home = optional_enum_selectbox(
        "Adults",
        EngagementBehaviorType,
        "form_adults_foster_home",
    )

    kids_12_under_foster_home = optional_enum_selectbox(
        "Kids 12 and under",
        EngagementBehaviorType,
        "form_kids_12_under_foster_home",
    )

    kids_13_over_foster_home = optional_enum_selectbox(
        "Kids 13 and over",
        EngagementBehaviorType,
        "form_kids_13_over_foster_home",
    )

    st.subheader("Social experiences in other homes")

    dogs_other_home = optional_enum_selectbox(
        "Dogs in other homes",
        EngagementBehaviorType,
        "form_dogs_other_home",
    )

    cats_other_home = optional_enum_selectbox(
        "Cats in other homes",
        EngagementBehaviorType,
        "form_cats_other_home",
    )

    adults_other_home = optional_enum_selectbox(
        "Adults in other homes",
        EngagementBehaviorType,
        "form_adults_other_home",
    )

    kids_12_under_other_home = optional_enum_selectbox(
        "Kids 12 and under in other homes",
        EngagementBehaviorType,
        "form_kids_12_under_other_home",
    )

    kids_13_over_other_home = optional_enum_selectbox(
        "Kids 13 and over in other homes",
        EngagementBehaviorType,
        "form_kids_13_over_other_home",
    )

    st.subheader("Other experiences")

    car_rides = optional_enum_selectbox(
        "Car rides",
        EnjoymentBehaviorType,
        "form_car_rides",
    )

    public_transportation = optional_enum_selectbox(
        "Public transportation",
        EnjoymentBehaviorType,
        "form_public_transportation",
    )

    carriers_strollers = optional_enum_selectbox(
        "Carriers, strollers, or pouches",
        EnjoymentBehaviorType,
        "form_carriers_strollers",
    )

    mobility_devices = optional_enum_selectbox(
        "Canes, walkers, or wheelchairs",
        EnjoymentBehaviorType,
        "form_mobility_devices",
    )

    toys = optional_enum_selectbox(
        "Toys",
        EnjoymentBehaviorType,
        "form_toys",
    )

    st.subheader("Handling")

    being_petted = optional_enum_selectbox(
        "Being petted",
        EnjoymentBehaviorType,
        "form_being_petted",
    )

    st.subheader("Walking and alone time")

    leash_behavior = st.multiselect(
        "Leash behavior",
        options=list(LeashBehaviorType),
        format_func=lambda option: option.value,
    )

    solo_mutt_behavior = optional_enum_selectbox(
        "Alone time",
        SoloMuttBehaviorType,
        "form_solo_mutt_behavior",
    )

    return {
        "stairs_behavior": stairs_behavior or None,
        "potty_behavior": potty_behavior or None,
        "sleep_behavior": sleep_behavior or None,
        "sleep_behavior_other_text": (
            sleep_behavior_other_text.strip() or None
        ),
        "dogs_foster_home": dogs_foster_home,
        "cats_foster_home": cats_foster_home,
        "adults_foster_home": adults_foster_home,
        "kids_12_under_foster_home": (
            kids_12_under_foster_home
        ),
        "kids_13_over_foster_home": (
            kids_13_over_foster_home
        ),
        "dogs_other_home": dogs_other_home,
        "cats_other_home": cats_other_home,
        "adults_other_home": adults_other_home,
        "kids_12_under_other_home": kids_12_under_other_home,
        "kids_13_over_other_home": kids_13_over_other_home,
        "car_rides": car_rides,
        "public_transportation": public_transportation,
        "carriers_strollers": carriers_strollers,
        "mobility_devices": mobility_devices,
        "toys": toys,
        "being_petted": being_petted,
        "leash_behavior": leash_behavior or None,
        "solo_mutt_behavior": solo_mutt_behavior,
    }


def create_foster_event(
    common_event_data: dict,
    foster_fields: dict,
) -> FosterBehaviorEvent:
    return FosterBehaviorEvent(
        **common_event_data,
        **foster_fields,
    )