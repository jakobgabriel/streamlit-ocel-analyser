import streamlit as st
import pm4py
from io import BytesIO
import base64
import tempfile
from PIL import Image

# Set the page configuration to wide
st.set_page_config(page_title="OCEL 2.0 - Process Discovery - OCDFG", layout="wide")

# Helper function to convert a saved image to a base64-encoded string
def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Define the function to show direct follows graph for the ocel log
def show_direct_follows_graph(ocel, act_threshold, edge_threshold, format, annotation, act_metric, edge_metric, performance_aggregation, bgcolor, rankdir):
    ocdfg = pm4py.discover_ocdfg(ocel)
    
    with tempfile.NamedTemporaryFile(suffix=f".{format}", delete=False) as temp_file:
        file_path = temp_file.name
        pm4py.save_vis_ocdfg(
            ocdfg, file_path, 
            annotation=annotation, 
            act_metric=act_metric, 
            edge_metric=edge_metric, 
            act_threshold=act_threshold, 
            edge_threshold=edge_threshold, 
            performance_aggregation=performance_aggregation, 
            bgcolor=bgcolor, 
            rankdir=rankdir
        )
        img_base64 = image_to_base64(file_path)
    
    st.subheader("Object Centric Direct Follows Graph (OC-DFG)")
    # Display the image in Streamlit
    st.image(f"data:image/{format};base64,{img_base64}", caption="Object Centric Direct Follows Graph")

# Streamlit page structure
if 'ocel' not in st.session_state:
    st.warning("Please upload an OCEL event log first on the Upload page.")
else:
    ocel = st.session_state['ocel']
    st.title("OCEL 2.0 - Process Discovery")
    
    # Interactive fields for Direct Follows Graph
    st.sidebar.header("Direct Follows Graph Settings")
    
    act_threshold = st.sidebar.slider("Activity Threshold", min_value=0, max_value=10000, value=0)
    edge_threshold = st.sidebar.slider("Edge Threshold", min_value=0, max_value=10000, value=0)
    format = st.sidebar.selectbox("Format", options=["png", "svg", "dot"], index=0)
    
    annotation = st.sidebar.selectbox("Annotation", options=["frequency", "performance"], index=0)
    act_metric = st.sidebar.selectbox("Activity Metric", options=["events", "unique_objects", "total_objects"], index=0)
    edge_metric = st.sidebar.selectbox("Edge Metric", options=["event_couples", "unique_objects", "total_objects"], index=0)
    performance_aggregation = st.sidebar.selectbox("Performance Aggregation", options=["mean", "median", "min", "max", "sum"], index=0)
    bgcolor = st.sidebar.color_picker("Background Color", value="#FFFFFF")
    rankdir = st.sidebar.selectbox("Rank Direction", options=["LR", "TB"], index=0)

    show_direct_follows_graph(ocel, act_threshold, edge_threshold, format, annotation, act_metric, edge_metric, performance_aggregation, bgcolor, rankdir)