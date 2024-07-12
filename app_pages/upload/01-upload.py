import streamlit as st
import pm4py
import tempfile
from pm4py.objects.ocel.exporter.jsonocel.exporter import apply as export_jsonocel
from pm4py.objects.ocel.exporter.jsonocel.exporter import Variants
import json

# Set the page configuration to wide
st.set_page_config(page_title="OCEL 2.0 - Upload", layout="wide")

# Load OCEL event log - only JSON support
def load_ocel(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as temp_file:
        temp_file.write(uploaded_file.read())
        temp_file_path = temp_file.name
    return pm4py.read_ocel2_json(temp_file_path)

# Convert OCEL to JSONOCEL and return as dictionary
def convert_ocel_to_jsonocel(ocel):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jsonocel") as temp_export_file:
        export_path = temp_export_file.name
        export_jsonocel(ocel, export_path, variant=Variants.CLASSIC)
        with open(export_path, 'r') as jsonocel_file:
            jsonocel_data = json.load(jsonocel_file)
    return jsonocel_data

st.title('OCEL 2.0 - Upload')

uploaded_file = st.file_uploader("Upload your JSON file", type="json")

if uploaded_file is not None:
    with st.spinner('Loading OCEL event log...'):
        ocel = load_ocel(uploaded_file)
        st.session_state['ocel'] = ocel
        st.success("File uploaded and OCEL event log loaded successfully!")
        
        # Convert the loaded OCEL to JSONOCEL format and store in session state
        jsonocel = convert_ocel_to_jsonocel(ocel)
        st.session_state['jsonocel'] = jsonocel
        st.success("OCEL event log converted to JSONOCEL format and stored in session state successfully!")