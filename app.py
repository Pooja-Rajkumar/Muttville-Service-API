from datetime import datetime
from html import escape

import streamlit as st

from auth.auth import authenticate_user, build_google_login_url, get_client
from backfill import backfill_all
from database.database import create_tables, get_all_behavior_events, get_db_connection, update_event_concerns
from main import get_dog_info, store_dog_info
from models.behavior_event import BehaviorConcern, BehaviorEvent, EventSource
from models.foster_behavior_event import FosterBehaviorEvent

st.set_page_config(
    page_title="Muttville Dog Timeline",
    page_icon="🐶",
    layout="wide",
)

create_tables()

# Warm, approachable visual theme. All application logic stays in Streamlit.
st.markdown("""
<style>
    /* Light, welcoming surface. The native widget/table palette is set in
       .streamlit/config.toml so Streamlit's canvas-based grid also changes. */
    .stApp { background-color: #FBF8F1; color: #283B32; }
    [data-testid="stHeader"] { background-color: #FBF8F1; }
    .block-container {
        max-width: none;
        width: 100%;
        padding-left: clamp(1rem, 3vw, 3.5rem);
        padding-right: clamp(1rem, 3vw, 3.5rem);
        /* Clear Streamlit's fixed top toolbar so the title is never hidden. */
        padding-top: 5rem;
        padding-bottom: 4rem;
    }
    h1, h2, h3 { color: #294C3A; letter-spacing: -0.025em; }
    [data-testid="stCaptionContainer"] { color: #667A6B; }

    /* Inputs must stay light even when an older Streamlit theme is cached. */
    .stApp [data-baseweb="input"] > div,
    .stApp [data-baseweb="select"] > div,
    .stApp [data-baseweb="textarea"] > div,
    .stApp input,
    .stApp textarea {
        background: #FFFFFF !important;
        color: #283B32 !important;
        border-color: #DDE5D9 !important;
        border-radius: 12px !important;
    }
    .stApp input::placeholder, .stApp textarea::placeholder {
        color: #89968D !important;
        opacity: 1;
    }
    .stApp [data-baseweb="tag"] {
        background: #E4EEE2 !important;
        border-radius: 8px !important;
    }
    .stApp [data-baseweb="tag"] span,
    .stApp [data-baseweb="tag"] svg {
        color: #294C3A !important;
        fill: #294C3A !important;
    }
    .stApp [data-baseweb="select"] svg { color: #567D65; }
    .stApp [data-baseweb="input"]:focus-within,
    .stApp [data-baseweb="select"]:focus-within,
    .stApp [data-baseweb="textarea"]:focus-within {
        outline: 1px solid #567D65;
        border-radius: 12px;
    }
    [data-testid="stWidgetLabel"] { color: #344E3D; }

    /* Buttons: avoid styling all p tags globally (which made button labels dark). */
    .stApp .stButton > button[kind="primary"],
    .stApp .stFormSubmitButton > button[kind="primary"] {
        background: #567D65 !important;
        border-color: #567D65 !important;
        color: #FFFFFF !important;
        border-radius: 12px;
    }
    .stApp .stButton > button[kind="primary"] p,
    .stApp .stFormSubmitButton > button[kind="primary"] p {
        color: #FFFFFF !important;
    }
    .stApp .stButton > button[kind="primary"]:hover,
    .stApp .stFormSubmitButton > button[kind="primary"]:hover {
        background: #416A52 !important;
        border-color: #416A52 !important;
    }
    .stApp .stButton > button:not([kind="primary"]) {
        background: #FFFFFF;
        border: 1px solid #C9D9CB;
        color: #294C3A !important;
        border-radius: 12px;
    }
    .stApp .stButton > button:not([kind="primary"]) p {
        color: #294C3A !important;
    }
    /* Sign-in is the primary action on the logged-out page. */
    .stApp [data-testid="stLinkButton"] a {
        background: #567D65 !important;
        border: 1px solid #567D65 !important;
        color: #FFFFFF !important;
        border-radius: 12px;
        min-height: 3.1rem;
    }
    .stApp [data-testid="stLinkButton"] a p {
        color: #FFFFFF !important;
        font-weight: 700;
    }
    .stApp [data-testid="stLinkButton"] a:hover {
        background: #416A52 !important;
        border-color: #416A52 !important;
    }

    /* Tabs, cards, tables, form framing */
    button[data-baseweb="tab"] { font-weight: 650; }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #294C3A !important;
        border-bottom-color: #567D65 !important;
    }
    [data-testid="stVerticalBlockBorderWrapper"] > div { border-radius: 18px; }
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.event-card-marker) {
        background: #FFFFFF;
        border: 1px solid #E2E9DD;
        box-shadow: 0 4px 18px rgba(52, 75, 58, 0.045);
    }
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.event-card-marker):hover {
        border-color: #B7CEB7;
    }
    [data-testid="stForm"] {
        background: #FFFDF9;
        border: 1px solid #E5EBDD;
        border-radius: 20px;
        padding: 1.3rem;
    }
    [data-testid="stDataFrame"] {
        background: #FFFFFF;
        border: 1px solid #DCE5D9;
        border-radius: 16px;
        overflow: hidden;
    }
    [data-testid="stDialog"] { color: #283B32; }

    /* Signed-out screen: one intentional focal point, not a stretched dashboard. */
    .login-eyebrow {
        color: #64836A;
        font-size: 0.8rem;
        font-weight: 800;
        letter-spacing: 0.12em;
        margin-bottom: 1.2rem;
    }
    .login-heading {
        color: #294C3A;
        font-size: clamp(2.3rem, 4vw, 3.7rem);
        font-weight: 800;
        line-height: 1.12;
        letter-spacing: -0.045em;
        margin-bottom: 1.15rem;
    }
    .login-description {
        color: #66786A;
        font-size: 1.08rem;
        line-height: 1.7;
        margin-bottom: 1.35rem;
    }
    .login-note {
        color: #738478;
        font-size: 0.84rem;
        margin-top: 0.45rem;
    }
    .login-card-marker { display: none; }
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.login-card-marker) {
        border: 1px solid #DCE7D8;
        background: linear-gradient(145deg, #FFFFFF 0%, #F2F6EC 100%);
        border-radius: 24px;
        box-shadow: 0 14px 42px rgba(52, 75, 58, 0.07);
        padding: clamp(1.2rem, 3vw, 2.4rem);
    }
    .muttville-title {
        font-size: clamp(2.0rem, 3.6vw, 2.85rem);
        font-weight: 800;
        letter-spacing: -0.045em;
        color: #294C3A;
        line-height: 1.25;
        overflow-wrap: anywhere;
    }
    .muttville-subtitle {
        color: #66786A;
        margin: 0.55rem 0 1.4rem;
        line-height: 1.55;
    }
    .muttville-eyebrow {
        color: #64836A;
        font-size: 0.76rem;
        font-weight: 800;
        letter-spacing: 0.11em;
        text-transform: uppercase;
        line-height: 1.7;
    }
    .timeline-empty {
        margin-top: 1.3rem;
        padding: 2rem 2.2rem;
        border: 1px solid #DFE7D7;
        border-radius: 20px;
        background: linear-gradient(110deg, #F0F5EC, #FBF8F1);
    }
    .timeline-empty-title {
        color: #294C3A;
        font-weight: 750;
        font-size: 1.1rem;
        margin-bottom: 0.35rem;
    }
    .timeline-empty-description {
        color: #687A6B;
        line-height: 1.5;
    }
    .dog-hero {
        background: linear-gradient(110deg, #E9F1E4, #F6F0E3);
        border: 1px solid #DFE7D7;
        border-radius: 22px;
        padding: 24px 28px;
        margin: 16px 0 22px;
    }
    .dog-hero-title {
        font-size: 2rem;
        line-height: 1.3;
        font-weight: 800;
        color: #294C3A;
        overflow-wrap: anywhere;
    }
    .dog-hero-meta { color: #687A6B; font-size: 0.93rem; margin-top: 6px; }
    .event-card-marker { display: none; }
    .event-heading {
        color: #294C3A;
        font-size: 1.13rem;
        line-height: 1.4;
        font-weight: 750;
        overflow-wrap: anywhere;
    }
    .soft-tag {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 99px;
        font-size: 0.79rem;
        line-height: 1.3;
        font-weight: 650;
        margin: 3px 6px 3px 0;
        white-space: normal;
        overflow-wrap: anywhere;
    }
    .section-intro { color: #687A6B; margin: -0.2rem 0 1.2rem; line-height: 1.55; }

    /* Signed-in brand: centered like the sign-in screen, but compact enough
       to leave working room for the timeline and the full-width database. */
    .app-brand {
        text-align: center;
        margin: 0 auto;
        padding: 0.2rem 0 0.6rem;
    }
    .app-brand-row {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.75rem;
    }
    .app-brand-mark {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        background: #E9F1E4;
        border: 1px solid #DCE7D8;
        border-radius: 15px;
        width: 3rem;
        height: 3rem;
        font-size: 1.8rem;
        flex-shrink: 0;
    }
    .app-brand-title {
        color: #294C3A;
        font-size: clamp(1.8rem, 2.8vw, 2.45rem);
        font-weight: 800;
        letter-spacing: -0.045em;
        line-height: 1.25;
        margin: 0;
    }
    .app-brand-tagline {
        color: #66786A;
        font-size: 0.95rem;
        margin: 0.45rem 0 0;
        line-height: 1.5;
    }
    .app-brand-status {
        color: #64836A;
        font-size: 0.87rem;
    }
    div[data-testid="stDataFrame"] {
        width: 100%;
    }
    .stat-card {
        background: #FFFFFF;
        border: 1px solid #E1E9DD;
        border-radius: 16px;
        padding: 10px 16px;
        min-height: 78px;
    }
    .stat-label {
        font-size: 0.78rem;
        color: #718474;
        font-weight: 700;
        letter-spacing: 0.03em;
        text-transform: uppercase;
    }
    .stat-number { font-size: 1.45rem; color: #294C3A; font-weight: 800; margin-top: 2px; }
    .database-help { color: #617969; font-size: 0.87rem; margin: 4px 0 10px; }

    @media (max-width: 720px) {
        .block-container { padding-top: 4.5rem; }
        .dog-hero { padding: 18px; }
        .app-brand-title { font-size: 1.6rem; }
        .app-brand-mark { width: 2.5rem; height: 2.5rem; font-size: 1.5rem; }
        .app-brand-tagline { font-size: 0.87rem; }
    }
</style>
""", unsafe_allow_html=True)

