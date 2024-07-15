import streamlit as st
import pm4py
import tempfile
import requests
from pm4py.objects.ocel.exporter.jsonocel.exporter import apply as export_jsonocel
from pm4py.objects.ocel.exporter.jsonocel.exporter import Variants
import json

# Set the page configuration to wide
st.set_page_config(page_title="OCEL 2.0 - Upload or Get", layout="wide")

# Load OCEL event log - only JSON support
def load_ocel(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json", mode='w') as temp_file:
        temp_file.write(uploaded_file.read().decode('utf-8'))
        temp_file_path = temp_file.name
    return pm4py.read_ocel2_json(temp_file_path)

# Convert OCEL to JSONOCEL and return as dictionary
def convert_ocel_to_jsonocel(ocel):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jsonocel", mode='w') as temp_export_file:
        export_path = temp_export_file.name
        export_jsonocel(ocel, export_path, variant=Variants.CLASSIC)
        with open(export_path, 'r') as jsonocel_file:
            jsonocel_data = json.load(jsonocel_file)
    return jsonocel_data

# Retrieve OCEL log via API GET request
def get_ocel_via_api():
    response = requests.get("http://localhost:8000/api/ocel2/get")
    if response.status_code == 200 or response.status_code == 201:
        return response.json()
    else:
        st.error(f"Failed to retrieve OCEL log: {response.status_code} - {response.text}")
        return None

# Convert retrieved JSON to OCEL format
def convert_json_to_ocel(json_data):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json", mode='w') as temp_json_file:
        json.dump(json_data, temp_json_file)
        temp_json_file_path = temp_json_file.name
    return pm4py.read_ocel2_json(temp_json_file_path)

# Main UI
st.title('OCEL 2.0 - Upload or Get')

option = st.radio("Choose an option", ('Upload Event Log File', 'Get Event Log via API'))

if option == 'Upload Event Log File':
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

elif option == 'Get Event Log via API':
    with st.spinner('Retrieving OCEL event log via API...'):
        json_data = get_ocel_via_api()
        if json_data:
            if not any([json_data['objectTypes'], json_data['eventTypes'], json_data['objects'], json_data['events']]):
                st.warning("The OCEL log retrieved is empty.")
            else:
                # Convert JSON data to OCEL format
                ocel = convert_json_to_ocel(json_data)
                st.session_state['ocel'] = ocel
                
                # Convert the loaded OCEL to JSONOCEL format and store in session state
                jsonocel = convert_ocel_to_jsonocel(ocel)
                st.session_state['jsonocel'] = jsonocel
                st.success("OCEL event log retrieved and converted to JSONOCEL format successfully!")