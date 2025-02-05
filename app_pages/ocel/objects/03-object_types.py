import streamlit as st
import pm4py
import pandas as pd
import json 

# Set the page configuration to wide
st.set_page_config(page_title="OCEL 2.0 - Object Types", layout="wide")

def show_object_statistics(ocel):
    # Show the amount of object types
    object_types = pm4py.ocel_get_object_types(ocel)
    num_object_types = len(object_types)

    # Show the amount of object attribute types
    attribute_names = pm4py.ocel_get_attribute_names(ocel)
    num_attribute_names = len(attribute_names)

    # Display metrics side by side
    st.subheader("Object Type Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Number of Object Types", num_object_types)
    with col2:
        st.metric("Number of Object Attribute Types", num_attribute_names)

    # Show the table with Object type and activities in a collapsible container
    ot_activities = pm4py.ocel_object_type_activities(ocel)
    ot_activities_df = pd.DataFrame([
        {"Object Type": k, "Activities": ", ".join(v)}
        for k, v in ot_activities.items()
    ])
    
    st.subheader("Object Type and Activities")
    st.dataframe(ot_activities_df, use_container_width=True)

def show_attribute_names(ocel):
    st.subheader('Object and Event Attribute Names')
    attribute_names = pm4py.ocel_get_attribute_names(ocel)
    # Convert the attribute names to a DataFrame
    attribute_names_df = pd.DataFrame(attribute_names, columns=['Attribute Names'])
    # Display the DataFrame using st.dataframe
    st.dataframe(attribute_names_df)

if 'ocel' not in st.session_state:
    st.warning("Please upload an OCEL event log first on the Upload page.")
else:
    ocel = st.session_state['ocel']
    st.title('OCEL - Object Types')
    show_object_statistics(ocel)
    show_attribute_names(ocel)