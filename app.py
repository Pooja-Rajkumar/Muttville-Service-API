import streamlit as st

from database.database import get_all_behavior_events, save_behavior_event
from forms.common import (
    build_common_event_data,
    render_common_fields,
)
from forms.foster_form import (
    create_foster_event,
    render_foster_fields,
)
from forms.intake_form import (
    create_intake_event,
    render_intake_fields,
)
from forms.medication_form import (
    create_medication_event,
    render_medication_fields,
)
from forms.trainer_form import (
    create_trainer_event,
    render_trainer_fields,
)
from main import get_dog_info, store_dog_info


st.set_page_config(
    page_title="Muttville Dog Timeline",
    page_icon="🐶",
    layout="centered",
)

st.title("🐶 Muttville Dog Timeline")


def concern_chip(concern: str) -> str:
    colors = {
        "Leash Reactivity": "#F97316",
        "Separation Distress": "#EF4444",
        "Handling Sensitivity": "#8B5CF6",
        "Resource Guarding": "#DC2626",
        "Potty Training": "#10B981",
        "Intros to Resident Pet": "#3B82F6",
        "Other": "#6B7280",
    }

    color = colors.get(concern, "#6B7280")

    return f"""
        <span style="
            display:inline-block;
            background-color:{color};
            color:white;
            padding:6px 12px;
            border-radius:999px;
            margin:4px;
            font-size:0.85rem;
            font-weight:600;
        ">
            {concern}
        </span>
    """


timeline_tab, add_event_tab, database_tab = st.tabs(
    [
        "View timeline",
        "Add event",
        "View database"
    ]
)


with timeline_tab:
    st.caption(
        "Search for a dog to view their care and behavior history."
    )

    dog_name = st.text_input(
        "Dog name",
        placeholder="Example: Pride",
        key="timeline_dog_name",
    )

    search_clicked = st.button(
        "Search",
        type="primary",
        use_container_width=True,
    )

    if search_clicked:
        dog_name = dog_name.strip()

        if not dog_name:
            st.warning("Enter a dog name.")

        else:
            try:
                with st.spinner(f"Loading {dog_name}..."):
                    timeline = get_dog_info(dog_name)

                if not timeline:
                    st.info(
                        f"No timeline events found for {dog_name}."
                    )

                else:
                    st.divider()

                    st.header(dog_name.title())
                    st.caption(
                        f"{len(timeline)} timeline events"
                    )

                    source_names = sorted(
                        {
                            event.source.value
                            if hasattr(event.source, "value")
                            else str(event.source)
                            for event in timeline
                        }
                    )

                    selected_sources = st.multiselect(
                        "Filter by source",
                        options=source_names,
                        default=source_names,
                    )

                    filtered_timeline = []

                    for event in timeline:
                        source = (
                            event.source.value
                            if hasattr(event.source, "value")
                            else str(event.source)
                        )

                        if source in selected_sources:
                            filtered_timeline.append(event)

                    st.caption(
                        f"Showing {len(filtered_timeline)} of "
                        f"{len(timeline)} events"
                    )

                    for event in filtered_timeline:
                        source = (
                            event.source.value
                            if hasattr(event.source, "value")
                            else str(event.source)
                        )

                        with st.container(border=True):
                            date_column, source_column = st.columns(
                                [2, 3]
                            )

                            with date_column:
                                st.caption(
                                    event.timestamp_display
                                )

                            with source_column:
                                st.caption(source)

                            if event.concerns:
                                st.markdown(
                                    "**Behavior concerns**"
                                )

                                chips = ""

                                for concern in event.concerns:
                                    concern_name = (
                                        concern.value
                                        if hasattr(
                                            concern,
                                            "value",
                                        )
                                        else str(concern)
                                    )

                                    chips += concern_chip(
                                        concern_name
                                    )

                                st.markdown(
                                    chips,
                                    unsafe_allow_html=True,
                                )

                            if event.summary:
                                st.write(event.summary)

                            if event.inputted_by:
                                st.write(
                                    "**Inputted by:** "
                                    f"{event.inputted_by}"
                                )

            except Exception as exc:
                st.error(
                    "Could not load the dog's timeline."
                )
                st.exception(exc)


with add_event_tab:
    st.header("Add an event")

    event_type = st.selectbox(
        "Event type",
        options=[
            "Medication",
            "Trainer",
            "Intake",
            "Foster Questionnaire",
        ],
    )

    with st.form(
        "add_behavior_event_form",
        clear_on_submit=True,
    ):
        common_fields = render_common_fields()

        event_specific_fields = {}

        if event_type == "Medication":
            event_specific_fields = (
                render_medication_fields()
            )

        elif event_type == "Trainer":
            event_specific_fields = render_trainer_fields()

        elif event_type == "Intake":
            event_specific_fields = render_intake_fields()

        elif event_type == "Foster Questionnaire":
            event_specific_fields = render_foster_fields()

        submit_clicked = st.form_submit_button(
            "Save event",
            type="primary",
            use_container_width=True,
        )

    if submit_clicked:
        pup_name = common_fields["pup_name"].strip()
        summary = common_fields["summary"].strip()

        if not pup_name:
            st.error("Pup name is required.")

        elif not summary:
            st.error("Summary is required.")

        else:
            try:
                common_event_data = build_common_event_data(
                    event_type,
                    common_fields,
                )

                if event_type == "Medication":
                    event = create_medication_event(
                        common_event_data,
                        event_specific_fields,
                    )

                elif event_type == "Trainer":
                    event = create_trainer_event(
                        common_event_data,
                        event_specific_fields,
                    )

                elif event_type == "Intake":
                    event = create_intake_event(
                        common_event_data,
                        event_specific_fields,
                    )

                else:
                    event = create_foster_event(
                        common_event_data,
                        event_specific_fields,
                    )

                
                store_dog_info(event)
                st.session_state["save_message"] = (
                    f"Saved {event_type.lower()} event for {pup_name}."
                )

                st.rerun()
            except Exception as exc:
                st.error("Could not save the event.")
                st.exception(exc)

with database_tab:
    st.header("All database events")

    try:
        events = get_all_behavior_events()

        if not events:
            st.info("No behavior events are stored yet.")

        else:
            table_rows = []

            for event in events:
                concern_names = []

                for concern in event.concerns:
                    concern_names.append(concern.value)

                table_rows.append(
                    {
                        "Event ID": event.event_id,
                        "Event Type": event.__class__.__name__,
                        "Timestamp": event.timestamp,
                        "Pup Name": event.dog_name,
                        "Source": event.source.value,
                        "Inputted By": event.inputted_by,
                        "Concerns": ", ".join(concern_names),
                        "Summary": event.summary,
                    }
                )

            st.dataframe(
                table_rows,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Timestamp": st.column_config.DatetimeColumn(
                        "Timestamp",
                        format="MMM D, YYYY h:mm a",
                    ),
                    "Summary": st.column_config.TextColumn(
                        "Summary",
                        width="large",
                    ),
                    "Event ID": st.column_config.TextColumn(
                        "Event ID",
                        width="medium",
                    ),
                },
            )

    except Exception as exc:
        st.error("Could not load database events.")
        st.exception(exc)