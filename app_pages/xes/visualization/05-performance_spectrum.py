import streamlit as st
import pm4py
from pm4py.algo.discovery.performance_spectrum import algorithm as performance_spectrum_discovery
from pm4py.visualization.performance_spectrum import visualizer
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
def show_event_to_object_types(log):
    # Get the list of activities
    list_activities = list(pm4py.get_event_attribute_values(log, "concept:name").keys())
    
    if not list_activities:
        st.error("No activities found in the log.")
        return
    
    # Discover the performance spectrum
    perf_spectrum = performance_spectrum_discovery.apply(log, list_activities)
    
    if "points" not in perf_spectrum or not perf_spectrum["points"]:
        st.error("No points found in the performance spectrum.")
        return
    
    # Generate the visualization with the given parameters
    gviz = visualizer.apply(perf_spectrum, variant=visualizer.Variants.NEATO)
    
    # Save the visualization to a temporary file and convert to base64
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
        temp_file.write(gviz.pipe(format='png'))
        img_base64 = image_to_base64(temp_file.name)
    
    st.subheader("Event to Object Types Graph")
    # Display the image in Streamlit
    st.image(f"data:image/png;base64,{img_base64}", caption="Event to Object Types Graph")

if 'log' not in st.session_state:
    st.warning("Please upload an OCEL event log first.")
else:
    log = st.session_state['log']
    st.title("OCEL 2.0 - Event to Object Relationships")
    
    # Interactive fields for Event to Object Types Graph
    st.sidebar.header("Event to Object Types Graph Settings")
        
    # Show the event to object types graph
    show_event_to_object_types(log)
