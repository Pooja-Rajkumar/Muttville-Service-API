import psycopg
import streamlit as st

from database.database import create_tables

connection = psycopg.connect(
    st.secrets["database"]["db_url"]
)

create_tables()

print("Tables created successfully.")