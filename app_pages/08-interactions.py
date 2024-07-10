import streamlit as st
import pm4py

# Set the page configuration to wide
st.set_page_config(page_title="OCEL 2.0 - Object to Object Interactions", layout="wide")

# Define the function to show extended relationship table
def show_interactions(ocel):
    interactions = pm4py.ocel_objects_interactions_summary(ocel)   
    st.dataframe(interactions)

# Streamlit page structure
if 'ocel' not in st.session_state:
    st.warning("Please upload an OCEL event log first on the Upload page.")
else:
    ocel = st.session_state['ocel']
    st.title('OCEL - Object to Object Interactions')
    show_interactions(ocel)