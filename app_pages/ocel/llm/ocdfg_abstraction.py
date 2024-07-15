import streamlit as st
import pm4py

# Set the page configuration to wide
st.set_page_config(page_title="OCEL 2.0 - OC-DFG Abstraction", layout="wide")

# Function to obtain the OCDFG abstraction
def get_ocdfg_abstraction():
    st.title('OC-DFG Abstraction')
    if 'ocel' not in st.session_state:
        st.warning("No object-centric event log available. Please upload or generate an object-centric event log first.")
    else:
        ocel = st.session_state['ocel']
        
        st.sidebar.header("OC-DFG Abstraction Settings")
        
        include_header = st.sidebar.checkbox("Include Header", value=True)
        include_timestamps = st.sidebar.checkbox("Include Timestamps", value=True)
        max_len = st.sidebar.number_input("Maximum Length", min_value=1, value=10000)
        
        if st.sidebar.button("Generate OCDFG Abstraction"):
            ocdfg_abstraction = pm4py.llm.abstract_ocel_ocdfg(
                ocel=ocel,
                include_header=include_header,
                include_timestamps=include_timestamps,
                max_len=max_len
            )
            st.text(ocdfg_abstraction)

# Streamlit page structure
if 'ocel' not in st.session_state:
    st.warning("Please upload an object-centric event log first on the Upload page.")
else:
    ocel = st.session_state['ocel']
    st.title("OCEL 2.0 - OC-DFG Abstraction")
    
    get_ocdfg_abstraction()