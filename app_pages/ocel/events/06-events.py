import streamlit as st
import pm4py
import pandas as pd

def show_temporal_summary(ocel):
    st.subheader('Events Temporal Summary')
    temporal_summary = pm4py.ocel_temporal_summary(ocel)
    st.dataframe(temporal_summary)  # Display the dataframe to understand its structure

if 'ocel' not in st.session_state:
    st.warning("Please upload an OCEL event log first on the Upload page.")
else:
    ocel = st.session_state['ocel']
    st.title('OCEL - Events Temporal Summary')
    show_temporal_summary(ocel)