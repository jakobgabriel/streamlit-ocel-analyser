import streamlit as st
import pandas as pd
import plotly.express as px
import re

# Set the page configuration to wide
st.set_page_config(page_title="OCEL 2.0 - Event Log Dashboard", layout="wide")

# Define the function to parse the summary string
def parse_summary(summary_text):
    # Extract general summary information
    general_pattern = r"\(number of events: (\d+), number of objects: (\d+), number of activities: (\d+), number of object types: (\d+), events-objects relationships: (\d+)\)"
    general_match = re.search(general_pattern, summary_text)
    number_of_events = int(general_match.group(1))
    number_of_objects = int(general_match.group(2))
    number_of_activities = int(general_match.group(3))
    number_of_object_types = int(general_match.group(4))
    events_objects_relationships = int(general_match.group(5))
    
    # Extract activities occurrences
    activities_pattern = r"Activities occurrences: {(.*?)}"
    activities_match = re.search(activities_pattern, summary_text)
    activities_str = activities_match.group(1)
    activities_occurrences = dict(re.findall(r"'([^']+)': (\d+)", activities_str))
    activities_occurrences = {k: int(v) for k, v in activities_occurrences.items()}
    
    # Extract object types occurrences
    object_types_pattern = r"Object types occurrences \(number of objects\): {(.*?)}"
    object_types_match = re.search(object_types_pattern, summary_text)
    object_types_str = object_types_match.group(1)
    object_types_occurrences = dict(re.findall(r"'([^']+)': (\d+)", object_types_str))
    object_types_occurrences = {k: int(v) for k, v in object_types_occurrences.items()}
    
    return {
        "number_of_events": number_of_events,
        "number_of_objects": number_of_objects,
        "number_of_activities": number_of_activities,
        "number_of_object_types": number_of_object_types,
        "events_objects_relationships": events_objects_relationships,
        "activities_occurrences": activities_occurrences,
        "object_types_occurrences": object_types_occurrences
    }

# Define the function to show the summary
def show_summary(ocel):
    summary_text = ocel.get_summary()
    
    # Parse the summary text
    parsed_summary = parse_summary(summary_text)
    
    # Display the general summary metrics next to each other
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Number of Events", parsed_summary["number_of_events"])
    col2.metric("Number of Objects", parsed_summary["number_of_objects"])
    col3.metric("Number of Activities", parsed_summary["number_of_activities"])
    col4.metric("Number of Object Types", parsed_summary["number_of_object_types"])
    col5.metric("Events-Objects Relationships", parsed_summary["events_objects_relationships"])

    # Show summary in a collapsible box with beautiful formatting
    with st.popover("Summary"):
        st.write(summary_text)

    # Convert the occurrences dictionaries to DataFrames
    activities_df = pd.DataFrame(list(parsed_summary["activities_occurrences"].items()), columns=['Activity', 'Occurrences'])
    object_types_df = pd.DataFrame(list(parsed_summary["object_types_occurrences"].items()), columns=['Object Type', 'Occurrences'])

    # Visualize the activities occurrences using a bar chart
    st.subheader('Activities Occurrences')
    activities_chart = px.bar(activities_df, x='Activity', y='Occurrences', title='Activities Occurrences')
    st.plotly_chart(activities_chart)

    # Visualize the object types occurrences using a bar chart
    st.subheader('Object Types Occurrences')
    object_types_chart = px.bar(object_types_df, x='Object Type', y='Occurrences', title='Object Types Occurrences')
    st.plotly_chart(object_types_chart)

# Streamlit page structure
st.title('OCEL Event Log Overview')

if 'ocel' not in st.session_state:
    st.warning("Please upload an OCEL event log first on the Upload page.")
else:
    ocel = st.session_state['ocel']
    show_summary(ocel)