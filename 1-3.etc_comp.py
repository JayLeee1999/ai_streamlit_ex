import streamlit as st
from datetime import datetime

start_time = st.slider(
    "When do you start?",
    value=datetime(2025, 1, 1, 9, 30),
    format="MM/DD/YY - hh:mm",
)
st.write("Start time:", start_time