import streamlit as st

from auth.auth import authenticate_user, build_google_login_url, get_client
from backfill import backfill_all, backfill_medications
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
from models.behavior_event import BehaviorConcern


st.set_page_config(
    page_title="Muttville Dog Timeline",
    page_icon="🐶",
    layout="wide",
)

st.title("🐶 Muttville Dog Timeline")
login_completed = authenticate_user()

if login_completed:
    st.rerun()

google_client = get_client()
if google_client:
    st.caption( "Logged into google")
else:
    st.caption("Not logged in.")
    st.link_button("Connect Google",build_google_login_url(),)  
    st.stop()

if st.button("Refresh database"):
    with st.spinner("Backfilling database..."):
        backfill_all()
    st.success("Backfill complete!")

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

@st.dialog("Behavior Event", width="large")
def show_event_details(event):
    st.subheader(event.dog_name)

    concern_names = []

    for concern in event.concerns:
        concern_names.append(concern.value)

    st.write(
        f"**Behavior Concern:** {', '.join(concern_names)}"
    )

    st.write(
        f"**Timestamp:** {event.timestamp.strftime('%b %d, %Y %I:%M %p')}"
    )

    st.write(
        f"**Inputted By:** {event.inputted_by}"
    )

    st.write("**Summary:**")
    st.write(event.summary)

    st.write(
        f"**Source:** {event.source.value}"
    )


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

        # Behavior concern filter
        selected_concern = st.selectbox(
            "Behavior concern",
            options=[None] + list(BehaviorConcern),
            format_func=lambda concern: (
                "All concerns"
                if concern is None
                else concern.value
            ),
        )

        # Filter events
        if selected_concern is None:
            filtered_events = events
        else:
            filtered_events = []

            for event in events:
                if selected_concern in event.concerns:
                    filtered_events.append(event)

        if not filtered_events:
            st.info("No matching behavior events.")

        else:
            # Build table
            all_table_rows = []

            for event in filtered_events:
                concern_names = []

                for concern in event.concerns:
                    concern_names.append(concern.value)

                all_table_rows.append(
                    {
                        "Timestamp": event.timestamp,
                        "Pup Name": event.dog_name,
                        "Behavior Concern": ", ".join(concern_names),
                        "Inputted By": event.inputted_by,
                        "Summary": event.summary,
                        "Source": event.source.value,
                    }
                )

            # Display table and allow row selection
            selection = st.dataframe(
                all_table_rows,
                use_container_width=True,
                hide_index=True,
                height=700,
                on_select="rerun",
                selection_mode="single-row",
                column_config={
                    "Timestamp": st.column_config.DatetimeColumn(
                        "Timestamp",
                        format="MMM D, YYYY h:mm a",
                        width="medium",
                    ),
                    "Summary": st.column_config.TextColumn(
                        "Summary",
                        width="large",
                    ),
                },
            )

            if selection.selection.rows:
                selected_index = selection.selection.rows[0]
                selected_event = filtered_events[selected_index]

                show_event_details(selected_event)

    except Exception as exc:
        st.error("Could not load database events.")
        st.exception(exc)
