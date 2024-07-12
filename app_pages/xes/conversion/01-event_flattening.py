import streamlit as st
import pm4py
import pandas as pd

# Function to flatten the OCEL event log based on selected object types
def flatten_event_log_old(ocel, object_types):
    st.subheader(f'Flattened Event Log for Object Types: {", ".join(object_types)}')
    if len(object_types) == 1:
        flattened_log = pm4py.ocel_flattening(ocel, object_types[0])
    else:
        # Flatten the log for each object type and then combine the results
        flattened_logs = [pm4py.ocel_flattening(ocel, obj_type) for obj_type in object_types]
        # Merging all flattened logs on their common columns (case identifier, activity, timestamp)
        flattened_log = flattened_logs[0]
        for idx, log in enumerate(flattened_logs[1:], start=1):
            flattened_log = flattened_log.merge(log, on=["case:concept:name", "concept:name", "time:timestamp"], how="outer", suffixes=('', f'_type{idx}'))
    
    st.session_state['log'] = flattened_log
    st.dataframe(flattened_log)

def flatten_event_log(ocel, object_types):
    st.subheader(f'Flattened Event Log for Object Types: {", ".join(object_types)}')
    
    flattened_logs = []
    
    # Flatten the log for each object type
    for obj_type in object_types:
        flattened_log = pm4py.ocel_flattening(ocel, obj_type)
        flattened_logs.append(flattened_log)
    
    # Combine all flattened logs by appending them
    combined_log = pd.concat(flattened_logs, ignore_index=True)
    
    # Drop duplicate columns
    combined_log = combined_log.loc[:,~combined_log.columns.duplicated()]
    
    st.session_state['log'] = combined_log
    st.dataframe(combined_log)

# Check if OCEL is uploaded
if 'ocel' not in st.session_state:
    st.warning("Please upload an OCEL event log first on the Upload page.")
else:
    ocel = st.session_state['ocel']
    st.title('OCEL - Event Log Flattening')
    
    # Get object types
    object_types = pm4py.ocel_get_object_types(ocel)
    
    # Select object types for flattening
    selected_object_types = st.multiselect("Select Object Types for Flattening", object_types)
    
    if selected_object_types:
        # Show flattened event log based on selected object types
        flatten_event_log(ocel, selected_object_types)