login_completed = authenticate_user()

if login_completed:
    st.rerun()

google_client = get_client()
if not google_client:
    # The sign-in screen is intentionally narrower than the full-width database.
    st.markdown("<div style='height: 5vh'></div>", unsafe_allow_html=True)
    left_column, login_column, right_column = st.columns([1, 2, 1])
    with login_column:
        with st.container(border=True):
            st.markdown('<span class="login-card-marker"></span>', unsafe_allow_html=True)
            st.markdown(
                '<div class="login-eyebrow">🐾 MUTTVILLE CARE HUB</div>'
                '<div class="login-heading">Every dog has a story.</div>'
                '<div class="login-description">'
                'Care notes, behavior observations, and each pup’s history — '
                'all in one welcoming place.'
                '</div>',
                unsafe_allow_html=True,
            )
            st.link_button(
                "Sign in with Google",
                build_google_login_url(),
                type="primary",
                use_container_width=True,
            )
            st.markdown(
                '<div class="login-note">Use your Muttville Google account to continue.</div>',
                unsafe_allow_html=True,
            )
    st.stop()

# Signed-in masthead: a centered wordmark, like the sign-in card.
st.markdown(
    '<div class="app-brand">'
    '<div class="app-brand-row">'
    '<span class="app-brand-mark">🐶</span>'
    '<div class="app-brand-title">Every dog has a story.</div>'
    '</div>'
    '<div class="app-brand-tagline">Care notes and observations, all in one place.</div>'
    '</div>',
    unsafe_allow_html=True,
)

