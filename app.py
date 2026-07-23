import streamlit as st

from main import get_dog_info


st.set_page_config(
    page_title="Muttville Dog Timeline",
    page_icon="🐶",
    layout="centered",
)

st.title("🐶 Muttville Dog Timeline")
st.caption("Search for a dog to view their care and behavior history.")

dog_name = st.text_input(
    "Dog name",
    placeholder="Example: Pride",
)

def concern_chip(concern: str) -> str:
    colors = {
        "Leash Reactivity": "#F97316",       # Orange
        "Separation Distress": "#EF4444",    # Red
        "Handling Sensitivity": "#8B5CF6",   # Purple
        "Resource Guarding": "#DC2626",      # Dark Red
        "Potty Training": "#10B981",         # Green
        "Intros to Resident Pet": "#3B82F6", # Blue
        "Other": "#6B7280",                  # Gray
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
                st.info(f"No timeline events found for {dog_name}.")

            else:
                st.divider()

                st.header(dog_name.title())
                st.caption(f"{len(timeline)} timeline events")

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

                filtered_timeline = [
                    event
                    for event in timeline
                    if (
                        event.source.value
                        if hasattr(event.source, "value")
                        else str(event.source)
                    )
                    in selected_sources
                ]

                st.caption(
                    f"Showing {len(filtered_timeline)} of "
                    f"{len(timeline)} events"
                )

                for event_index, event in enumerate(filtered_timeline):
                    source = (
                        event.source.value
                        if hasattr(event.source, "value")
                        else str(event.source)
                    )

                    with st.container(border=True):
                        date_column, source_column = st.columns([2, 3])

                        with date_column:
                            st.caption(event.occurred_at_display)

                        with source_column:
                            st.caption(source)

                        if event.concern:
                            st.markdown("**Behavior concerns**")

                            chips = ""

                            for concern in event.concern:
                                concern_name = (
                                    concern.value
                                    if hasattr(concern, "value")
                                    else str(concern)
                                )

                                chips += concern_chip(concern_name)

                            st.markdown(chips, unsafe_allow_html=True)

                        if event.summary:
                            st.write(event.summary)


                        if event.medication:
                            st.write(
                                f"**Medication:** {event.medication}"
                            )

                        if event.location:
                            st.write(
                                f"**Location:** {event.location}"
                            )

                        if event.details:
                            visible_details = {
                                key: value
                                for key, value in event.details.items()
                                if value not in (
                                    None,
                                    "",
                                    [],
                                    {},
                                )
                            }

                            if visible_details:
                                with st.expander("View details"):
                                    for key, value in (
                                        visible_details.items()
                                    ):
                                        label = (
                                            key.replace("_", " ")
                                            .strip()
                                            .title()
                                        )

                                        st.write(
                                            f"**{label}:** {value}"
                                        )

        except Exception as exc:
            st.error("Could not load the dog's timeline.")
            st.exception(exc)