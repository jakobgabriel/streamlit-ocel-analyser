import streamlit as st
import pm4py
import pandas as pd
import plotly.express as px

# Set the page configuration to wide
st.set_page_config(page_title="OCEL 2.0 - Objects", layout="wide")

# Define the function to show extended relationship table
def show_objects_summary(ocel):
    objects_summary = pm4py.ocel_objects_summary(ocel)
    
    st.subheader("Objects Summary")
    with st.popover("Method"):
        st.markdown("""
                    ##### Method: `pm4py.ocel.ocel_objects_summary(ocel: OCEL) → DataFrame`
                    Gets the objects summary of an object-centric event log
                    """)
    st.dataframe(objects_summary)

st.title("OCEL 2.0 - Objects")

# Streamlit page structure
if 'ocel' not in st.session_state:
    st.warning("Please upload an OCEL event log first on the Upload page.")
else:
    ocel = st.session_state['ocel']
    show_objects_summary(ocel)