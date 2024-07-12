import streamlit as st

st.set_page_config(page_title="Home", layout="wide")

st.title("Home")

st.subheader("Features")
st.markdown("""
            The OCEL Event Log Dashboard is a multi-page Streamlit application designed to visualize OCEL (Object-Centric Event Logs). 
            This app allows users to upload OCEL event logs, view summary statistics, and explore detailed object statistics through interactive visualizations.
            """)

# TODO