# Keep the refresh action right-aligned beneath the centered brand.
_, right_column = st.columns([5, 1], vertical_alignment="center")
with right_column:
    if st.button("Refresh database", use_container_width=True):
        with st.spinner("Refreshing records..."):
            backfill_all()
        st.success("Database refreshed!")

        
def concern_chip(concern: str) -> str:
    colors = {
        "Leash Reactivity": ("#FFF0DE", "#9D5D20"),
        "Separation Distress": ("#FBE8E5", "#A64F49"),
        "Handling Sensitivity": ("#F0EAF8", "#785A9A"),
        "Resource Guarding": ("#F9E7E5", "#9D4D4B"),
        "Potty Training": ("#E5F3E7", "#35764A"),
        "Intros to Resident Pet": ("#E6EFF7", "#476F92"),
        "Other": ("#EFF0EA", "#667267"),
    }
    background, foreground = colors.get(concern, ("#EFF0EA", "#667267"))
    return (
        f'<span class="soft-tag" style="background:{background};color:{foreground};">'
        f'{escape(concern)}</span>'
    )


def event_label(event):
    if hasattr(event, "medication") and event.medication:
        return "💊 Medication update"
    if isinstance(event, FosterBehaviorEvent):
        return "🏡 Foster observation"
    if event.source == EventSource.MANUAL:
        return "📝 Staff observation"
    return "🐾 Care & behavior update"


