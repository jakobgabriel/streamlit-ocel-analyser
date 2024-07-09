import streamlit as st
import pandas as pd
import plotly.express as px

# Set the page configuration to wide
st.set_page_config(page_title="OCEL 2.0 - Event to Object Relationships", layout="wide")

# Define the function to show extended relationship table
def show_relationships(ocel):
    relationships = ocel.get_extended_table()
    st.dataframe(relationships)

# Streamlit page structure
if 'ocel' not in st.session_state:
    st.warning("Please upload an OCEL event log first on the Upload page.")
else:
    ocel = st.session_state['ocel']
    show_relationships(ocel)