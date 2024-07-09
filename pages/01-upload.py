import streamlit as st
import pm4py
import tempfile

# Set the page configuration to wide
st.set_page_config(page_title="OCEL 2.0 - Upload", layout="wide")

# Load ocel event log - only JSON support
def load_ocel(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as temp_file:
        temp_file.write(uploaded_file.read())
        temp_file_path = temp_file.name
    return pm4py.read_ocel2_json(temp_file_path)

st.title('OCEL 2.0 - Upload')

uploaded_file = st.file_uploader("Upload your JSON file", type="json")

if uploaded_file is not None:
    with st.spinner('Loading OCEL event log...'):
        ocel = load_ocel(uploaded_file)
        st.session_state['ocel'] = ocel
        st.success("File uploaded and OCEL event log loaded successfully!")