# modal 
@st.dialog("Behavior Event", width="large")
def show_event_details(event):
    st.subheader(event.dog_name)

    # Allow staff to edit behavior concerns
    updated_concerns = st.multiselect(
        "Behavior concerns",
        options=list(BehaviorConcern),
        default=event.concerns,
        format_func=lambda concern: concern.value,
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

    if st.button("Save changes"):
        with get_db_connection() as connection:
            update_event_concerns(event, updated_concerns, connection)
        st.success("Behavior concerns updated!")
        st.rerun()

timeline_tab, add_event_tab, database_tab = st.tabs(
    [
        "View timeline",
        "Add event",
        "View database"
    ]
)

with timeline_tab:
    # Keep reading and entry forms comfortable on wide screens.
    # The database tab below stays full width.
    left_margin, content_column, right_margin = st.columns([1, 4, 1])
    with content_column:
        st.subheader("Pup timeline")
        # st.markdown('<div class="section-intro">Follow a pup’s journey through observations, care, and updates.</div>', unsafe_allow_html=True)

        # Text inputs run on_change when Enter is pressed (or the field loses focus).
        # Use the same search code for keyboard and button submissions.
        def request_timeline_search():
            st.session_state["timeline_search_requested"] = True

        search_column, button_column = st.columns([5, 1], vertical_alignment="bottom")
        with search_column:
            dog_name = st.text_input(
                "",
                placeholder="Search by pup name, e.g. Pride",
                key="timeline_dog_name",
                on_change=request_timeline_search,
            )
        with button_column:
            search_clicked = st.button(
                "Search",
                type="primary",
                use_container_width=True,
            )

        # Clear stale results when the dog name is changed or erased.
        previous_dog = st.session_state.get("timeline_dog")
        if previous_dog:
            if dog_name.strip().lower() != previous_dog.strip().lower():
                st.session_state.pop("timeline", None)
                st.session_state.pop("timeline_dog", None)

        # Both Enter in the input and the Search button run this same search.
        search_requested = st.session_state.pop("timeline_search_requested", False)

        # SEARCH FOR DOG AND SAVE RESULTS
        if search_clicked or search_requested:
            dog_name = dog_name.strip()

            if not dog_name:
                if search_clicked:
                    st.warning("Enter a dog name.")

            else:
                try:
                    with st.spinner(f"Loading {dog_name}..."):
                        timeline = get_dog_info(dog_name)

                    st.session_state["timeline"] = timeline
                    st.session_state["timeline_dog"] = dog_name

                except Exception as exc:
                    st.error("Could not load the dog's timeline.")
                    st.exception(exc)

        # DISPLAY SAVED TIMELINE
        if "timeline" in st.session_state:

            timeline = st.session_state["timeline"]
            dog_name = st.session_state["timeline_dog"]

            if not timeline:
                st.info(
                    f"No timeline events found for {dog_name}."
                )

            else:
                st.markdown(
                    '<div class="dog-hero">'
                    '<div class="muttville-eyebrow">🐾 Dog profile</div>'
                    f'<div class="dog-hero-title">{escape(dog_name.title())}</div>'
                    f'<div class="dog-hero-meta">{len(timeline)} care & behavior events recorded</div>'
                    '</div>',
                    unsafe_allow_html=True,
                )

                # Get all behavior concerns for this dog
                concern_names = set()

                for event in timeline:
                    for concern in event.concerns:
                        concern_names.add(concern.value)

                concern_names = sorted(concern_names)

                # Filter
                selected_concerns = st.multiselect(
                    "Filter by behavior concern",
                    options=concern_names,
                    default=[],
                )

                filtered_timeline = []

                for event in timeline:
                    # No concern selected means show all of this dog's events.
                    if not selected_concerns:
                        filtered_timeline.append(event)
                    else:
                        for concern in event.concerns:
                            if concern.value in selected_concerns:
                                filtered_timeline.append(event)
                                break

                st.caption(
                    f"Showing {len(filtered_timeline)} of "
                    f"{len(timeline)} events"
                )

                st.markdown("#### Care timeline")
                # Each entry uses a clear title, date, source and softly colored tags.
                for event in filtered_timeline:
                    with st.container(border=True):
                        st.markdown('<span class="event-card-marker"></span>', unsafe_allow_html=True)
                        heading_column, date_column = st.columns([3, 2])
                        with heading_column:
                            st.markdown(
                                f'<div class="event-heading">{escape(event_label(event))}</div>',
                                unsafe_allow_html=True,
                            )
                            st.caption(f"Source: {event.source.value}")
                        with date_column:
                            st.caption(event.timestamp_display)
                            if event.location:
                                st.caption(f"📍 {event.location}")

                        if event.concerns:
                            chips = ""
                            for concern in event.concerns:
                                chips += concern_chip(concern.value)
                            st.markdown(chips, unsafe_allow_html=True)

                        if event.summary:
                            st.write(event.summary)

                        if hasattr(event, "medication") and event.medication:
                            st.write(f"**Medication:** {event.medication}")
                            if event.status:
                                status_names = []
                                for status in event.status:
                                    status_names.append(status.value)
                                st.write(f"**Status:** {', '.join(status_names)}")

                        if isinstance(event, FosterBehaviorEvent):
                            if (
                                event.anything_to_add
                                or event.potential_adopter_info
                                or event.muttville_care_additional_notes
                            ):
                                with st.expander("Read additional foster notes"):
                                    if event.anything_to_add:
                                        st.write(f"**Anything to add:** {event.anything_to_add}")
                                    if event.potential_adopter_info:
                                        st.write(f"**Potential adopter information:** {event.potential_adopter_info}")
                                    if event.muttville_care_additional_notes:
                                        st.write(f"**Muttville care additional notes:** {event.muttville_care_additional_notes}")

                        if event.inputted_by:
                            st.caption(f"Recorded by {event.inputted_by}")
        else:
            st.markdown(
                '<div class="timeline-empty">'
                '<div class="timeline-empty-title">🐾 Start with a dog’s name</div>'
                '<div class="timeline-empty-description">Search above to see care updates, '
                'behavior observations, and foster notes together.</div>'
                '</div>',
                unsafe_allow_html=True,
            )

with add_event_tab:
    # Keep reading and entry forms comfortable on wide screens.
    # The database tab below stays full width.
    left_margin, content_column, right_margin = st.columns([1, 4, 1])
    with content_column:
        st.header("Add a care update")
        st.markdown('<div class="section-intro">Capture what happened so the whole team has the context.</div>', unsafe_allow_html=True)

        with st.form(
            "add_behavior_event_form",
            clear_on_submit=True,
            enter_to_submit=False,
        ):
            st.markdown("#### 🐶 Who & when")
            pup_names = st.multiselect(
                "Pup names",
                options=[],
                placeholder="Type a pup name and press Enter",
                accept_new_options=True,
            )
            inputted_by = st.text_input(
                "Inputted by",
            )

            date_column, time_column = st.columns(2)
            with date_column:
                date = st.date_input("Date")
            with time_column:
                time = st.time_input("Time")

            st.markdown("#### 📝 What happened")
            concerns = st.multiselect(
                "Behavior concerns",
                options=list(BehaviorConcern),
                format_func=lambda concern: concern.value,
            )

            summary = st.text_area(
                "Summary of occurrence",
                placeholder="Describe the behavior or care update.",
            )

            st.markdown("#### 📍 Where")
            location = st.selectbox(
                "Location",
                options=[
                    "Foster",
                    "HQ",
                ],
            )

            submit_clicked = st.form_submit_button(
                "Save event",
                type="primary",
                use_container_width=True,
            )

        if submit_clicked:
            inputted_by = inputted_by.strip()
            summary = summary.strip()

            if not pup_names:
                st.error("Pup names are required.")

            elif not inputted_by:
                st.error("Inputted by is required.")

            elif not concerns:
                st.error("Select at least one behavior concern.")

            elif not summary:
                st.error("Summary of occurrence is required.")

            else:
                try:
                    timestamp = datetime.combine(
                        date,
                        time,
                    )
                    for pup_name in pup_names:
                        event = BehaviorEvent(
                            timestamp=timestamp,
                            event_id=(
                                str(timestamp)
                                + "-"
                                + pup_name
                                + "-"
                                + inputted_by
                            ),
                            inputted_by=inputted_by,
                            dog_name=pup_name,
                            source=EventSource.MANUAL,
                            concerns=concerns,
                            summary=summary,
                            location=location,
                        )

                        store_dog_info(event)

                    st.toast(
                        "Saved to database! 🐶",
                        icon="✅",
                    )

                    st.rerun()

                except Exception as exc:
                    st.error("Could not save the event.")
                    st.exception(exc)

   

with database_tab:
    st.subheader("Behavior database")
    st.caption("Search records, open full notes, and correct behavior tags.")
    try:
        events = get_all_behavior_events()

        total_dogs = len(set(event.dog_name.lower() for event in events))
        total_sources = len(set(event.source.value for event in events))
        first_stat, second_stat, third_stat = st.columns(3)
        with first_stat:
            st.markdown(
                f'<div class="stat-card"><div class="stat-label">Total events</div>'
                f'<div class="stat-number">{len(events):,}</div></div>',
                unsafe_allow_html=True,
            )
        with second_stat:
            st.markdown(
                f'<div class="stat-card"><div class="stat-label">Dogs recorded</div>'
                f'<div class="stat-number">{total_dogs:,}</div></div>',
                unsafe_allow_html=True,
            )
        with third_stat:
            st.markdown(
                f'<div class="stat-card"><div class="stat-label">Information sources</div>'
                f'<div class="stat-number">{total_sources:,}</div></div>',
                unsafe_allow_html=True,
            )

        st.markdown("**Search & filter**")
        # A form applies all three filters together when Search is clicked
        # or when Enter is pressed in the pup-name field.
        with st.form("database_search_form", border=False, enter_to_submit=True):
            concern_column, pup_column, date_column, button_column = st.columns(
                [2, 2, 2, 1], vertical_alignment="bottom"
            )
            with concern_column:
                selected_concern = st.selectbox(
                    "Behavior concern",
                    options=[None] + list(BehaviorConcern),
                    format_func=lambda concern: (
                        "All concerns" if concern is None else concern.value
                    ),
                )
            with pup_column:
                pup_name = st.text_input(
                    "Filter by pup name",
                    placeholder="Enter pup name",
                )
            with date_column:
                date_range = st.date_input(
                    "Filter by date range",
                    value=(),
                )
            with button_column:
                st.form_submit_button(
                    "Search",
                    type="primary",
                    use_container_width=True,
                )

        # Filter events
        filtered_events = []

        for event in events:

            # Filter by behavior concern
            if selected_concern is not None:
                if selected_concern not in event.concerns:
                    continue

            # Filter by pup name
            if pup_name:
                if pup_name.lower() not in event.dog_name.lower():
                    continue

            # Filter by date range
            if len(date_range) == 2:
                start_date, end_date = date_range

                if event.timestamp.date() < start_date:
                    continue

                if event.timestamp.date() > end_date:
                    continue

            filtered_events.append(event)

        st.caption(f"Showing {len(filtered_events)} of {len(events)} events")
        if not filtered_events:
            st.info("No matching behavior events.")

        else:
            # Keep the existing interactive table and row-click edit dialog.
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

            # Keep the selectable table, but show only the most useful columns.
            # Inputted By and Source are available in the full event dialog.
            st.markdown("**Event records** · Select a row for the full note and editable tags.")
            selection = st.dataframe(
                all_table_rows,
                width="stretch",
                hide_index=True,
                height=740,
                row_height=88,
                column_order=["Pup Name", "Timestamp", "Behavior Concern", "Summary"],
                on_select="rerun",
                selection_mode="single-row",
                column_config={
                    "Pup Name": st.column_config.TextColumn(
                        "Pup name",
                        width="small",
                    ),
                    "Timestamp": st.column_config.DatetimeColumn(
                        "Date",
                        format="MMM D, YYYY h:mm a",
                        width="small",
                    ),
                    "Behavior Concern": st.column_config.TextColumn(
                        "Behavior concern",
                        width="small",
                    ),
                    "Summary": st.column_config.TextColumn(
                        "Observation · select row for full text",
                        width="large",
                    ),
                },
            )

            if selection.selection.rows:
                selected_index = selection.selection.rows[0]
                selected_event = filtered_events[selected_index]

                selected_event_id = selected_event.event_id

                if st.session_state.get("opened_event_id") != selected_event_id:
                    st.session_state["opened_event_id"] = selected_event_id
                    show_event_details(selected_event)

            else:
                st.session_state["opened_event_id"] = None

    except Exception as exc:
        st.error("Could not load database events.")
        st.exception(exc)
