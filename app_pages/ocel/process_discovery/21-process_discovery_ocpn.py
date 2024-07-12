import streamlit as st
import pm4py
from io import BytesIO
import base64
import tempfile
from PIL import Image

# Set the page configuration to wide
st.set_page_config(page_title="OCEL 2.0 - Process Discovery - OC-PN", layout="wide")

# Helper function to convert a saved image to a base64-encoded string
def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Define the function to show Petri net for the OCEL log
def show_object_centric_petri_net(ocel, format, bgcolor, rankdir):
    ocpn = pm4py.discover_oc_petri_net(ocel)
    
    with tempfile.NamedTemporaryFile(suffix=f".{format}", delete=False) as temp_file:
        file_path = temp_file.name
        pm4py.save_vis_ocpn(
            ocpn, file_path, 
            bgcolor=bgcolor, 
            rankdir=rankdir
        )
        img_base64 = image_to_base64(file_path)
    
    st.subheader("Object-Centric Petri Net (OC-PN)")
    # Display the image in Streamlit
    st.image(f"data:image/{format};base64,{img_base64}", caption="Object-Centric Petri Net")

# Streamlit page structure
if 'ocel' not in st.session_state:
    st.warning("Please upload an OCEL event log first on the Upload page.")
else:
    ocel = st.session_state['ocel']
    st.title("OCEL 2.0 - Process Discovery")
    
    # Interactive fields for Petri Net Visualization
    st.sidebar.header("Object Centric Petri Net Visualization Settings")
    
    format = st.sidebar.selectbox("Format", options=["png", "svg", "dot"], index=0)
    bgcolor = st.sidebar.color_picker("Background Color", value="#FFFFFF")
    rankdir = st.sidebar.selectbox("Rank Direction", options=["LR", "TB"], index=0)

    show_object_centric_petri_net(ocel, format, bgcolor, rankdir)
