import streamlit as st
import pm4py
import plotly.express as px
import pandas as pd

# Set the page configuration to wide
st.set_page_config(page_title="Event Log Dotted Chart", layout="wide")

# Function to create a dotted chart
def create_dotted_chart():
    st.title('Dotted Chart')
    if 'log' not in st.session_state:
        st.warning("No flattened log available. Please go back and flatten the event log first.")
    else:
        log = st.session_state['log']
        
        # Ensure the timestamp is in datetime format
        log['time:timestamp'] = pd.to_datetime(log['time:timestamp'], utc=True)
        
        # Get the min and max timestamps
        min_timestamp = log['time:timestamp'].min()
        max_timestamp = log['time:timestamp'].max()
        
        # Get the list of unique cases
        unique_cases = log['case:concept:name'].unique()
        
        # Sidebar for filtering
        st.sidebar.header("Dotted Chart Settings")
        
        # Date input for selecting the range of timestamps
        start_date = st.sidebar.date_input("Start Date", min_timestamp.date())
        end_date = st.sidebar.date_input("End Date", max_timestamp.date())
        
        # Convert date inputs to datetime and localize to UTC
        start_date = pd.to_datetime(start_date).tz_localize('UTC')
        end_date = pd.to_datetime(end_date).tz_localize('UTC')
        
        # Slider for selecting the number of cases to display
        max_cases = st.sidebar.slider(
            "Select Number of Cases to Display",
            min_value=1,
            max_value=len(unique_cases),
            value=min(10, len(unique_cases))
        )
        
        # Filter the log based on the selected timestamp range and number of cases
        filtered_log = log[(log['time:timestamp'] >= start_date) & (log['time:timestamp'] <= end_date)]
        filtered_cases = filtered_log['case:concept:name'].unique()[:max_cases]
        filtered_log = filtered_log[filtered_log['case:concept:name'].isin(filtered_cases)]
        
        # Add dynamic filters for other columns
        columns_to_filter = [col for col in log.columns if col not in ['time:timestamp', 'case:concept:name', 'concept:name']]
        for column in columns_to_filter:
            unique_values = log[column].dropna().unique()
            options = ["All"] + list(unique_values)
            selected_values = st.sidebar.multiselect(f"Filter by {column}", options, default="All")
            if "All" not in selected_values:
                filtered_log = filtered_log[filtered_log[column].isin(selected_values)]
        
        fig = px.scatter(filtered_log, x='time:timestamp', y='case:concept:name', color='concept:name', 
                         title='Dotted Chart of Flattened Event Log')
        
        # Background color and legend options
        fig.update_layout(plot_bgcolor=st.sidebar.color_picker("Background Color", value="#FFFFFF"))
        fig.update_layout(showlegend=st.sidebar.checkbox("Show Legend", value=True))
        
        st.plotly_chart(fig)

# Streamlit page structure
if 'log' not in st.session_state:
    st.warning("Please upload an event log first on the Upload page.")
else:
    log = st.session_state['log']
    st.title("Event Log Dotted Chart Visualization")
    
    create_dotted_chart()