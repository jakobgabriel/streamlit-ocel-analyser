import streamlit as st
import pm4py
import pandas as pd
from io import BytesIO
import base64
import tempfile
from PIL import Image

# Set the page configuration to wide
st.set_page_config(page_title="OCEL 2.0 - Objects and Object Graph", layout="wide")

# Helper function to convert a saved image to a base64-encoded string
def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Define the function to show object graph for the OCEL log
def show_object_graph(ocel, graph_type, format, bgcolor, rankdir):
    obj_graph = pm4py.ocel.discover_objects_graph(ocel, graph_type=graph_type)

    with tempfile.NamedTemporaryFile(suffix=f".{format}", delete=False) as temp_file:
        file_path = temp_file.name
        pm4py.save_vis_object_graph(
            ocel, obj_graph, file_path, 
            bgcolor=bgcolor, 
            rankdir=rankdir
        )
        img_base64 = image_to_base64(file_path)
    
    st.subheader("Object Graph")
    # Display the image in Streamlit
    st.image(f"data:image/{format};base64,{img_base64}", caption="Object Graph")

# Define the function to show extended relationship table
def show_objects_summary(ocel):
    objects_summary = pm4py.ocel.ocel_objects_summary(ocel)
    
    st.subheader("Objects Summary")
    with st.expander("Method"):
        st.markdown("""
                    ##### Method: `pm4py.ocel.ocel_objects_summary(ocel: OCEL) → DataFrame`
                    Gets the objects summary of an object-centric event log
                    """)
    st.dataframe(objects_summary)

# Streamlit page structure
if 'ocel' not in st.session_state:
    st.warning("Please upload an OCEL event log first on the Upload page.")
else:
    ocel = st.session_state['ocel']
    st.title("OCEL 2.0 - Objects and Object Graph")
    
    # Interactive fields for Object Graph Visualization
    st.sidebar.header("Object Graph Visualization Settings")
    
    graph_type = st.sidebar.selectbox("Graph Type", options=["object_descendants", "object_interaction", "object_inheritance", "object_cobirth", "object_codeath"], index=0)
    format = st.sidebar.selectbox("Format", options=["png", "svg", "dot"], index=0)
    bgcolor = st.sidebar.color_picker("Background Color", value="#FFFFFF")
    rankdir = st.sidebar.selectbox("Rank Direction", options=["LR", "TB"], index=0)

    show_objects_summary(ocel)

    show_object_graph(ocel, graph_type, format, bgcolor, rankdir)