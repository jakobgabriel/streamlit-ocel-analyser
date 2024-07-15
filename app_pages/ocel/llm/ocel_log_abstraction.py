import streamlit as st
import pm4py

# Set the page configuration to wide
st.set_page_config(page_title="OCEL 2.0 - Abstraction of Object-Centric Event Log", layout="wide")

# Function to obtain the OCEL abstraction
def get_ocel_abstraction():
    st.title('OCEL Abstraction')
    if 'ocel' not in st.session_state:
        st.warning("No object-centric event log available. Please upload or generate an object-centric event log first.")
    else:
        ocel = st.session_state['ocel']
        
        st.sidebar.header("OCEL 2.0 Abstraction Settings")
        
        include_timestamps = st.sidebar.checkbox("Include Timestamps", value=True)
        
        if st.sidebar.button("Generate OCEL Abstraction"):
            try:
                ocel_abstraction = pm4py.llm.abstract_ocel(
                    ocel=ocel,
                    include_timestamps=include_timestamps
                )
                st.text(ocel_abstraction)
            except Exception as e:
                st.error(f"Error generating OCEL abstraction: {e}")

# Streamlit page structure
if 'ocel' not in st.session_state:
    st.warning("Please upload an object-centric event log first on the Upload page.")
else:
    st.title("Object-Centric Event Log OCEL Abstraction")
    get_ocel_abstraction()
