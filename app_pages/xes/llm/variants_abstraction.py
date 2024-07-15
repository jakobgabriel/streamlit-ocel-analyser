import streamlit as st
import pm4py
import pandas as pd

# Set the page configuration to wide
st.set_page_config(page_title="Variants Abstraction of Event Log", layout="wide")

# Function to obtain the variants abstraction
def get_variants_abstraction():
    st.title('Variants Abstraction')
    if 'log' not in st.session_state:
        st.warning("No event log available. Please upload or generate an event log first.")
    else:
        log = st.session_state['log']
        
        # Ensure the timestamp is in datetime format
        log['time:timestamp'] = pd.to_datetime(log['time:timestamp'], utc=True)
        
        st.sidebar.header("Variants Abstraction Settings")
        
        max_len = st.sidebar.number_input("Maximum Length", min_value=1, value=10000)
        include_performance = st.sidebar.checkbox("Include Performance", value=True)
        relative_frequency = st.sidebar.checkbox("Use Relative Frequency", value=False)
        response_header = st.sidebar.checkbox("Include Response Header", value=True)
        
        primary_performance_aggregation = st.sidebar.selectbox(
            "Primary Performance Aggregation", 
            ["mean", "median", "min", "max", "sum", "stdev"],
            index=0
        )
        
        secondary_performance_aggregation = st.sidebar.selectbox(
            "Secondary Performance Aggregation (optional)",
            [None, "mean", "median", "min", "max", "sum", "stdev"],
            index=0
        )
        
        activity_key = st.sidebar.text_input("Activity Key", value="concept:name")
        timestamp_key = st.sidebar.text_input("Timestamp Key", value="time:timestamp")
        case_id_key = st.sidebar.text_input("Case ID Key", value="case:concept:name")
        
        if st.sidebar.button("Generate Variants Abstraction"):
            variants_abstraction = pm4py.llm.abstract_variants(
                log_obj=log,
                max_len=max_len,
                include_performance=include_performance,
                relative_frequency=relative_frequency,
                response_header=response_header,
                primary_performance_aggregation=primary_performance_aggregation,
                secondary_performance_aggregation=secondary_performance_aggregation,
                activity_key=activity_key,
                timestamp_key=timestamp_key,
                case_id_key=case_id_key
            )
            st.subheader("Variants Abstraction Result")
            st.text(variants_abstraction)

# Streamlit page structure
if 'log' not in st.session_state:
    st.warning("Please upload an event log first on the Upload page.")
else:
    log = st.session_state['log']
    st.title("Event Log Variants Abstraction")
    
    get_variants_abstraction()
