import streamlit as st
import pm4py
from pm4py.visualization.ocel.eve_to_obj_types.variants import graphviz as visualizer
from io import BytesIO
import base64
import tempfile
from PIL import Image

# Set the page configuration to wide
st.set_page_config(page_title="OCEL 2.0 - Event to Object Relationships", layout="wide")

# Helper function to convert a saved image to a base64-encoded string
def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Define the function to show event to object types graph for the OCEL log
def show_event_to_object_types(ocel, parameters):
    # Generate the visualization with the given parameters
    gviz = visualizer.apply(ocel, parameters=parameters)
    
    # Save the visualization to a temporary file and convert to base64
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
        temp_file.write(gviz.pipe(format='png'))
        img_base64 = image_to_base64(temp_file.name)
    
    st.subheader("Event to Object Types Graph")
    # Display the image in Streamlit
    st.image(f"data:image/png;base64,{img_base64}", caption="Event to Object Types Graph")

# Define the function to show extended relationship table
def show_relationships(ocel):
    relationships = ocel.get_extended_table()
    st.subheader("Extended Relationship Table")
    st.dataframe(relationships)

# Streamlit page structure
if 'ocel' not in st.session_state:
    st.warning("Please upload an OCEL event log first on the Upload page.")
else:
    ocel = st.session_state['ocel']
    st.title("OCEL 2.0 - Event to Object Relationships")
    
    # Interactive fields for Event to Object Types Graph
    st.sidebar.header("Event to Object Types Graph Settings")
    
    rankdir = st.sidebar.selectbox("Rank Direction", options=["LR", "TB"], index=0)
    bgcolor = st.sidebar.color_picker("Background Color", value="#FFFFFF")
    
    parameters = {
        "rankdir": rankdir,
        "bgcolor": bgcolor,
    }
    
    # Show the extended relationship table
    show_relationships(ocel)
    
    # Show the event to object types graph
    show_event_to_object_types(ocel, parameters)