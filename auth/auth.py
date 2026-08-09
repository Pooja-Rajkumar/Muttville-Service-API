from datetime import datetime, timedelta, timezone
import secrets
from urllib.parse import urlencode
import gspread
import requests
import streamlit as st
from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from database.database import consume_google_oauth_state, save_google_oauth_state

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
]

GOOGLE_AUTH_URL = (
    "https://accounts.google.com/o/oauth2/v2/auth"
)

GOOGLE_TOKEN_URL = (
    "https://oauth2.googleapis.com/token"
)

REDIRECT_URI = (
    "https://dy9rxmwhhd56yjutls8uqs.streamlit.app/"
)

def build_google_login_url() -> str:
    state = secrets.token_urlsafe(16)
    save_google_oauth_state(state)

    params = {
        "client_id": st.secrets["google"]["client_id"],
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": " ".join(SCOPES),
        "state": state,
        "access_type": "offline",
        "prompt": "consent",
    }

    return f"{GOOGLE_AUTH_URL}?{urlencode(params)}"

def check_if_google_callback():
    query_params = st.query_params
    try:
        code = query_params.get("code")
        state = query_params.get("state")
    except Exception as e:
        print(f"Error occurred while fetching Google callback data: {e}")
        return None, None
    if code is None or state is None:
        return None # it is not a google callback request
    
    return code, state

def exchange_code_for_credentials(
    authorization_code: str,
) -> Credentials:
    data = {
        "code": authorization_code,
        "client_id": st.secrets["google"]["client_id"],
        "client_secret": st.secrets["google"]["client_secret"],
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    response = requests.post(GOOGLE_TOKEN_URL, data=data)
    response.raise_for_status()
    token_data = response.json()

    credentials = Credentials(
        token=token_data["access_token"],
        refresh_token=token_data.get("refresh_token"),
        token_uri=GOOGLE_TOKEN_URL,
        client_id=st.secrets["google"]["client_id"],
        client_secret=st.secrets["google"]["client_secret"],
        scopes=SCOPES,
    )

    return credentials


def complete_google_login() -> bool:
    callback_data = check_if_google_callback()
    if callback_data is None:
        return False

    valid_state = consume_google_oauth_state(callback_data)
    if not valid_state:
        st.error("Invalid OAuth state.")
        return False
    
    code, state = callback_data
    try:
        credentials = exchange_code_for_credentials(code)
        st.session_state["google_credentials"] = credentials
        return True
    except Exception as e:
        st.error(f"Error during Google login: {e}")
        return False

def get_credentials() -> Credentials | None:
    credentials = st.session_state.get("google_credentials")
    if credentials is None:
        return None

    if credentials.expired and credentials.refresh_token:
        try:
            credentials.refresh(Request())
            st.session_state["google_credentials"] = credentials
        except RefreshError as e:
            st.error(f"Error refreshing Google credentials: {e}")
            return None

    return credentials

def get_client():
    credentials = get_credentials()

    if credentials is None:
        return None

    return gspread.authorize(credentials)