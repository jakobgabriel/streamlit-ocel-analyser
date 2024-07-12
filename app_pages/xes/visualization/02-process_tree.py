import streamlit as st
import pm4py
import pandas as pd
import base64
import tempfile
from io import BytesIO
import os

# Set the page configuration to wide
st.set_page_config(page_title="Process Tree Visualization", layout="wide")

# Helper function to convert a saved image to a base64-encoded string
def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Function to visualize and save process tree
def create_process_tree_visualization():
    st.title('Process Tree Visualization')
    if 'log' not in st.session_state:
        st.warning("No flattened log available. Please go back and flatten the event log first.")
    else:
        log = st.session_state['log']
        
        # Ensure the timestamp is in datetime format
        log['time:timestamp'] = pd.to_datetime(log['time:timestamp'], utc=True)
        
        # Discover the process tree using PM4Py
        process_tree = pm4py.discover_process_tree_inductive(log, activity_key='concept:name', case_id_key='case:concept:name', timestamp_key='time:timestamp')
        
        # Define file format and other parameters
        format = 'png'
        bgcolor = st.sidebar.color_picker("Background Color", value="#FFFFFF")
        rankdir = st.sidebar.selectbox("Rank Direction", options=["LR", "TB"], index=0)
        
        # Save the process tree visualization to a temporary file
        with tempfile.NamedTemporaryFile(suffix=f".{format}", delete=False) as temp_file:
            file_path = temp_file.name
            pm4py.save_vis_process_tree(process_tree, file_path, bgcolor=bgcolor, rankdir=rankdir)
            img_base64 = image_to_base64(file_path)
        
        st.subheader("Process Tree Visualization")
        # Display the image in Streamlit
        st.image(f"data:image/{format};base64,{img_base64}", caption="Process Tree")

        # Remove the temporary file after displaying it to clean up
        if os.path.exists(file_path):
            os.remove(file_path)

# Streamlit page structure
if 'log' not in st.session_state:
    st.warning("Please upload an event log first on the Upload page.")
else:
    log = st.session_state['log']
    st.title("Event Log Process Tree Visualization")
    
    create_process_tree_visualization()