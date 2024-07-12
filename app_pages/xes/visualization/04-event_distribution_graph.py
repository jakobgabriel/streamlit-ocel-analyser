import streamlit as st
import pandas as pd
import pm4py
from io import BytesIO
import base64
import tempfile
from PIL import Image

# Set the page configuration to wide
st.set_page_config(page_title="Event Distribution Graph", layout="wide")

# Helper function to convert a saved image to a base64-encoded string
def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Function to show events distribution graph
def show_events_distribution_graph(log, file_format, distr_type):
    with tempfile.NamedTemporaryFile(suffix=f".{file_format}", delete=False) as temp_file:
        file_path = temp_file.name
        pm4py.save_vis_events_distribution_graph(
            log, file_path, distr_type=distr_type, activity_key='concept:name', timestamp_key='time:timestamp', case_id_key='case:concept:name'
        )
        img_base64 = image_to_base64(file_path)
    
    st.subheader("Events Distribution Graph")
    st.image(f"data:image/{file_format};base64,{img_base64}", caption="Events Distribution Graph")

# Streamlit page structure
st.title("Event Distribution Graph")

# Check if log is available in session_state
if 'log' not in st.session_state:
    st.warning("Please upload an event log first.")
else:
    log = st.session_state['log']

    # Interactive fields for Events Distribution Graph
    st.sidebar.header("Events Distribution Graph Settings")
    
    file_format = st.sidebar.selectbox("Format", options=["png", "svg"], index=0)
    distr_type = st.sidebar.selectbox(
        "Distribution Type",
        options=["days_week", "days_month", "months", "years", "hours"],
        index=0
    )
    
    show_events_distribution_graph(log, file_format, distr_type)
