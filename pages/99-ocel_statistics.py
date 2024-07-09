import streamlit as st
import pm4py
import pandas as pd
import plotly.express as px

def show_object_types(ocel):
    st.subheader('Object Types')
    object_types = pm4py.ocel_get_object_types(ocel)
    st.write(", ".join(object_types))

def show_attribute_names(ocel):
    st.subheader('Attribute Names')
    attribute_names = pm4py.ocel_get_attribute_names(ocel)
    st.write(", ".join(attribute_names))

def show_object_type_activities(ocel):
    st.subheader('Object Type Activities')
    ot_activities = pm4py.ocel_object_type_activities(ocel)
    ot_activities_df = pd.DataFrame([
        {"Object Type": k, "Activities": ", ".join(v)}
        for k, v in ot_activities.items()
    ])
    st.dataframe(ot_activities_df)

def show_objects_ot_count(ocel):
    st.subheader('Objects OT Count')
    objects_ot_count = pm4py.ocel_objects_ot_count(ocel)
    objects_ot_count_df = pd.DataFrame(objects_ot_count).T.reset_index()
    st.dataframe(objects_ot_count_df)

def show_temporal_summary(ocel):
    st.subheader('Temporal Summary')
    temporal_summary = pm4py.ocel_temporal_summary(ocel)
    st.dataframe(temporal_summary)  # Display the dataframe to understand its structure
    if not temporal_summary.empty:
        fig = px.bar(temporal_summary, x='ocel:timestamp', y=temporal_summary.columns[1], title='Event Count Over Time')
        st.plotly_chart(fig)

def show_objects_summary(ocel):
    st.subheader('Objects Summary')
    objects_summary = pm4py.ocel_objects_summary(ocel)
    st.dataframe(objects_summary)  # Display the dataframe to understand its structure
    if not objects_summary.empty:
        fig = px.bar(objects_summary, x=objects_summary.columns[0], y=objects_summary.columns[1], title='Object Count per Type')
        st.plotly_chart(fig)

def show_objects_interactions_summary(ocel):
    st.subheader('Objects Interactions Summary')
    interactions_summary = pm4py.ocel_objects_interactions_summary(ocel)
    st.dataframe(interactions_summary)  # Display the dataframe to understand its structure
    if not interactions_summary.empty:
        fig = px.scatter(interactions_summary, x=interactions_summary.columns[0], y=interactions_summary.columns[1], title='Object Interactions by Event Activity')
        st.plotly_chart(fig)

st.title('OCEL Event Log Statistics')

if 'ocel' not in st.session_state:
    st.warning("Please upload an OCEL event log first on the Upload page.")
else:
    ocel = st.session_state['ocel']
    show_object_types(ocel)
    show_attribute_names(ocel)
    show_object_type_activities(ocel)
    show_objects_ot_count(ocel)
    show_temporal_summary(ocel)
    show_objects_summary(ocel)
    show_objects_interactions_summary(ocel)
